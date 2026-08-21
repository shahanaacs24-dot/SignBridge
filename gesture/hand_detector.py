import os
import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models",
            "hand_landmarker.task"
        )

        base_options = mp.tasks.BaseOptions(
            model_asset_path=model_path
        )

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = mp.tasks.vision.HandLandmarker.create_from_options(
            options
        )

    def detect(self, frame, timestamp_ms):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        results = self.detector.detect_for_video(
            image,
            timestamp_ms
        )

        return results