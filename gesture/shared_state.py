import threading


class SharedState:

    def __init__(self):
        self.lock = threading.Lock()

        self.result = {
            "gesture": None,
            "message": None,
            "emergency": False,
            "triggered": False,
            "confidence": 0.0
        }

    def update(self, result):

        with self.lock:
            self.result = {
                "gesture": result.get("gesture"),
                "message": result.get("message"),
                "emergency": result.get("emergency", False),
                "triggered": result.get("triggered", False),
                "confidence": result.get("confidence", 0.0)
            }

    def get(self):

        with self.lock:
            return self.result.copy()