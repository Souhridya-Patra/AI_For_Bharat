"""Voice cloning API endpoints."""
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import VoiceCloneRequest, VoiceCloneResponse, ErrorResponse
from app.services.cloning_module import cloning_module, InvalidAudioDurationError, MultipleSpeakersError
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/clone",
    response_model=VoiceCloneResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def clone_voice(
    audio_file: UploadFile = File(..., description="Audio file (6-10 seconds)"),
    voice_name: str = Form(..., description="Name for the cloned voice")
):
    """
    Clone a voice from an audio sample.
    
    Upload an audio file (6-10 seconds) to create a custom voice model.
    The audio should contain a single speaker with clear speech.
    """
    logger.info(f"Voice cloning request: voice_name={voice_name}, filename={audio_file.filename}")
    
    # TODO: Get user_id from authentication
    user_id = "demo_user"
    
    try:
        # Read audio file
        audio_bytes = await audio_file.read()
        
        # Validate file size (max 10MB)
        if len(audio_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": {
                        "code": "FILE_TOO_LARGE",
                        "message": "Audio file must be less than 10MB",
                        "details": {
                            "max_size_mb": 10,
                            "provided_size_mb": len(audio_bytes) / (1024 * 1024)
                        }
                    }
                }
            )
        
        # Clone voice
        voice_id = cloning_module.clone_voice(
            audio_bytes=audio_bytes,
            voice_name=voice_name,
            user_id=user_id
        )
        
        return VoiceCloneResponse(
            voice_id=voice_id,
            status="success",
            message=f"Voice '{voice_name}' cloned successfully"
        )
    
    except InvalidAudioDurationError as e:
        logger.error(f"Invalid audio duration: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_AUDIO_DURATION",
                    "message": str(e),
                    "details": {
                        "provided_duration": e.duration,
                        "min_duration": e.min_duration,
                        "max_duration": e.max_duration
                    }
                }
            }
        )
    
    except MultipleSpeakersError as e:
        logger.error(f"Multiple speakers detected: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "MULTIPLE_SPEAKERS",
                    "message": str(e)
                }
            }
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e)
                }
            }
        )
    
    except Exception as e:
        logger.error(f"Voice cloning failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "CLONING_FAILED",
                    "message": "Failed to clone voice",
                    "details": str(e) if settings.debug else None
                }
            }
        )
