"""Google TTS synthesis engine for languages not supported by AWS Polly."""
import logging
from typing import Iterator, Optional
import io
from gtts import gTTS

logger = logging.getLogger(__name__)


class GTTSSynthesisEngine:
    """Voice synthesis engine using Google TTS for additional Indian languages."""
    
    def __init__(self):
        """Initialize gTTS synthesis engine."""
        self.sample_rate = 24000
        
        # Map language codes to gTTS language codes
        self.language_map = {
            "en": "en",      # English
            "en-US": "en",
            "en-GB": "en",
            "en-IN": "en",
            "hi": "hi",      # Hindi
            "hi-IN": "hi",
            "ta": "ta",      # Tamil
            "ta-IN": "ta",
            "te": "te",      # Telugu
            "te-IN": "te",
            "bn": "bn",      # Bengali
            "bn-IN": "bn",
            "mr": "mr",      # Marathi
            "mr-IN": "mr",
            "kn": "kn",      # Kannada
            "kn-IN": "kn",
            "ml": "ml",      # Malayalam
            "ml-IN": "ml",
            "gu": "gu",      # Gujarati
            "gu-IN": "gu",
            "pa": "pa",      # Punjabi
            "pa-IN": "pa",
            "ur": "ur",      # Urdu
            "ur-IN": "ur",
        }
    
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> bytes:
        """
        Generate audio from text using Google TTS.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID (ignored for gTTS)
            speed: Speech rate multiplier (0.5-2.0)
            pitch: Pitch adjustment (not supported by gTTS)
            language: Language code
        
        Returns:
            Audio waveform as bytes (MP3 format)
        """
        logger.info(f"[GTTS] Synthesizing text with language={language}, speed={speed}, text='{text[:50]}...'")
        
        # Get gTTS language code
        gtts_lang = self.language_map.get(language, "en")
        
        # Clean text - remove excessive punctuation but keep sentence structure
        cleaned_text = text.strip()
        
        # If text is empty after cleaning, raise error
        if not cleaned_text:
            raise ValueError("Text is empty after cleaning")
        
        try:
            # Create gTTS object with explicit language
            tts = gTTS(
                text=cleaned_text,
                lang=gtts_lang,
                slow=(speed < 0.8),  # Use slow mode if speed is very slow
                lang_check=False  # Disable language check to avoid issues
            )
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Read MP3 bytes
            audio_bytes = audio_buffer.read()
            
            logger.info(f"[GTTS] Generated audio: size={len(audio_bytes)} bytes, language={gtts_lang}")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"[GTTS] Synthesis failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to synthesize audio with Google TTS: {str(e)}")
    
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
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID
            speed: Speech rate multiplier
            pitch: Pitch adjustment
            language: Language code
        
        Yields:
            Audio chunks as bytes
        """
        logger.info(f"[GTTS] Starting streaming synthesis")
        
        # Split text into sentences
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            logger.debug(f"[GTTS] Synthesizing sentence {i+1}/{len(sentences)}")
            
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
                logger.error(f"[GTTS] Failed to synthesize sentence {i+1}: {e}")
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
        
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?।])\s+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences


# Global gTTS synthesis engine instance
gtts_synthesis_engine = GTTSSynthesisEngine()
