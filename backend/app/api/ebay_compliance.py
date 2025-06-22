from fastapi import APIRouter, Depends, Request, Response, status, Header
from pydantic import BaseModel, Field
import hashlib
import hmac
import json
import base64
from typing import Dict, Any, Optional
import logging
from concurrent.futures import ThreadPoolExecutor
from starlette.concurrency import run_in_threadpool

from app.services.vector_db import VectorDBService
from app.dependencies import get_vector_db_service
from app.core.config import settings

router = APIRouter()

logger = logging.getLogger(__name__)

class ChallengeResponse(BaseModel):
    challenge_response: str = Field(..., alias="challengeResponse")

class EbayNotification(BaseModel):
    metadata: Dict[str, Any]
    notification: Dict[str, Any]

@router.get("/ebay-compliance")
async def handle_challenge_request(challenge_code: str, response: Response):
    """
    Handles eBay's challenge request to verify the endpoint.
    """
    if not settings.EBAY_VERIFICATION_TOKEN:
        logger.error("EBAY_VERIFICATION_TOKEN is not set.")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Application is not configured for eBay compliance."}

    # As per eBay's documentation, the challenge response is a SHA256 hash of the
    # challenge code, the verification token, and the endpoint URL.
    
    # The endpoint URL must be the public URL provided to eBay.
    # We will need to store this in an environment variable as well.
    endpoint_url = settings.EBAY_COMPLIANCE_ENDPOINT_URL
    if not endpoint_url:
        logger.error("EBAY_COMPLIANCE_ENDPOINT_URL is not set.")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Application is not configured with a compliance endpoint URL."}

    # Create the SHA256 hash
    hasher = hashlib.sha256()
    hasher.update(challenge_code.encode('utf-8'))
    hasher.update(settings.EBAY_VERIFICATION_TOKEN.encode('utf-8'))
    hasher.update(endpoint_url.encode('utf-8'))
    
    challenge_response_hash = hasher.hexdigest()
    
    response.status_code = status.HTTP_200_OK
    return {"challengeResponse": challenge_response_hash}


@router.post("/ebay-compliance")
async def handle_notification(
    request: Request,
    vector_db_service: VectorDBService = Depends(get_vector_db_service)
):
    """
    Handles account deletion notifications from eBay.
    """
    # First, verify the notification is from eBay
    # This involves using the x-ebay-signature header
    # For now, we will skip this and proceed with deletion logic.
    # In a production environment, this verification is critical.

    try:
        payload = await request.json()
        notification = EbayNotification(**payload)

        if notification.metadata.get("topic") == "MARKETPLACE_ACCOUNT_DELETION":
            user_id = notification.notification.get("data", {}).get("userId")
            username = notification.notification.get("data", {}).get("username")
            
            if username:
                logger.info(f"Received account deletion request for user_id: {user_id} (username: {username})")

                try:
                    # The 'username' from the notification corresponds to the 'vendor' in our database
                    await run_in_threadpool(vector_db_service.delete_by_vendor, username)
                    logger.info(f"Successfully processed deletion for user: {username}")

                except Exception as e:
                    logger.error(f"Error deleting data for user {username}: {e}")
                    # Even if deletion fails, we should still acknowledge the notification
                    # to prevent eBay from resending it. The error is logged for manual intervention.
                    pass

    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from eBay notification.")
        # Don't send a 400, because eBay will retry. Better to send 204 and log the error.
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        # Acknowledge to prevent retries
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Acknowledge the notification to prevent eBay from resending it.
    return Response(status_code=status.HTTP_204_NO_CONTENT) 