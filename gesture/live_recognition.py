import cv2
import time
import os
import joblib

from gesture.hand_detector import HandDetector
from gesture.feature_extractor import extract_features
from gesture.prediction_stabilizer import PredictionStabilizer

from emergency.emergency_handler import EmergencyHandler


# -----------------------------
# Load model
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
# Initialize components
# -----------------------------

detector = HandDetector()

stabilizer = PredictionStabilizer(
    window_size=7,
    required_count=5
)

emergency_handler = EmergencyHandler()

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

    raw_prediction = None
    confirmed_prediction = None
    confidence = 0.0

    # -----------------------------
    # Detect hand
    # -----------------------------

    if results.hand_landmarks:

        hand = results.hand_landmarks[0]

        features = extract_features(hand)

        # Raw model prediction
        raw_prediction = model.predict(
            [features]
        )[0]

        probabilities = model.predict_proba(
            [features]
        )[0]

        confidence = max(probabilities)

        # Stabilize prediction
        confirmed_prediction = stabilizer.update(
            raw_prediction
        )

    else:

        stabilizer.reset()


    # -----------------------------
    # Process confirmed gesture
    # -----------------------------

    emergency = False
    message = ""

    if confirmed_prediction:

        result = emergency_handler.process(
            confirmed_prediction
        )

        emergency = result["emergency"]
        triggered = result["triggered"]
        message = result["message"]


    # -----------------------------
    # Display
    # -----------------------------

    cv2.rectangle(
        frame,
        (10, 10),
        (550, 130),
        (0, 0, 0),
        -1
    )

    if confirmed_prediction:

        cv2.putText(
            frame,
            f"Sign: {confirmed_prediction}",
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

        if emergency:

            cv2.putText(
                frame,
                "!!! EMERGENCY !!!",
                (25, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

    else:

        cv2.putText(
            frame,
            "Detecting...",
            (25, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )


    cv2.imshow(
        "SignBridge - Live Recognition",
        frame
    )


    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------

camera.release()
detector.detector.close()
cv2.destroyAllWindows()