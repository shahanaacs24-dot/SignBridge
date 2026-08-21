import cv2
import csv
import os
import time

from hand_detector import HandDetector
from feature_extractor import extract_features


DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "gesture_data.csv"
)

GESTURES = {
    "1": "HELLO",
    "2": "YES",
    "3": "NO",
    "4": "HELP",
    "5": "STOP",
    "6": "WATER"
}


detector = HandDetector()
camera = cv2.VideoCapture(0)

print("\n=== SignBridge Data Collection ===")
print("Choose a gesture:")
for key, gesture in GESTURES.items():
    print(f"{key} -> {gesture}")

choice = input("\nEnter gesture number: ").strip()

if choice not in GESTURES:
    print("Invalid choice.")
    camera.release()
    detector.detector.close()
    exit()

label = GESTURES[choice]

print(f"\nCollecting samples for: {label}")
print("Press SPACE to start collecting.")
print("Press Q to quit.")

# Create CSV if it doesn't exist
file_exists = os.path.exists(DATA_FILE)

with open(DATA_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:
        header = [f"feature_{i}" for i in range(63)]
        header.append("label")
        writer.writerow(header)

    collecting = False
    sample_count = 0

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

            if collecting:

                writer.writerow(
                    features.tolist() + [label]
                )

                sample_count += 1

                cv2.putText(
                    frame,
                    f"COLLECTING: {label}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Samples: {sample_count}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    f"READY: {label}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

        cv2.imshow("SignBridge Data Collection", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):
            collecting = True
            print(f"Collecting {label} samples...")

        elif key == ord("q"):
            break

camera.release()
detector.detector.close()
cv2.destroyAllWindows()

print(f"\nCollected {sample_count} samples for {label}.")
print(f"Data saved to: {DATA_FILE}")