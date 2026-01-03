import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_api_call(endpoint: str, method: str, user_id: str = None, status_code: int = None):
    """Log API calls for monitoring and debugging"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "status_code": status_code
    }
    logger.info(f"API_CALL: {json.dumps(log_data)}")

def log_error(error: Exception, context: str = ""):
    """Log errors with context for debugging"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "context": context,
        "error_type": type(error).__name__,
        "error_message": str(error)
    }
    logger.error(f"ERROR: {json.dumps(log_data)}")

def log_security_event(event_type: str, user_id: str = None, details: dict = None):
    """Log security-related events"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "details": details
    }
    logger.warning(f"SECURITY: {json.dumps(log_data)}")