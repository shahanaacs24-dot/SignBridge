from collections import deque, Counter


class PredictionStabilizer:

    def __init__(self, window_size=7, required_count=5):
        self.predictions = deque(maxlen=window_size)
        self.required_count = required_count

    def update(self, prediction):
        self.predictions.append(prediction)

        if len(self.predictions) < self.required_count:
            return None

        counts = Counter(self.predictions)

        gesture, count = counts.most_common(1)[0]

        if count >= self.required_count:
            return gesture

        return None

    def reset(self):
        self.predictions.clear()