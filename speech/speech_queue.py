import queue
import threading

from speech.text_to_speech import TextToSpeech


class SpeechQueue:

    def __init__(self):

        self.queue = queue.Queue()

        self.tts = TextToSpeech()

        self.worker = threading.Thread(
            target=self._process,
            daemon=True
        )

        self.worker.start()


    def _process(self):

        while True:

            message = self.queue.get()

            if message:

                self.tts.speak(message)

            self.queue.task_done()


    def speak(self, message):

        if message:

            self.queue.put(message)