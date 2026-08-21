from gesture.communication_event import CommunicationEvent

class CommunicationEvent:

    def __init__(
        self,
        gesture=None,
        message=None,
        emergency=False,
        triggered=False,
        confidence=0.0
    ):
        self.gesture = gesture
        self.message = message
        self.emergency = emergency
        self.triggered = triggered
        self.confidence = confidence

    def to_dict(self):
        return {
            "gesture": self.gesture,
            "message": self.message,
            "emergency": self.emergency,
            "triggered": self.triggered,
            "confidence": round(self.confidence, 3)
        }