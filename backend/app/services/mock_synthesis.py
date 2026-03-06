"""Mock synthesis engine for local development without SageMaker."""
import numpy as np
import logging
from typing import Iterator, Optional

logger = logging.getLogger(__name__)


class MockVoiceSynthesisEngine:
    """Mock synthesis engine that generates synthetic audio for testing."""
    
    def __init__(self):
        """Initialize mock synthesis engine."""
        self.sample_rate = 24000
        self.min_sample_rate = 24000
    
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> np.ndarray:
        """
        Generate mock audio from text.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID to use
            speed: Speech rate multiplier (0.5-2.0)
            pitch: Pitch adjustment in semitones (-12 to +12)
            language: Language code (auto-detect if None)
        
        Returns:
            Audio waveform as numpy array
        """
        logger.info(f"[MOCK] Synthesizing text with voice_id={voice_id}, speed={speed}, pitch={pitch}, language={language}")
        
        # Calculate duration based on text length (rough estimate: 150 words per minute)
        words = len(text.split())
        base_duration = (words / 150) * 60  # seconds
        duration = base_duration / speed  # Adjust for speed
        
        # Generate synthetic audio (sine wave with some variation)
        num_samples = int(duration * self.sample_rate)
        
        # Base frequency adjusted by pitch (A4 = 440 Hz)
        base_freq = 440 * (2 ** (pitch / 12))
        
        # Generate time array
        t = np.linspace(0, duration, num_samples, dtype=np.float32)
        
        # Generate audio with multiple harmonics for more natural sound
        audio = np.zeros(num_samples, dtype=np.float32)
        
        # Add fundamental frequency
        audio += 0.3 * np.sin(2 * np.pi * base_freq * t)
        
        # Add harmonics
        audio += 0.2 * np.sin(2 * np.pi * base_freq * 2 * t)
        audio += 0.1 * np.sin(2 * np.pi * base_freq * 3 * t)
        
        # Add some variation to simulate speech
        modulation = 1 + 0.3 * np.sin(2 * np.pi * 3 * t)
        audio *= modulation
        
        # Add envelope (fade in/out)
        fade_samples = int(0.1 * self.sample_rate)  # 100ms fade
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        audio[:fade_samples] *= fade_in
        audio[-fade_samples:] *= fade_out
        
        # Normalize
        audio = audio / np.max(np.abs(audio)) * 0.8
        
        logger.info(f"[MOCK] Generated audio: duration={duration:.2f}s, samples={num_samples}, sample_rate={self.sample_rate}")
        
        return audio
    
    def synthesize_streaming(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> Iterator[np.ndarray]:
        """
        Generate mock audio chunks in real-time.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID to use
            speed: Speech rate multiplier
            pitch: Pitch adjustment in semitones
            language: Language code
        
        Yields:
            Audio chunks as numpy arrays
        """
        logger.info(f"[MOCK] Starting streaming synthesis for voice_id={voice_id}")
        
        # Split text into sentences for streaming
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            logger.debug(f"[MOCK] Synthesizing sentence {i+1}/{len(sentences)}: {sentence[:50]}...")
            
            # Synthesize each sentence
            audio_chunk = self.synthesize(
                text=sentence,
                voice_id=voice_id,
                speed=speed,
                pitch=pitch,
                language=language
            )
            
            yield audio_chunk
    
    def _split_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences for streaming.
        
        Args:
            text: Input text
        
        Returns:
            List of sentences
        """
        import re
        
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences


# Global mock synthesis engine instance
mock_synthesis_engine = MockVoiceSynthesisEngine()
