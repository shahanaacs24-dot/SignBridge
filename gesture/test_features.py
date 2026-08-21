import cv2
import time

from hand_detector import HandDetector
from feature_extractor import extract_features


detector = HandDetector()

camera = cv2.VideoCapture(0)

start_time = time.time()

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera.")
        break

    timestamp_ms = int((time.time() - start_time) * 1000)

    results = detector.detect(frame, timestamp_ms)

    if results.hand_landmarks:

        hand = results.hand_landmarks[0]

        features = extract_features(hand)

        print("Feature shape:", features.shape)
        print("First 6 values:", features[:6])

        # Only print once every ~1 second
        time.sleep(1)

    cv2.imshow("SignBridge", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
detector.detector.close()
cv2.destroyAllWindows()