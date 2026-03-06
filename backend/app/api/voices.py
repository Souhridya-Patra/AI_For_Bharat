"""Voice management API endpoints."""
import logging
from fastapi import APIRouter, HTTPException, Path
from app.models.schemas import VoiceListResponse, VoiceModel, ErrorResponse
from app.services.aws_client import aws_client
from app.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/voices",
    response_model=VoiceListResponse,
    responses={
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def list_voices():
    """
    List all voice models for the authenticated user.
    
    Returns a list of voice models with metadata including name,
    creation date, and reference audio duration.
    """
    # TODO: Get user_id from authentication
    user_id = "demo_user"
    
    logger.info(f"Listing voices for user_id={user_id}")
    
    try:
        table = aws_client.dynamodb.Table(settings.dynamodb_voices_table)
        
        # Query voices by user_id
        # Note: This requires a GSI on user_id in production
        response = table.scan(
            FilterExpression='user_id = :user_id',
            ExpressionAttributeValues={':user_id': user_id}
        )
        
        voices = []
        for item in response.get('Items', []):
            voice = VoiceModel(
                id=item['id'],
                name=item['name'],
                user_id=item['user_id'],
                created_at=datetime.fromisoformat(item['created_at']),
                reference_audio_duration=item['reference_audio_duration'],
                is_shared=item.get('is_shared', False),
                shared_with=item.get('shared_with', [])
            )
            voices.append(voice)
        
        logger.info(f"Found {len(voices)} voices for user {user_id}")
        
        return VoiceListResponse(
            voices=voices,
            total=len(voices)
        )
    
    except Exception as e:
        # If table doesn't exist, return empty list for demo
        if 'ResourceNotFoundException' in str(e):
            logger.warning(f"DynamoDB table not found, returning empty list")
            return VoiceListResponse(voices=[], total=0)
        
        logger.error(f"Failed to list voices: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "LIST_FAILED",
                    "message": "Failed to retrieve voice list",
                    "details": str(e) if settings.debug else None
                }
            }
        )


@router.delete(
    "/voices/{voice_id}",
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def delete_voice(
    voice_id: str = Path(..., description="Voice model ID to delete")
):
    """
    Delete a voice model.
    
    Removes the voice model and all associated data including
    reference audio and embeddings.
    """
    # TODO: Get user_id from authentication
    user_id = "demo_user"
    
    logger.info(f"Deleting voice: voice_id={voice_id}, user_id={user_id}")
    
    try:
        table = aws_client.dynamodb.Table(settings.dynamodb_voices_table)
        
        # Get voice to verify ownership
        response = table.get_item(Key={'id': voice_id})
        
        if 'Item' not in response:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": {
                        "code": "VOICE_NOT_FOUND",
                        "message": f"Voice model not found: {voice_id}"
                    }
                }
            )
        
        voice = response['Item']
        
        # Verify ownership
        if voice['user_id'] != user_id:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "You don't have permission to delete this voice"
                    }
                }
            )
        
        # Delete from DynamoDB
        table.delete_item(Key={'id': voice_id})
        
        # TODO: Delete reference audio from S3
        # TODO: Schedule cleanup of associated data
        
        logger.info(f"Voice deleted successfully: {voice_id}")
        
        return {"status": "deleted", "voice_id": voice_id}
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Failed to delete voice: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "DELETE_FAILED",
                    "message": "Failed to delete voice",
                    "details": str(e) if settings.debug else None
                }
            }
        )
