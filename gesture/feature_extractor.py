import numpy as np


def extract_features(hand_landmarks):
    """
    Convert 21 MediaPipe hand landmarks into
    a normalized 63-value feature vector.
    """

    # Wrist = landmark 0
    wrist = hand_landmarks[0]

    features = []

    # Make coordinates relative to the wrist
    for landmark in hand_landmarks:
        x = landmark.x - wrist.x
        y = landmark.y - wrist.y
        z = landmark.z - wrist.z

        features.extend([x, y, z])

    # Convert to numpy array
    features = np.array(features, dtype=np.float32)

    # Normalize by the largest absolute value
    max_value = np.max(np.abs(features))

    if max_value > 0:
        features = features / max_value

    return features