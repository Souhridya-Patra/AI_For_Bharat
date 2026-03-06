"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class AudioFormat(str, Enum):
    """Supported audio formats."""
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"


class SynthesisRequest(BaseModel):
    """Request model for text-to-speech synthesis."""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to synthesize")
    voice_id: str = Field(..., description="Voice model ID to use")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Speech rate multiplier")
    pitch: int = Field(0, ge=-12, le=12, description="Pitch adjustment in semitones")
    stream: bool = Field(False, description="Enable streaming mode")
    post_process: bool = Field(True, description="Apply audio post-processing")
    language: Optional[str] = Field(None, description="Language code (auto-detect if not provided)")


class SynthesisResponse(BaseModel):
    """Response model for synthesis."""
    audio_url: str = Field(..., description="URL to download generated audio")
    duration: float = Field(..., description="Audio duration in seconds")
    sample_rate: int = Field(..., description="Audio sample rate in Hz")
    request_id: str = Field(..., description="Unique request identifier")


class VoiceCloneRequest(BaseModel):
    """Request model for voice cloning."""
    voice_name: str = Field(..., min_length=1, max_length=100, description="Name for the cloned voice")
    
    @validator('voice_name')
    def validate_voice_name(cls, v):
        """Validate voice name contains only allowed characters."""
        if not v.replace(' ', '').replace('-', '').replace('_', '').isalnum():
            raise ValueError('Voice name must contain only alphanumeric characters, spaces, hyphens, and underscores')
        return v


class VoiceCloneResponse(BaseModel):
    """Response model for voice cloning."""
    voice_id: str = Field(..., description="Unique voice model ID")
    status: str = Field(..., description="Cloning status")
    message: str = Field(..., description="Status message")


class VoiceModel(BaseModel):
    """Voice model metadata."""
    id: str = Field(..., description="Unique voice model ID")
    name: str = Field(..., description="Voice model name")
    user_id: str = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    reference_audio_duration: float = Field(..., description="Duration of reference audio in seconds")
    is_shared: bool = Field(False, description="Whether voice is shared with collaborators")
    shared_with: List[str] = Field(default_factory=list, description="User IDs with access")


class VoiceListResponse(BaseModel):
    """Response model for listing voices."""
    voices: List[VoiceModel]
    total: int


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: dict = Field(..., description="Error details")
    
    class Config:
        schema_extra = {
            "example": {
                "error": {
                    "code": "INVALID_AUDIO_DURATION",
                    "message": "Audio sample must be between 6 and 10 seconds",
                    "details": {
                        "provided_duration": 4.2,
                        "min_duration": 6.0,
                        "max_duration": 10.0
                    },
                    "request_id": "req_abc123"
                }
            }
        }


class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")


class AudioClip(BaseModel):
    """Audio clip within a project."""
    id: str
    text: str
    voice_id: str
    speed: float = 1.0
    pitch: int = 0
    audio_url: str
    start_time: float
    duration: float


class Project(BaseModel):
    """Project model."""
    id: str
    user_id: str
    name: str
    audio_clips: List[AudioClip] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
