from datetime import datetime, timedelta
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=10, recovery_timeout=20):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout  
        self.recovery_timeout = recovery_timeout  
        self.failure_count = 0
        self.last_failure_time = None
        self.last_success_time = None
        self.state = "CLOSED"  

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        logger.warning(f"[Breaker] Failure recorded ({self.failure_count}/{self.max_failures})")

        if self.failure_count >= self.max_failures and self.state != "OPEN":
            self.state = "OPEN"
            logger.error(f"[Breaker] Max failures reached. Circuit is now OPEN.")

    def record_success(self):
        if self.state != "CLOSED":
            logger.info(f"[Breaker] Successful call. Circuit now CLOSED.")
        self.failure_count = 0
        self.last_success_time = datetime.now()
        self.state = "CLOSED"

    def is_request_allowed(self):
        now = datetime.now()

        if self.state == "CLOSED" and self.last_success_time:
            inactive_time = (now - self.last_success_time).total_seconds()
            if inactive_time > self.recovery_timeout:
                logger.info(f"[Breaker] Inactive for {inactive_time:.1f}s. Resetting.")
                self.reset()

        if self.state == "OPEN":
            elapsed = (now - self.last_failure_time).total_seconds()
            if elapsed > self.reset_timeout:
                self.state = "HALF_OPEN"
                logger.info(f"[Breaker] Timeout passed. Trying HALF_OPEN state.")
                return True
            logger.warning(f"[Breaker] OPEN. Retry in {self.reset_timeout - elapsed:.1f}s.")
            return False

        if self.state == "HALF_OPEN":
            return True

        return True

    def reset(self):
        logger.info(f"[Breaker] Resetting circuit breaker to CLOSED.")
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
