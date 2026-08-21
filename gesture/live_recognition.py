import cv2
import time
import os
import joblib

from hand_detector import HandDetector
from feature_extractor import extract_features


# -----------------------------
# Load trained model
# -----------------------------

MODEL_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "gesture_model.pkl"
)

model = joblib.load(MODEL_FILE)

print("Model loaded successfully!")


# -----------------------------
# Start hand detector
# -----------------------------

detector = HandDetector()

camera = cv2.VideoCapture(0)

start_time = time.time()


# -----------------------------
# Live recognition
# -----------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera.")
        break

    timestamp_ms = int(
        (time.time() - start_time) * 1000
    )

    results = detector.detect(
        frame,
        timestamp_ms
    )

    prediction = "No hand detected"
    confidence = 0.0

    if results.hand_landmarks:

        hand = results.hand_landmarks[0]

        features = extract_features(hand)

        # Make prediction
        prediction = model.predict(
            [features]
        )[0]

        # Get confidence
        probabilities = model.predict_proba(
            [features]
        )[0]

        confidence = max(probabilities)

    # -----------------------------
    # Display prediction
    # -----------------------------

    cv2.rectangle(
        frame,
        (10, 10),
        (500, 100),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        f"Sign: {prediction}",
        (25, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Confidence: {confidence * 100:.1f}%",
        (25, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "SignBridge - Live Recognition",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
detector.detector.close()
cv2.destroyAllWindows()