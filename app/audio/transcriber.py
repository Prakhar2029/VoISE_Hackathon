import speech_recognition as sr

class Transcriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_data):
        """
        Transcribes audio data to text.
        Returns: (text, error_message)
        """
        if audio_data is None:
            return "", "No audio data"

        try:
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data)
            return text, None
        except sr.UnknownValueError:
            return "", "Speech not recognized (UnknownValueError)"
        except sr.RequestError as e:
            return "", f"API unavailable: {e}"
        except Exception as e:
            return "", f"Error: {e}"

    def transcribe_file(self, file_path):
        """
        Transcribes audio from a file path.
        """
        try:
            with sr.AudioFile(file_path) as source:
                # Adjust for noise in the file
                self.recognizer.adjust_for_ambient_noise(source)
                audio_data = self.recognizer.record(source)
                return self.transcribe(audio_data)
        except Exception as e:
            return "", f"Error reading file: {e}"
