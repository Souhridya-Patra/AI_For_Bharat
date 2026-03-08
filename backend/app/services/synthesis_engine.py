"""Voice synthesis engine implementation."""
import json
import logging
from typing import Iterator, Optional, Union
from app.services.aws_client import aws_client
from app.config import settings

logger = logging.getLogger(__name__)


class VoiceSynthesisEngine:
    """Voice synthesis engine using AWS Polly for supported languages and gTTS for others."""
    
    def __init__(self):
        """Initialize synthesis engine."""
        self.endpoint_name = settings.sagemaker_endpoint_name
        self.min_sample_rate = 24000
        self.use_mock = settings.use_mock_synthesis
        self.use_polly = settings.use_aws_polly
        self.use_xtts = settings.use_xtts
        
        # Languages supported by AWS Polly
        self.polly_languages = {"en", "en-us", "en-gb", "en-in", "hi", "hi-in", "auto"}
        self.language_aliases = {
            "english": "en",
            "hindi": "hi",
            "tamil": "ta",
            "telugu": "te",
            "bengali": "bn",
            "marathi": "mr",
            "kannada": "kn",
            "malayalam": "ml",
            "gujarati": "gu",
            "punjabi": "pa",
            "urdu": "ur",
        }
        
        # Languages supported by Google TTS
        self.gtts_languages = {
            "en", "en-us", "en-gb", "en-in",
            "hi", "hi-in",
            "ta", "ta-in",
            "te", "te-in",
            "bn", "bn-in",
            "mr", "mr-in",
            "kn", "kn-in",
            "ml", "ml-in",
            "gu", "gu-in",
            "pa", "pa-in",
            "ur", "ur-in",
            "auto",
        }
        
        # Initialize XTTS-v2 (ultra-realistic synthesis)
        self.xtts_engine = None
        if self.use_xtts:
            try:
                from app.services.xtts_synthesis import get_xtts_engine
                self.xtts_engine = get_xtts_engine()
                logger.info("✨ XTTS-v2 enabled for ultra-realistic voice synthesis (ElevenLabs-quality)")
            except Exception as e:
                logger.warning(f"XTTS-v2 initialization failed: {e}. Falling back to Polly/gTTS")
                self.use_xtts = False
        
        # Determine which engines to use
        if self.use_polly:
            logger.info("Using AWS Polly Neural for Hindi and English (high quality)")
            from app.services.polly_synthesis import polly_synthesis_engine
            self.polly_engine = polly_synthesis_engine
        
        # Always initialize gTTS for additional languages
        try:
            from app.services.gtts_synthesis import gtts_synthesis_engine
            self.gtts_engine = gtts_synthesis_engine
            logger.info("Using Google TTS for Tamil, Telugu, Bengali, Marathi, and other Indian languages")
        except ImportError:
            logger.warning("gTTS not available - install with: pip install gTTS")
            self.gtts_engine = None
        
        if self.use_mock:
            logger.warning("Using MOCK synthesis engine - set use_mock_synthesis=False in .env for production")
            from app.services.mock_synthesis import mock_synthesis_engine
            self.mock_engine = mock_synthesis_engine

    def _normalize_language(self, language: Optional[str]) -> str:
        """Normalize incoming language code/name to canonical lowercase form."""
        if not language:
            return "auto"

        normalized = language.strip().lower().replace("_", "-")
        normalized = self.language_aliases.get(normalized, normalized)

        # Normalize region/script forms like hi-IN -> hi-in
        parts = normalized.split("-")
        if len(parts) > 1:
            normalized = f"{parts[0]}-{parts[1]}"

        return normalized

    def _select_engine(self, normalized_language: str) -> str:
        """Select synthesis engine based on normalized language and priority."""
        if self.use_mock:
            return "mock"

        # XTTS has highest priority for all languages (when enabled)
        # It provides the most natural, human-like synthesis
        if self.use_xtts and self.xtts_engine:
            logger.info(f"[ENGINE] Selected XTTS-v2 for {normalized_language} (ultra-realistic synthesis)")
            return "xtts"

        # Polly for Hindi/English (neural voices, very good quality)
        if self.use_polly and normalized_language in self.polly_languages:
            return "polly"

        # gTTS for other Indian languages (basic but functional)
        if self.gtts_engine and (
            normalized_language in self.gtts_languages
            or normalized_language.split("-")[0] in self.gtts_languages
        ):
            return "gtts"

        # SageMaker fallback (if not using Polly)
        if not self.use_polly:
            return "sagemaker"

        return "unsupported"
    
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> Union[bytes, 'np.ndarray']:
        """
        Generate audio from text.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID to use
            speed: Speech rate multiplier (0.5-2.0)
            pitch: Pitch adjustment in semitones (-12 to +12)
            language: Language code (auto-detect if None)
        
        Returns:
            Audio waveform as bytes or numpy array
        """
        normalized_language = self._normalize_language(language)
        
        # PRIORITY: If voice_id is a cloned voice (starts with "voice_"), use XTTS
        if voice_id and voice_id.startswith("voice_"):
            if self.use_xtts and self.xtts_engine:
                logger.info(f"✨ Using XTTS-v2 for CLONED voice: {voice_id}")
                return self.xtts_engine.synthesize(text, voice_id, speed, pitch, normalized_language)
            else:
                logger.warning(f"⚠️ Cloned voice requested but XTTS not enabled. Install XTTS or enable in .env")
                logger.warning("Falling back to default Polly/gTTS voice")
        
        engine = self._select_engine(normalized_language)

        if engine == "mock":
            return self.mock_engine.synthesize(text, voice_id, speed, pitch, normalized_language)

        if engine == "xtts":
            logger.info(f"✨ Using XTTS-v2 for language: {normalized_language} (ultra-realistic)")
            result = self.xtts_engine.synthesize(text, voice_id, speed, pitch, normalized_language)
            logger.info(f"XTTS returned {len(result) if isinstance(result, bytes) else 'unknown'} bytes")
            return result

        if engine == "polly":
            logger.info(f"Using AWS Polly Neural for language: {normalized_language}")
            return self.polly_engine.synthesize(text, voice_id, speed, pitch, normalized_language)

        if engine == "gtts":
            logger.info(f"Using Google TTS for language: {normalized_language}")
            result = self.gtts_engine.synthesize(text, voice_id, speed, pitch, normalized_language)
            logger.info(f"gTTS returned {len(result) if isinstance(result, bytes) else 'unknown'} bytes")
            return result

        if engine == "sagemaker":
            return self._synthesize_sagemaker(text, voice_id, speed, pitch, normalized_language)

        raise ValueError(
            f"Unsupported language: {language}. "
            f"Supported Polly: {sorted(self.polly_languages)} | "
            f"Supported gTTS: {sorted(self.gtts_languages)}"
        )
    
    def _synthesize_sagemaker(
        self,
        text: str,
        voice_id: str,
        speed: float,
        pitch: int,
        language: Optional[str]
    ):
        """Synthesize using SageMaker endpoint."""
        logger.info(f"Synthesizing text with voice_id={voice_id}, speed={speed}, pitch={pitch}")
        
        # Import numpy only when needed for SageMaker
        import numpy as np
        
        # Prepare request payload for SageMaker endpoint
        payload = {
            "text": text,
            "voice_id": voice_id,
            "speed": speed,
            "pitch": pitch,
            "language": language or "auto"
        }
        
        try:
            # Invoke SageMaker endpoint
            response = aws_client.sagemaker_runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse response
            result = json.loads(response['Body'].read().decode())
            
            # Extract audio data
            audio_array = np.array(result['audio'], dtype=np.float32)
            sample_rate = result.get('sample_rate', self.min_sample_rate)
            
            # Validate sample rate
            if sample_rate < self.min_sample_rate:
                logger.warning(f"Sample rate {sample_rate} is below minimum {self.min_sample_rate}")
            
            logger.info(f"Successfully synthesized audio: duration={len(audio_array)/sample_rate:.2f}s, sample_rate={sample_rate}")
            
            return audio_array
            
        except Exception as e:
            logger.error(f"Synthesis failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to synthesize audio: {str(e)}")
    
    def synthesize_streaming(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> Iterator[Union[bytes, 'np.ndarray']]:
        """
        Generate audio chunks in real-time.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID to use
            speed: Speech rate multiplier
            pitch: Pitch adjustment in semitones
            language: Language code
        
        Yields:
            Audio chunks as bytes (Polly) or numpy arrays (SageMaker/Mock)
        """
        normalized_language = self._normalize_language(language)
        engine = self._select_engine(normalized_language)

        if engine == "xtts":
            yield from self.xtts_engine.synthesize_streaming(text, voice_id, speed, pitch, normalized_language)
            return

        if engine == "polly":
            yield from self.polly_engine.synthesize_streaming(text, voice_id, speed, pitch, normalized_language)
            return

        if engine == "gtts":
            yield from self.gtts_engine.synthesize_streaming(text, voice_id, speed, pitch, normalized_language)
            return

        if engine == "mock":
            yield from self.mock_engine.synthesize_streaming(text, voice_id, speed, pitch, normalized_language)
            return

        if engine == "unsupported":
            raise ValueError(f"Unsupported language for streaming: {language}")

        # Use SageMaker endpoint
        logger.info(f"Starting streaming synthesis for voice_id={voice_id}")
        
        # Split text into sentences for streaming
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            logger.debug(f"Synthesizing sentence {i+1}/{len(sentences)}: {sentence[:50]}...")
            
            try:
                # Synthesize each sentence
                audio_chunk = self.synthesize(
                    text=sentence,
                    voice_id=voice_id,
                    speed=speed,
                    pitch=pitch,
                    language=normalized_language
                )
                
                yield audio_chunk
                
            except Exception as e:
                logger.error(f"Failed to synthesize sentence {i+1}: {e}")
                # Continue with next sentence instead of failing completely
                continue
    
    def _split_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences for streaming.
        
        Args:
            text: Input text
        
        Returns:
            List of sentences
        """
        import re
        
        # Simple sentence splitting (can be improved with NLP libraries)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text before synthesis.
        
        Args:
            text: Raw input text
        
        Returns:
            Preprocessed text
        """
        # TODO: Implement text preprocessing
        # - Expand numbers (123 -> one hundred twenty-three)
        # - Expand abbreviations (Dr. -> doctor)
        # - Normalize punctuation
        
        return text


# Global synthesis engine instance
synthesis_engine = VoiceSynthesisEngine()
