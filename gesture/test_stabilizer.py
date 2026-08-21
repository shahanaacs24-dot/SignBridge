from prediction_stabilizer import PredictionStabilizer


stabilizer = PredictionStabilizer(
    window_size=7,
    required_count=5
)


predictions = [
    "HELP",
    "HELP",
    "HELP",
    "NO",
    "HELP",
    "HELP",
    "HELP"
]


for prediction in predictions:

    result = stabilizer.update(prediction)

    print(
        f"Input: {prediction} → Confirmed: {result}"
    )