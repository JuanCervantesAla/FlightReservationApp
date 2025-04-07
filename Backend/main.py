from fastapi import FastAPI, HTTPException
from protocol.reservation_handle import handle_reservation
from model.flights import get_flights
from model.users import get_users
from model.reservations import get_reservations_by_user
from context.state import service_down, service_up, services_status, auto_reup
from context.retry_queue import process_retrys
from pydantic import BaseModel
from database.addDataMongo import addFlights,addUsers
import random
from context.retry_queue import retry
import logging
import asyncio
from database.mongo import reservations_collection
from context.retry_queue import run_retry_processor
from fastapi import Query
import collections

#Creates app instance
app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

#Rservation request
class ReservationRequest(BaseModel):
    user_id : str
    flight_id: str

#On startup always listen
@app.on_event("startup")
async def startup_event():
    logger.info("Starting retry processor in background...")
    asyncio.create_task(run_retry_processor())

#Get the flights
@app.get("/flights")
async def listingFlights():
    return await get_flights()

#Get the users
@app.get("/users")
async def listingUsers():
    return await get_users()

#Get reservations of a user
@app.get("/reservations")
async def get_user_reservations(user_id: str = Query(...)):
    return await get_reservations_by_user(user_id)

#Reserve
@app.post("/reserve")
async def reserve(data: ReservationRequest):
    logger.info(f"[Reserve Request] User: {data.user_id}, Flight: {data.flight_id}")

    async def reserve_operation():
        if random.random() < 0.7:
            raise Exception("Simulated reservation error")
        return await handle_reservation(data.user_id, data.flight_id, "confirmed")
    return await call_services("reservations", reserve_operation)

#Down a service
@app.post("/failure/{service}")
def failure(service: str):
    if service in services_status:
        services_status[service]["active"] = False
        services_status[service]["cb"].record_failure()
        logger.warning(f"Service {service} marked down as inactive.")

        asyncio.create_task(auto_recover_service(service, delay=15))

        return {"state": f"{service} inactive (will auto re-up in 15s)"}
    return {"state": "Service not found"}

#Auto recovery service
async def auto_recover_service(service: str, delay: int = 15):
    await asyncio.sleep(delay)
    if service in services_status:
        services_status[service]["active"] = True
        services_status[service]["cb"].reset()
        logger.info(f"[Auto-Recovery] {service} auto re-up after {delay}s.")

#Manual reup service
@app.post("/reup/{service}")
def reUp(service: str):
    if service in services_status:
        services_status[service]["active"] = True
        services_status[service]["cb"].reset()
        logger.info(f"Service {service} restaured and active.")
        return {"state": f"{service} active"}
    return {"state": "Service not found"}

#Get service status
@app.get("/status")
async def status():
    logger.info("Services status.")
    return {
        service: {
            "active": config["active"],
            "circuit_breaker": config["cb"].state,
            "failure_count": config["cb"].failure_count
        }
        for service, config in services_status.items()
    }

#Hardcode data
@app.get("/hardcodeflights")
def hardcodeFlights():
    addFlights()
    return{"state":"Flights added"}

@app.get("/hardcoreusers")
def hardcodeUsers():
    addUsers()
    return{"state":"Users added"}

@app.get("/reservation_status/{user_id}/{flight_id}")
async def reservation_status(user_id: str, flight_id: str):
    reservation = await reservations_collection.find_one({
        "user_id": user_id,
        "flight_id": flight_id
    })
    if reservation:
        return {"status": reservation["status"], "msg": "Reservation found"}
    return {"status": "not_found", "msg": "Reservation not found"}

#Call the services
@retry()
async def call_services(service_name: str, operation):
    service = services_status.get(service_name)
    if not service or not service["active"]:
        logger.warning(f"[Circuit Breaker] {service_name} is down.")
        asyncio.create_task(auto_reup(service_name, delay=10))
        return {"status": "pending", "msg": f"{service_name} is down. Attempting to auto-recover... Will retry soon."}
    
    cb = service["cb"]
    if not cb.is_request_allowed():
        logger.warning(f"[Circuit Breaker] {service_name} is OPEN or not ready.")
        return {"status": "pending", "msg": "Service temporarily unavailable. Will retry."}
    
    try:
        result = await operation()
        cb.record_success()
        return result
    except Exception as e:
        cb.record_failure()
        logger.error(f"[Try] Error in {service_name}: {e}")
        return {"status": "pending", "msg": "Reservation failed. Retrying in background."}

