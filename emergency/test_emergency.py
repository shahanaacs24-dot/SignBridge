from emergency_handler import EmergencyHandler


handler = EmergencyHandler()


test_gestures = [
    "HELLO",
    "HELP",
    "WATER",
    "STOP",
    "YES"
]


for gesture in test_gestures:

    result = handler.process(gesture)

    print(f"\nGesture: {gesture}")
    print(f"Emergency: {result['emergency']}")
    print(f"Message: {result['message']}")