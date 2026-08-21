import cv2
import time

from gesture.gesture_engine import GestureEngine


engine = GestureEngine()

camera = cv2.VideoCapture(0)

start_time = time.time()

while True:

    success, frame = camera.read()

    if not success:
        break

    timestamp_ms = int(
        (time.time() - start_time) * 1000
    )

    result = engine.process_frame(
        frame,
        timestamp_ms
    )

    print(result)

    cv2.imshow(
        "SignBridge Gesture Engine",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
engine.close()
cv2.destroyAllWindows()