class EmergencyHandler:

    EMERGENCY_GESTURES = {
        "HELP": "I NEED HELP",
        "STOP": "STOP - URGENT"
    }

    def __init__(self):
        self.active = False
        self.message = ""

    def process(self, gesture):
        """
        Process a recognized gesture and determine
        whether it represents an emergency.
        """

        if gesture in self.EMERGENCY_GESTURES:
            self.active = True
            self.message = self.EMERGENCY_GESTURES[gesture]

            return {
                "emergency": True,
                "gesture": gesture,
                "message": self.message
            }

        self.active = False
        self.message = ""

        return {
            "emergency": False,
            "gesture": gesture,
            "message": gesture
        }

    def reset(self):
        self.active = False
        self.message = ""