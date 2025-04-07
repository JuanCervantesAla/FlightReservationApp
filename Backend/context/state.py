from protocol.circuit_braker import CircuitBreaker
import logging
import asyncio

#This file is for the status of the services
#Every service has an status and a cirbuit breaker that will automatically try
#To reUp the service if down(False) and has a fallback if cant reUp

logger = logging.getLogger(__name__)

services_status = {
    "reservations": {
        "active": True,
        "cb": CircuitBreaker(max_failures=3, reset_timeout=10),
        "fallback": lambda: {"message": "Using data on cache"}
    },
    "flights": {
        "active": True,
        "cb": CircuitBreaker(max_failures=3, reset_timeout=10),
        "fallback": lambda: {"message": "Services not available"}
    }
}

#Verifies if service active
def isActive(service):
    return services_status.get(service, {}).get("active", True)

#Verifies if service down
def service_down(service):
    if service in services_status:
        services_status[service]["active"] = False
        services_status[service]["cb"].record_failure() 

#Set the service manually up
def service_up(service):
    if service in services_status:
        services_status[service]["active"] = True
        services_status[service]["cb"].record_success() 

#AutoReup the service using the circuit breaker
async def auto_reup(service, delay=10):
    await asyncio.sleep(delay)
    if not services_status[service]["active"]:
        services_status[service]["active"] = True
        services_status[service]["cb"].reset()
        logger.info(f"[AUTO-REUP] Service {service} automatically reactivated after {delay} seconds.")