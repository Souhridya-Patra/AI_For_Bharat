"""AWS Polly synthesis engine for real voice synthesis."""
import logging
from typing import Iterator, Optional
import io
import array
from app.services.aws_client import aws_client

logger = logging.getLogger(__name__)


class PollySynthesisEngine:
    """Voice synthesis engine using AWS Polly."""
    
    def __init__(self):
        """Initialize Polly synthesis engine."""
        self.sample_rate_neural = 24000    # Neural engine supports 24000 Hz
        self.sample_rate_standard = 16000  # Standard engine supports 8000 or 16000 Hz
        self.sample_rate = self.sample_rate_standard  # Default to standard
        
        # Map language codes to Polly voices
        # Note: AWS Polly has limited Indian language support
        # Using NEURAL voices for maximum human-like quality
        self.voice_map = {
            "en": "Matthew",     # English (US) - Male Neural (most natural)
            "en-us": "Matthew",
            "en-gb": "Amy",      # English (UK) - Female Neural (very expressive)
            "en-in": "Kajal",    # English (Indian) - Female Neural - BEST FOR INDIAN ACCENT
            "hi": "Kajal",       # Hindi - Female Neural - MOST HUMAN-LIKE
            "hi-in": "Kajal",
            "ta": None,          # Tamil - NOT SUPPORTED by Polly
            "ta-in": None,
            "te": None,          # Telugu - NOT SUPPORTED by Polly
            "te-in": None,
            "bn": None,          # Bengali - NOT SUPPORTED by Polly
            "bn-in": None,
            "mr": None,          # Marathi - NOT SUPPORTED by Polly
            "mr-in": None,
            "auto": "Kajal",     # Default to Indian English Neural
        }
        
        # Neural-compatible voices (these support the neural engine for best quality)
        self.neural_voices = {"Matthew", "Joanna", "Amy", "Kajal", "Aria", "Ruth", "Stephen"}
        
        # Supported languages (for validation)
        self.supported_languages = {"en", "en-US", "en-GB", "en-IN", "hi", "hi-IN", "auto"}
    
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: int = 0,
        language: Optional[str] = None
    ) -> bytes:
        """
        Generate audio from text using AWS Polly.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID (ignored for Polly, uses language)
            speed: Speech rate multiplier (0.5-2.0)
            pitch: Pitch adjustment (not supported by Polly)
            language: Language code
        
        Returns:
            Audio waveform as bytes (PCM format)
        """
        logger.info(f"[POLLY] Synthesizing text with language={language}, speed={speed}")
        
        # Check if language is supported
        if language and language not in self.supported_languages:
            error_msg = (
                f"Language '{language}' is not supported by AWS Polly. "
                f"Supported languages: Hindi (hi), English (en, en-IN). "
                f"Tamil, Telugu, Bengali, and Marathi are not available in AWS Polly."
            )
            logger.error(f"[POLLY] {error_msg}")
            raise ValueError(error_msg)
        
        # Get Polly voice for language
        polly_voice = self.voice_map.get(language or "auto", "Aditi")
        
        if polly_voice is None:
            raise ValueError(f"No voice available for language: {language}")
        
        # Convert speed to Polly format (percentage)
        # Polly supports 20% to 200%
        speed_percent = int(speed * 100)
        speed_percent = max(20, min(200, speed_percent))
        
        # Check if voice supports neural engine
        use_neural = polly_voice in self.neural_voices
        
        # Build SSML for natural speech with prosody controls
        if speed != 1.0 or use_neural:
            # Enhanced SSML with breathing pauses and natural intonation
            ssml_text = f'<speak><prosody rate="{speed_percent}%"><amazon:auto-breaths>{text}</amazon:auto-breaths></prosody></speak>'
            text_type = 'ssml'
        else:
            ssml_text = text
            text_type = 'text'
        
        try:
            # Call AWS Polly
            polly = aws_client.session.client('polly')
            
            # Use neural engine for compatible voices, standard for others
            if use_neural:
                try:
                    response = polly.synthesize_speech(
                        Text=ssml_text,
                        TextType=text_type,
                        OutputFormat='pcm',
                        VoiceId=polly_voice,
                        Engine='neural'  # Neural engine for maximum naturalness
                    )
                    actual_sample_rate = self.sample_rate_neural
                    logger.info(f"[POLLY] Using NEURAL engine with {polly_voice} for human-like quality")
                except Exception as neural_error:
                    if 'does not support' in str(neural_error) or 'InvalidSampleRate' in str(neural_error):
                        logger.warning(f"[POLLY] Neural engine not available for {polly_voice}, falling back to standard")
                        response = polly.synthesize_speech(
                            Text=ssml_text,
                            TextType=text_type,
                            OutputFormat='pcm',
                            VoiceId=polly_voice,
                            SampleRate=str(self.sample_rate_standard)
                        )
                        actual_sample_rate = self.sample_rate_standard
                    else:
                        raise
            else:
                # Standard engine for non-neural voices
                response = polly.synthesize_speech(
                    Text=ssml_text,
                    TextType=text_type,
                    OutputFormat='pcm',
                    VoiceId=polly_voice,
                    SampleRate=str(self.sample_rate_standard)
                )
                actual_sample_rate = self.sample_rate_standard
            
            # Read audio stream
            audio_bytes = response['AudioStream'].read()
            
            duration = len(audio_bytes) / (actual_sample_rate * 2)  # 2 bytes per sample (16-bit)
            logger.info(f"[POLLY] Generated audio: duration={duration:.2f}s, sample_rate={actual_sample_rate}, quality={'NEURAL' if use_neural else 'STANDARD'}")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"[POLLY] Synthesis failed: {e}", exc_info=True)
            raise RuntimeError(f"Failed to synthesize audio with Polly: {str(e)}")
    
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
        
        Note: Polly doesn't support true streaming, so we split by sentences.
        
        Args:
            text: Input text to synthesize
            voice_id: Voice model ID
            speed: Speech rate multiplier
            pitch: Pitch adjustment
            language: Language code
        
        Yields:
            Audio chunks as bytes
        """
        logger.info(f"[POLLY] Starting streaming synthesis")
        
        # Split text into sentences
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            logger.debug(f"[POLLY] Synthesizing sentence {i+1}/{len(sentences)}")
            
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
                logger.error(f"[POLLY] Failed to synthesize sentence {i+1}: {e}")
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
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences


# Global Polly synthesis engine instance
polly_synthesis_engine = PollySynthesisEngine()
