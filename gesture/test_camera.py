import cv2
import time

from hand_detector import HandDetector


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

    # Draw detected landmarks
    if results.hand_landmarks:

        for hand_landmarks in results.hand_landmarks:

            height, width, _ = frame.shape

            points = []

            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                points.append((x, y))

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

            # Draw connections between landmarks
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (0, 9), (9, 10), (10, 11), (11, 12),
                (0, 13), (13, 14), (14, 15), (15, 16),
                (0, 17), (17, 18), (18, 19), (19, 20),
                (5, 9), (9, 13), (13, 17)
            ]

            for start, end in connections:
                cv2.line(
                    frame,
                    points[start],
                    points[end],
                    (0, 255, 0),
                    2
                )

    cv2.imshow("SignBridge - Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
detector.detector.close()
cv2.destroyAllWindows()