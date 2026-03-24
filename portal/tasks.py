import httpx
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def sync_all_news():
    """
    Task to trigger full news synchronization from FastAPI Backend.
    This call is non-blocking on the API side as it runs in the background.
    """
    url = f"{settings.API_BASE_URL}/api/sync/full"
    logger.info(f"Triggering scheduled sync at {url}")
    
    try:
        # Use synchronous client for the scheduler task
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json={"articles_per_domain": 15})
            if response.status_code == 200:
                logger.info("Successfully triggered news synchronization.")
                return True
            else:
                logger.error(f"Failed to trigger sync. Status: {response.status_code}")
    except Exception as e:
        logger.error(f"Error during scheduled sync trigger: {e}")
    
    return False
