import pyttsx3
import threading


class TextToSpeech:

    def __init__(self):
        self.lock = threading.Lock()

    def speak(self, text):

        if not text:
            return

        # Prevent multiple speech engines running at once
        if not self.lock.acquire(blocking=False):
            return

        try:
            engine = pyttsx3.init()

            engine.setProperty("rate", 150)
            engine.setProperty("volume", 1.0)

            engine.say(text)
            engine.runAndWait()

            engine.stop()

        finally:
            self.lock.release()