import os
import joblib

from gesture.hand_detector import HandDetector
from gesture.feature_extractor import extract_features
from gesture.prediction_stabilizer import PredictionStabilizer
from emergency.emergency_handler import EmergencyHandler


class GestureEngine:

    def __init__(self):

        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models",
            "gesture_model.pkl"
        )

        self.model = joblib.load(model_path)

        self.detector = HandDetector()

        self.stabilizer = PredictionStabilizer(
            window_size=7,
            required_count=5
        )

        self.emergency_handler = EmergencyHandler()

    def process_frame(self, frame, timestamp_ms):

        results = self.detector.detect(
            frame,
            timestamp_ms
        )

        if not results.hand_landmarks:

            self.stabilizer.reset()

            return {
                "frame": frame,
                "gesture": None,
                "message": None,
                "emergency": False,
                "triggered": False,
                "confidence": 0.0
            }

        hand = results.hand_landmarks[0]

        features = extract_features(hand)

        raw_prediction = self.model.predict(
            [features]
        )[0]

        probabilities = self.model.predict_proba(
            [features]
        )[0]

        confidence = max(probabilities)

        confirmed = self.stabilizer.update(
            raw_prediction
        )

        if confirmed is None:

            return {
                "frame": frame,
                "gesture": None,
                "message": None,
                "emergency": False,
                "triggered": False,
                "confidence": confidence
            }

        emergency_result = self.emergency_handler.process(
            confirmed
        )

        return {
            "frame": frame,
            "gesture": confirmed,
            "message": emergency_result["message"],
            "emergency": emergency_result["emergency"],
            "triggered": emergency_result["triggered"],
            "confidence": confidence
        }

    def close(self):
        self.detector.detector.close()