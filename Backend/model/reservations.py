from database.mongo import reservations_collection, flights_collection
from datetime import datetime
from bson import ObjectId

import logging
logger = logging.getLogger(__name__)

async def create_reservation(user_id, flight_id, status):
    reservation = {
        "user_id": user_id,
        "flight_id": flight_id,
        "status": status,
        "dateFlight": datetime.utcnow()
    }

    result = await reservations_collection.insert_one(reservation)
    
    if result.inserted_id:
        logger.info(f"[MongoDB] Reservation done: {result.inserted_id}")
    else:
        logger.error("[MongoDB] Error at reserving.")
        raise Exception("Reservation not saved in DB")

    return True

async def find_reservation(user_id: str = None, flight_id: str = None):
    query = {}
    if user_id:
        query["user_id"] = user_id
    if flight_id:
        query["flight_id"] = flight_id

    results = await reservations_collection.find(query).to_list(length=100)
    return results

async def get_reservations_by_user(user_id: str):
    results = []
    async for reservation in reservations_collection.find({"user_id": user_id}):
        flight = await flights_collection.find_one({"_id": ObjectId(reservation["flight_id"])})
        if flight:
            reservation["from"] = flight.get("from")
            reservation["to"] = flight.get("to")
            reservation["date"] = flight.get("date")
            reservation["price"] = flight.get("price")
        reservation["_id"] = str(reservation["_id"])
        results.append(reservation)
    return results