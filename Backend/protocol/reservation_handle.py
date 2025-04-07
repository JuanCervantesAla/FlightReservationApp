from model.flights import reserve_space
from model.reservations import create_reservation
from model.users import validate_user
from context.state import isActive, services_status, service_up
from context.retry_queue import add_try
import logging
import asyncio

#Reservation handler just takes the info from the flights and attempt to reserve

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

#Making a reservation
async def handle_reservation(user_id, flight_id, status):
    logger.info(f"Attempting reservation: Flight {flight_id}, User {user_id}")

    #Validating user
    if not await validate_user(user_id):
        logger.warning(f"Invalid user: {user_id}")
        return {"status": "error", "msg": "User not valid"}

    try:
        if not isActive("reservations") or not isActive("flights"):
            raise Exception("Simulated service down")

        #Reserve the sit
        if await reserve_space(flight_id):
            await create_reservation(user_id, flight_id, status)
            logger.info(f"Reservation successful: Flight {flight_id}, User {user_id}")
            return {"status": "ok", "msg": "Reservation successful"}
        else:#If not available sits left
            logger.info(f"No seats available on flight {flight_id}")
            return {"status": "error", "msg": "No seats available on this flight"}

    except Exception as e:
        logger.error(f"Reservation failed with error: {e}")
        add_try(handle_reservation, user_id, flight_id, status)

        #Trying to reup the service
        async def restore_service():
            await asyncio.sleep(5)
            service_up("reservations")
            logger.info("Auto reup: Servicio 'reservations' restaurado automáticamente.")

        asyncio.create_task(restore_service())

        return {"status": "pending", "msg": "Reservation failed, retrying later"}
