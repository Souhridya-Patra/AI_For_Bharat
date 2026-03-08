"""XTTS-v2 synthesis engine for ultra-realistic voice cloning and synthesis.

This module provides access to Coqui XTTS-v2, which offers:
- Professional-grade voice synthesis (rivals ElevenLabs quality)
- Voice cloning from 6 seconds of audio
- Support for 16+ languages including all major Indian languages
- Natural prosody, emotion, and breathing patterns
"""
import logging
import io
import json
import numpy as np
from typing import Iterator, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class XTTSSynthesisEngine:
    """Voice synthesis engine using XTTS-v2 for ultra-realistic output."""
    
    def __init__(self, use_sagemaker: bool = False, endpoint_name: Optional[str] = None):
        """
        Initialize XTTS synthesis engine.
        
        Args:
            use_sagemaker: If True, use SageMaker endpoint; if False, use local model
            endpoint_name: SageMaker endpoint name (required if use_sagemaker=True)
        """
        self.use_sagemaker = use_sagemaker
        self.endpoint_name = endpoint_name
        self.sample_rate = 24000
        self.model = None
        
        # Supported languages by XTTS-v2
        self.supported_languages = {
            "en", "en-us", "en-gb", "en-in",
            "hi", "hi-in",
            "es", "fr", "de", "it", "pt", "pl",
            "tr", "ru", "nl", "cs", "ar",
            "zh-cn", "ja", "ko",
            # Add more as XTTS adds support
        }
        
        if not use_sagemaker:
            self._initialize_local_model()
        else:
            if not endpoint_name:
                raise ValueError("endpoint_name is required when use_sagemaker=True")
            logger.info(f"[XTTS] Using SageMaker endpoint: {endpoint_name}")
    
    def _initialize_local_model(self):
        """Initialize local XTTS model (lazy loading)."""
        try:
            from TTS.api import TTS
            logger.info("[XTTS] Initializing local XTTS-v2 model...")
            
            # Initialize XTTS-v2 model
            # This will download ~1.8GB on first run
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            
            logger.info("[XTTS] Local XTTS-v2 model initialized successfully")
        except ImportError:
            logger.error("[XTTS] TTS library not installed. Run: pip install TTS")
            raise RuntimeError(
                "XTTS-v2 requires TTS library. Install with: pip install TTS==0.22.0"
            )
        except Exception as e:
            logger.error(f"[XTTS] Failed to initialize model: {e}")
            raise
    
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> bytes:
        """
        Generate ultra-realistic audio from text using XTTS-v2.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID or path to reference audio for cloning
            speed: Speech rate multiplier (0.5-2.0) - XTTS handles this naturally
            pitch: Pitch adjustment (not directly supported by XTTS)
            language: Language code
        
        Returns:
            Audio waveform as bytes (WAV format)
        """
        logger.info(f"[XTTS] Synthesizing text with language={language}, speed={speed}")
        
        # Normalize language code
        lang = self._normalize_language(language)
        
        if self.use_sagemaker:
            return self._synthesize_sagemaker(text, voice_id, speed, lang)
        else:
            return self._synthesize_local(text, voice_id, speed, lang)
    
    def _synthesize_local(
        self,
        text: str,
        voice_id: str,
        speed: float,
        language: str
    ) -> bytes:
        """Synthesize using local XTTS model."""
        if self.model is None:
            self._initialize_local_model()
        
        try:
            # For XTTS, voice_id can be:
            # 1. "voice_XXXXX" - fetch cloned voice from DynamoDB/S3
            # 2. Path to a reference audio file for cloning
            # 3. "default" to use built-in speaker
            
            reference_audio_path = None
            
            # Check if this is a cloned voice ID
            if voice_id and voice_id.startswith("voice_"):
                logger.info(f"[XTTS] Loading cloned voice: {voice_id}")
                reference_audio_path = self._get_cloned_voice_audio(voice_id)
            elif voice_id != "default" and voice_id and Path(voice_id).exists():
                # Direct file path provided
                reference_audio_path = voice_id
            
            # Generate audio
            output_path = "/tmp/xtts_output.wav"
            
            if reference_audio_path:
                # Use voice cloning with reference audio
                logger.info(f"[XTTS] Cloning voice from: {reference_audio_path}")
                self.model.tts_to_file(
                    text=text,
                    language=language,
                    speaker_wav=reference_audio_path,  # Reference audio for cloning
                    file_path=output_path
                )
            else:
                # Use built-in XTTS speaker
                logger.info("[XTTS] Using default built-in voice")
                self.model.tts_to_file(
                    text=text,
                    language=language,
                    file_path=output_path
                )
            
            # Read generated audio
            with open(output_path, 'rb') as f:
                audio_bytes = f.read()
            
            # Handle speed adjustment if needed (post-processing)
            if speed != 1.0:
                audio_bytes = self._adjust_speed(audio_bytes, speed)
            
            logger.info(f"[XTTS] Generated audio: size={len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"[XTTS] Local synthesis failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to synthesize with XTTS: {str(e)}")
    
    def _synthesize_sagemaker(
        self,
        text: str,
        voice_id: str,
        speed: float,
        language: str
    ) -> bytes:
        """Synthesize using SageMaker endpoint."""
        from app.services.aws_client import aws_client
        
        try:
            # Prepare request payload for SageMaker
            payload = {
                "text": text,
                "voice_id": voice_id,
                "speed": speed,
                "language": language,
                "model": "xtts_v2"
            }
            
            # Invoke SageMaker endpoint
            response = aws_client.sagemaker_runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            # Extract audio data
            if 'audio' in result:
                # Audio is base64 encoded
                import base64
                audio_bytes = base64.b64decode(result['audio'])
            elif 'audio_array' in result:
                # Audio is numpy array
                audio_array = np.array(result['audio_array'], dtype=np.float32)
                # Convert to WAV bytes
                audio_bytes = self._numpy_to_wav(audio_array)
            else:
                raise ValueError("Invalid response from SageMaker endpoint")
            
            logger.info(f"[XTTS] SageMaker synthesis successful: size={len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"[XTTS] SageMaker synthesis failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to synthesize with XTTS on SageMaker: {str(e)}")
    
    def synthesize_streaming(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> Iterator[bytes]:
        """
        Generate audio chunks in real-time.
        
        Note: XTTS doesn't support true streaming yet, so we split by sentences.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID
            speed: Speech rate multiplier
            pitch: Pitch adjustment
            language: Language code
        
        Yields:
            Audio chunks as bytes
        """
        logger.info(f"[XTTS] Starting streaming synthesis")
        
        # Split text into sentences
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            logger.debug(f"[XTTS] Synthesizing sentence {i+1}/{len(sentences)}")
            
            try:
                # Synthesize each sentence
                audio_chunk = self.synthesize(
                    text=sentence,
                    voice_id=voice_id,
                    speed=speed,
                    pitch=pitch,
                    language=language
                )
                
                yield audio_chunk
                
            except Exception as e:
                logger.error(f"[XTTS] Failed to synthesize sentence {i+1}: {e}")
                continue
    
    def _normalize_language(self, language: Optional[str]) -> str:
        """Normalize language code for XTTS."""
        if not language:
            return "en"
        
        lang = language.lower().replace("_", "-")
        
        # Map common variants
        lang_map = {
            "en-in": "en",  # XTTS doesn't have Indian English, use standard
            "hi-in": "hi",
            "ta": "en",     # Tamil not in XTTS, fallback to English
            "ta-in": "en",
            "te": "en",     # Telugu not in XTTS, fallback to English
            "te-in": "en",
            "bn": "en",     # Bengali not in XTTS, fallback to English
            "bn-in": "en",
            "mr": "en",     # Marathi not in XTTS, fallback to English
            "mr-in": "en",
        }
        
        return lang_map.get(lang, lang.split("-")[0])
    
    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences for streaming."""
        import re
        
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?।])\s+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _adjust_speed(self, audio_bytes: bytes, speed: float) -> bytes:
        """Adjust audio speed using pydub."""
        try:
            from pydub import AudioSegment
            from pydub.effects import speedup
            
            # Load audio
            audio = AudioSegment.from_wav(io.BytesIO(audio_bytes))
            
            # Adjust speed
            if speed > 1.0:
                # Speed up
                audio = speedup(audio, playback_speed=speed)
            elif speed < 1.0:
                # Slow down
                audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * speed)
                })
                audio = audio.set_frame_rate(self.sample_rate)
            
            # Export to bytes
            buffer = io.BytesIO()
            audio.export(buffer, format='wav')
            buffer.seek(0)
            
            return buffer.read()
            
        except ImportError:
            logger.warning("[XTTS] pydub not available, speed adjustment skipped")
            return audio_bytes
        except Exception as e:
            logger.warning(f"[XTTS] Speed adjustment failed: {e}")
            return audio_bytes
    
    def _get_cloned_voice_audio(self, voice_id: str) -> str:
        """
        Retrieve cloned voice reference audio from DynamoDB/S3.
        
        Args:
            voice_id: Voice model ID (e.g., "voice_abc123def456")
        
        Returns:
            Path to downloaded reference audio file
        """
        from app.services.aws_client import aws_client
        from app.config import settings
        import tempfile
        import os
        
        try:
            # Get voice metadata from DynamoDB
            table = aws_client.dynamodb.Table(settings.dynamodb_voices_table)
            response = table.get_item(Key={'id': voice_id})
            
            if 'Item' not in response:
                raise ValueError(f"Cloned voice not found: {voice_id}")
            
            item = response['Item']
            audio_url = item.get('reference_audio_url')
            
            if not audio_url:
                raise ValueError(f"No reference audio found for voice: {voice_id}")
            
            # Parse S3 URL: s3://bucket/key
            if audio_url.startswith('s3://'):
                parts = audio_url[5:].split('/', 1)
                bucket = parts[0]
                key = parts[1]
            else:
                raise ValueError(f"Invalid S3 URL: {audio_url}")
            
            # Download from S3 to temp file
            temp_dir = tempfile.gettempdir()
            local_path = os.path.join(temp_dir, f"{voice_id}_reference.wav")
            
            logger.info(f"[XTTS] Downloading cloned voice from S3: {audio_url}")
            aws_client.s3.download_file(bucket, key, local_path)
            logger.info(f"[XTTS] Downloaded to: {local_path}")
            
            return local_path
            
        except Exception as e:
            logger.error(f"[XTTS] Failed to retrieve cloned voice audio: {e}")
            raise RuntimeError(f"Failed to load cloned voice '{voice_id}': {str(e)}")
    
    def _numpy_to_wav(self, audio_array: np.ndarray) -> bytes:
        """Convert numpy array to WAV bytes."""
        import wave
        
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            
            # Convert float32 to int16
            audio_int16 = (audio_array * 32767).astype(np.int16)
            wav_file.writeframes(audio_int16.tobytes())
        
        buffer.seek(0)
        return buffer.read()


# Global XTTS synthesis engine instance (lazy initialization)
# By default, use local model. Set USE_XTTS_SAGEMAKER=True in .env to use SageMaker
_xtts_engine = None

def get_xtts_engine():
    """Get or create XTTS engine instance."""
    global _xtts_engine
    
    if _xtts_engine is None:
        from app.config import settings
        
        # Check if SageMaker should be used
        use_sagemaker = getattr(settings, 'use_xtts_sagemaker', False)
        endpoint = getattr(settings, 'sagemaker_endpoint_name', None)
        
        _xtts_engine = XTTSSynthesisEngine(
            use_sagemaker=use_sagemaker,
            endpoint_name=endpoint if use_sagemaker else None
        )
    
    return _xtts_engine


# Convenience reference
xtts_synthesis_engine = None  # Will be initialized on first use via get_xtts_engine()
