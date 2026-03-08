"""Voice cloning module implementation."""
import uuid
import numpy as np
import librosa
import soundfile as sf
import logging
from typing import Tuple
from datetime import datetime
from app.services.aws_client import aws_client
from app.config import settings

logger = logging.getLogger(__name__)


class InvalidAudioDurationError(Exception):
    """Raised when audio duration is invalid."""
    def __init__(self, duration: float, min_duration: float = 6.0, max_duration: float = 10.0):
        self.duration = duration
        self.min_duration = min_duration
        self.max_duration = max_duration
        super().__init__(
            f"Audio sample must be between {min_duration} and {max_duration} seconds. "
            f"Provided: {duration:.2f} seconds"
        )


class MultipleSpeakersError(Exception):
    """Raised when multiple speakers are detected."""
    pass


class VoiceCloningModule:
    """Voice cloning module using speaker encoder."""
    
    def __init__(self):
        """Initialize voice cloning module."""
        self.min_duration = 6.0
        self.max_duration = 10.0
        self.embedding_dim = 256
    
    def clone_voice(
        self,
        audio_bytes: bytes,
        voice_name: str,
        user_id: str
    ) -> str:
        """
        Create voice model from audio sample.
        
        Args:
            audio_bytes: Audio file bytes
            voice_name: Name for the voice model
            user_id: User ID who owns the voice
        
        Returns:
            Voice model ID
        
        Raises:
            InvalidAudioDurationError: If audio duration is invalid
            MultipleSpeakersError: If multiple speakers detected
        """
        logger.info(f"Cloning voice: name={voice_name}, user_id={user_id}")
        
        # Load audio
        audio_array, sample_rate = self._load_audio(audio_bytes)
        
        # Validate duration
        duration = len(audio_array) / sample_rate
        if duration < self.min_duration or duration > self.max_duration:
            raise InvalidAudioDurationError(duration, self.min_duration, self.max_duration)
        
        # Detect multiple speakers
        num_speakers = self._detect_speakers(audio_array, sample_rate)
        if num_speakers > 1:
            raise MultipleSpeakersError(
                f"Multiple speakers detected ({num_speakers}). "
                "Please provide audio with a single speaker."
            )
        
        # Extract voice embedding
        embedding = self._extract_embedding(audio_array, sample_rate)
        
        # Generate voice ID
        voice_id = f"voice_{uuid.uuid4().hex[:16]}"
        
        # Save reference audio to S3
        audio_url = self._save_reference_audio(audio_bytes, voice_id)
        
        # Store voice model in DynamoDB
        self._store_voice_model(
            voice_id=voice_id,
            user_id=user_id,
            voice_name=voice_name,
            embedding=embedding,
            audio_url=audio_url,
            duration=duration
        )
        
        logger.info(f"Voice cloned successfully: voice_id={voice_id}")
        return voice_id
    
    def get_voice_embedding(self, voice_id: str) -> np.ndarray:
        """
        Retrieve stored voice embedding.
        
        Args:
            voice_id: Voice model ID
        
        Returns:
            Voice embedding as numpy array
        """
        table = aws_client.dynamodb.Table(settings.dynamodb_voices_table)
        
        try:
            response = table.get_item(Key={'id': voice_id})
            
            if 'Item' not in response:
                raise ValueError(f"Voice model not found: {voice_id}")
            
            # Convert embedding from list to numpy array
            embedding = np.array(response['Item']['embedding'], dtype=np.float32)
            
            return embedding
        
        except Exception as e:
            logger.error(f"Failed to retrieve voice embedding: {e}")
            raise
    
    def _load_audio(self, audio_bytes: bytes) -> Tuple[np.ndarray, int]:
        """Load audio from bytes."""
        import io
        
        try:
            audio_array, sample_rate = sf.read(io.BytesIO(audio_bytes))
            
            # Convert to mono if stereo
            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)
            
            return audio_array, sample_rate
        
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            raise ValueError(f"Invalid audio file: {str(e)}")
    
    def _detect_speakers(self, audio: np.ndarray, sample_rate: int) -> int:
        """
        Detect number of speakers in audio.
        
        Args:
            audio: Audio waveform
            sample_rate: Sample rate
        
        Returns:
            Number of speakers detected
        """
        # TODO: Implement proper speaker diarization
        # For now, assume single speaker
        # In production, use pyannote.audio or similar
        
        return 1
    
    def _extract_embedding(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Extract voice embedding from audio.
        
        Args:
            audio: Audio waveform
            sample_rate: Sample rate
        
        Returns:
            Voice embedding
        """
        # TODO: Implement proper speaker encoder
        # For now, generate random embedding for testing
        # In production, use Resemblyzer, ECAPA-TDNN, or similar
        
        logger.warning("Using random embedding - implement proper speaker encoder")
        embedding = np.random.randn(self.embedding_dim).astype(np.float32)
        
        # Normalize embedding
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def _save_reference_audio(self, audio_bytes: bytes, voice_id: str) -> str:
        """Save reference audio to S3."""
        import io
        
        try:
            s3_key = f"voices/{voice_id}/reference.wav"
            
            aws_client.s3.upload_fileobj(
                io.BytesIO(audio_bytes),
                settings.s3_models_bucket,
                s3_key,
                ExtraArgs={'ContentType': 'audio/wav'}
            )
            
            # Generate URL
            url = f"s3://{settings.s3_models_bucket}/{s3_key}"
            
            logger.info(f"Reference audio saved: {s3_key}")
            return url
        
        except Exception as e:
            logger.error(f"Failed to save reference audio: {e}")
            raise
    
    def _store_voice_model(
        self,
        voice_id: str,
        user_id: str,
        voice_name: str,
        embedding: np.ndarray,
        audio_url: str,
        duration: float
    ):
        """Store voice model metadata in DynamoDB."""
        table = aws_client.dynamodb.Table(settings.dynamodb_voices_table)
        
        try:
            # Convert numpy float32 to Python float for DynamoDB compatibility
            embedding_list = [float(x) for x in embedding]
            
            item = {
                'id': voice_id,
                'user_id': user_id,
                'name': voice_name,
                'embedding': embedding_list,  # List of Python floats
                'reference_audio_url': audio_url,
                'reference_audio_duration': duration,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'is_shared': False,
                'shared_with': []
            }
            
            table.put_item(Item=item)
            
            logger.info(f"Voice model stored in DynamoDB: {voice_id}")
        
        except Exception as e:
            logger.error(f"Failed to store voice model: {e}")
            raise


# Global cloning module instance
cloning_module = VoiceCloningModule()
