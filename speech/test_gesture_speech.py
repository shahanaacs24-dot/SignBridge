import cv2
import time

from gesture.gesture_engine import GestureEngine
from speech.text_to_speech import TextToSpeech


engine = GestureEngine()
tts = TextToSpeech()

camera = cv2.VideoCapture(0)

start_time = time.time()

last_message = None

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera.")
        break

    timestamp_ms = int(
        (time.time() - start_time) * 1000
    )

    result = engine.process_frame(
        frame,
        timestamp_ms
    )

    # Speak only when a NEW event is triggered
    if result["triggered"]:

        message = result["message"]

        if message and message != last_message:

            print("Speaking:", message)

            tts.speak(message)

            last_message = message

    # Display the result
    if result["gesture"]:

        cv2.putText(
            frame,
            f"Sign: {result['gesture']}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    if result["emergency"]:

        cv2.putText(
            frame,
            "!!! EMERGENCY !!!",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "SignBridge - Gesture to Speech",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
engine.close()
cv2.destroyAllWindows()