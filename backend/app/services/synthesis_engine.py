"""Voice synthesis engine implementation."""
import json
import logging
from typing import Iterator, Optional, Union
from app.services.aws_client import aws_client
from app.config import settings

logger = logging.getLogger(__name__)


class VoiceSynthesisEngine:
    """Voice synthesis engine using XTTS-v2 on SageMaker, AWS Polly, or mock for development."""
    
    def __init__(self):
        """Initialize synthesis engine."""
        self.endpoint_name = settings.sagemaker_endpoint_name
        self.min_sample_rate = 24000
        self.use_mock = settings.use_mock_synthesis
        self.use_polly = settings.use_aws_polly
        
        # Determine which engine to use
        if self.use_polly:
            logger.info("Using AWS Polly for real voice synthesis")
            from app.services.polly_synthesis import polly_synthesis_engine
            self.polly_engine = polly_synthesis_engine
        elif self.use_mock:
            logger.warning("Using MOCK synthesis engine - set use_mock_synthesis=False in .env for production")
            from app.services.mock_synthesis import mock_synthesis_engine
            self.mock_engine = mock_synthesis_engine
        else:
            logger.info("Using SageMaker endpoint for synthesis")
    
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
            Audio waveform as bytes (Polly) or numpy array (SageMaker/Mock)
        """
        # Use AWS Polly if enabled
        if self.use_polly:
            return self.polly_engine.synthesize(text, voice_id, speed, pitch, language)
        
        # Use mock if enabled
        if self.use_mock:
            return self.mock_engine.synthesize(text, voice_id, speed, pitch, language)
        
        # Use SageMaker endpoint
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
        # Use AWS Polly if enabled
        if self.use_polly:
            yield from self.polly_engine.synthesize_streaming(text, voice_id, speed, pitch, language)
            return
        
        # Use mock if enabled
        if self.use_mock:
            yield from self.mock_engine.synthesize_streaming(text, voice_id, speed, pitch, language)
            return
        
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
                    language=language
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
