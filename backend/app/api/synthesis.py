"""Synthesis API endpoints."""
import logging
import uuid
import io
import soundfile as sf
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from app.models.schemas import SynthesisRequest, SynthesisResponse, ErrorResponse
from app.services.synthesis_engine import synthesis_engine
from app.services.aws_client import aws_client
from app.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/synthesize",
    response_model=SynthesisResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def synthesize_speech(request: SynthesisRequest):
    """
    Synthesize speech from text.
    
    This endpoint converts text to speech using the specified voice model.
    Supports both synchronous and streaming modes.
    """
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    logger.info(f"[{request_id}] Synthesis request: voice_id={request.voice_id}, stream={request.stream}")
    
    try:
        # Validate voice exists (TODO: implement voice validation)
        
        if request.stream:
            # Streaming mode
            return StreamingResponse(
                _stream_audio(request, request_id),
                media_type="audio/wav",
                headers={
                    "X-Request-ID": request_id,
                    "Cache-Control": "no-cache"
                }
            )
        else:
            # Synchronous mode
            audio_data = synthesis_engine.synthesize(
                text=request.text,
                voice_id=request.voice_id,
                speed=request.speed,
                pitch=request.pitch,
                language=request.language
            )
            
            # Save audio to S3
            audio_url = await _save_audio_to_s3(audio_data, request_id)
            
            # Calculate duration
            sample_rate = 24000  # TODO: Get from synthesis engine
            if isinstance(audio_data, bytes):
                # PCM audio: 2 bytes per sample (16-bit)
                duration = len(audio_data) / (sample_rate * 2)
            else:
                # Numpy array
                duration = len(audio_data) / sample_rate
            
            return SynthesisResponse(
                audio_url=audio_url,
                duration=duration,
                sample_rate=sample_rate,
                request_id=request_id
            )
    
    except ValueError as e:
        logger.error(f"[{request_id}] Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e),
                    "request_id": request_id
                }
            }
        )
    
    except Exception as e:
        logger.error(f"[{request_id}] Synthesis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "SYNTHESIS_FAILED",
                    "message": "Failed to synthesize audio",
                    "details": str(e) if settings.debug else None,
                    "request_id": request_id
                }
            }
        )


async def _stream_audio(request: SynthesisRequest, request_id: str):
    """Stream audio chunks."""
    try:
        for chunk in synthesis_engine.synthesize_streaming(
            text=request.text,
            voice_id=request.voice_id,
            speed=request.speed,
            pitch=request.pitch,
            language=request.language
        ):
            # Handle both bytes (Polly) and numpy arrays (Mock/SageMaker)
            if isinstance(chunk, bytes):
                # Convert PCM bytes to WAV
                import wave
                buffer = io.BytesIO()
                with wave.open(buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(24000)
                    wav_file.writeframes(chunk)
                buffer.seek(0)
                yield buffer.read()
            else:
                # Convert numpy array to WAV bytes
                buffer = io.BytesIO()
                sf.write(buffer, chunk, 24000, format='WAV')
                buffer.seek(0)
                yield buffer.read()
    
    except Exception as e:
        logger.error(f"[{request_id}] Streaming failed: {e}", exc_info=True)
        raise


async def _save_audio_to_s3(audio_data, request_id: str) -> str:
    """Save audio to S3 and return URL."""
    try:
        # Determine audio format based on data type and content
        if isinstance(audio_data, bytes):
            # Check if it's MP3 (gTTS) or PCM (Polly)
            # MP3 files start with ID3 tag or MPEG sync bytes
            is_mp3 = (len(audio_data) > 3 and 
                     (audio_data[:3] == b'ID3' or 
                      audio_data[:2] == b'\xff\xfb' or 
                      audio_data[:2] == b'\xff\xf3' or
                      audio_data[:2] == b'\xff\xf2'))
            
            if is_mp3:
                # gTTS returns MP3 directly - no conversion needed
                logger.info(f"Detected MP3 format from gTTS, size={len(audio_data)} bytes")
                audio_bytes = audio_data
                file_extension = "mp3"
                content_type = "audio/mpeg"
            else:
                # Convert PCM bytes to WAV (Polly)
                logger.info(f"Converting PCM to WAV, size={len(audio_data)} bytes")
                import wave
                buffer = io.BytesIO()
                with wave.open(buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(24000)
                    wav_file.writeframes(audio_data)
                buffer.seek(0)
                audio_bytes = buffer.read()
                file_extension = "wav"
                content_type = "audio/wav"
        else:
            # Convert numpy array to WAV bytes (Mock/SageMaker)
            logger.info(f"Converting numpy array to WAV")
            buffer = io.BytesIO()
            sf.write(buffer, audio_data, 24000, format='WAV')
            buffer.seek(0)
            audio_bytes = buffer.read()
            file_extension = "wav"
            content_type = "audio/wav"
        
        logger.info(f"Final audio: format={file_extension}, size={len(audio_bytes)} bytes")
        
        # Generate S3 key
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        s3_key = f"synthesized/{timestamp}/{request_id}.{file_extension}"
        
        # Upload to S3 with public-read ACL
        try:
            # Create new buffer for upload
            upload_buffer = io.BytesIO(audio_bytes)
            aws_client.s3.upload_fileobj(
                upload_buffer,
                settings.s3_bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'
                }
            )
            
            # Return public URL
            url = f"https://{settings.s3_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            
        except Exception as acl_error:
            # If public-read fails, use presigned URL
            logger.warning(f"Public upload failed, using presigned URL: {acl_error}")
            
            # Create new buffer for retry
            upload_buffer = io.BytesIO(audio_bytes)
            aws_client.s3.upload_fileobj(
                upload_buffer,
                settings.s3_bucket_name,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Generate presigned URL with correct signature version
            url = aws_client.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.s3_bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=3600
            )
        
        logger.info(f"Audio saved to S3: {s3_key}, URL: {url}")
        return url
    
    except Exception as e:
        logger.error(f"Failed to save audio to S3: {e}", exc_info=True)
        raise
