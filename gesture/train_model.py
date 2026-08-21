import csv
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "gesture_data.csv"
)

MODEL_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "gesture_model.pkl"
)


# -----------------------------
# Load dataset
# -----------------------------

X = []
y = []

with open(DATA_FILE, newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        features = [
            float(row[f"feature_{i}"])
            for i in range(63)
        ]

        X.append(features)
        y.append(row["label"])


print("Total samples:", len(X))
print("Classes:", sorted(set(y)))


# -----------------------------
# Train / test split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# Train Random Forest
# -----------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)


# -----------------------------
# Evaluate
# -----------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)


# -----------------------------
# Save model
# -----------------------------

joblib.dump(model, MODEL_FILE)

print("\nModel saved to:")
print(MODEL_FILE)