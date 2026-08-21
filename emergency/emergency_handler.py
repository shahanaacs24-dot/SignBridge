import time


class EmergencyHandler:

    EMERGENCY_GESTURES = {
        "HELP": "I NEED HELP",
        "STOP": "STOP - URGENT"
    }

    def __init__(self, cooldown_seconds=3):
        self.active = False
        self.message = ""
        self.last_trigger_time = 0
        self.cooldown_seconds = cooldown_seconds

    def process(self, gesture):
        current_time = time.time()

        if gesture in self.EMERGENCY_GESTURES:

            # Prevent the same emergency from firing repeatedly
            if current_time - self.last_trigger_time < self.cooldown_seconds:
                return {
                    "emergency": False,
                    "triggered": False,
                    "gesture": gesture,
                    "message": self.message
                }

            self.active = True
            self.message = self.EMERGENCY_GESTURES[gesture]
            self.last_trigger_time = current_time

            return {
                "emergency": True,
                "triggered": True,
                "gesture": gesture,
                "message": self.message
            }

        self.active = False
        self.message = ""

        return {
            "emergency": False,
            "triggered": False,
            "gesture": gesture,
            "message": gesture
        }

    def reset(self):
        self.active = False
        self.message = ""
        self.last_trigger_time = 0