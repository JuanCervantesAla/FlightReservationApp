import time
import random
from functools import wraps
from asyncio import timeout
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

queueRetry = []

def add_try(func, *args):
    queueRetry.append((func,args))

def retry(max_retries=3, initial_delay=1, backoff_factor=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            while retries < max_retries:
                try:
                    logger.info(f"Trying to execute {func.__name__} try {retries + 1} of {max_retries}")
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.warning(f"Error  {func.__name__} (try {retries}): {e}")
                    if retries >= max_retries:
                        logger.error(f"{func.__name__} failure after {max_retries} tries.")
                        raise
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
                    logger.info(f"Trying {func.__name__} in {delay} secs...")
        return wrapper
    return decorator

async def run_retry_processor():
    while True:
        await asyncio.sleep(5)  
        logger.info("[Retry Processor] Checking queue...")
        for func, args in queueRetry.copy():
            try:
                await func(*args)
                logger.info(f"[Retry Processor] Retried {func.__name__} successfully!")
                queueRetry.remove((func, args))
            except Exception as e:
                logger.warning(f"[Retry Processor] Retry failed: {e}")

def process_retrys():
    for func, args in queueRetry.copy():
        try:
            func(*args)
            queueRetry.remove((func,args))
        except Exception:
            continue