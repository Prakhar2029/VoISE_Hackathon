import pyttsx3
import threading

class Speaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
        except:
            self.engine = None

    def speak(self, text):
        """
        Speaks the text in a separate thread to avoid blocking the UI.
        """
        if self.engine:
            # Run in a separate thread
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.start()

    def _speak_thread(self, text):
        try:
            # Re-initialize in thread if needed (pyttsx3 can be picky about threads)
            # But usually sharing the engine instance or creating a new one per thread works differently per OS.
            # Safest for a hackathon script: create a new engine locally in the thread
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            pass
