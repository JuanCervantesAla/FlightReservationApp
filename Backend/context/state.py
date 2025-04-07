from protocol.circuit_braker import CircuitBreaker
import logging
import asyncio

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

def isActive(service):
    return services_status.get(service, {}).get("active", True)

def service_down(service):
    if service in services_status:
        services_status[service]["active"] = False
        services_status[service]["cb"].record_failure() 

def service_up(service):
    if service in services_status:
        services_status[service]["active"] = True
        services_status[service]["cb"].record_success() 

async def auto_reup(service, delay=10):
    await asyncio.sleep(delay)
    if not services_status[service]["active"]:
        services_status[service]["active"] = True
        services_status[service]["cb"].reset()
        logger.info(f"[AUTO-REUP] Service {service} automatically reactivated after {delay} seconds.")