import io
import tempfile
import os


class SpeechProcessor:
    def __init__(self):
        # Defer creation of the recognizer to avoid import-time errors
        self.recognizer = None
        self.supported_languages = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'ta': 'ta-IN',
            'te': 'te-IN',
            'bn': 'bn-IN',
            'mr': 'mr-IN'
        }

    async def speech_to_text(self, audio_file, language: str = 'en') -> str:
        """Convert speech to text with multilingual support"""
        try:
            # Local imports to avoid import-time dependency errors
            import speech_recognition as sr
            from pydub import AudioSegment
            # Convert uploaded audio to WAV format
            audio_data = await audio_file.read()
            audio = AudioSegment.from_file(io.BytesIO(audio_data))

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                audio.export(temp_file.name, format="wav")

                with sr.AudioFile(temp_file.name) as source:
                    # Ensure recognizer exists
                    if self.recognizer is None:
                        self.recognizer = sr.Recognizer()

                    recorded = self.recognizer.record(source)

                    # Use Google Speech Recognition
                    language_code = self.supported_languages.get(
                        language, 'en-US')
                    text = self.recognizer.recognize_google(
                        recorded, language=language_code)

                # Clean up
                os.unlink(temp_file.name)

            return text

        except Exception as e:
            # speech_recognition-specific exceptions may not be importable if
            # package missing; normalize to a generic exception
            raise Exception(f"Error processing audio: {e}")
