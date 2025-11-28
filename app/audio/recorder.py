import speech_recognition as sr

class AudioRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listens to the microphone and returns the audio data.
        """
        try:
            with self.microphone as source:
                # Re-adjust for ambient noise before every listen
                # This helps if the environment changes (e.g. AC turns on)
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return audio
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            # print(f"Error recording audio: {e}")
            return None
