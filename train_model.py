import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

# Create model folder
os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("data/pitstop_data.csv")

print("Dataset loaded successfully!")
print(df.head())

# Convert target to numeric (important)
df["PitNextLap"] = pd.to_numeric(df["PitNextLap"], errors="coerce")

# Remove rows where target is missing
df = df.dropna(subset=["PitNextLap"])

# Fill missing feature values
numeric_cols = [
    "LapNumber",
    "Stint",
    "TyreLife",
    "Position",
    "LapTime (s)",
    "LapTime_Delta",
    "Cumulative_Degradation",
    "RaceProgress",
    "Position_Change",
    "Prev_TyreLife"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(0)

# Encode Compound
encoder = LabelEncoder()
df["Compound"] = encoder.fit_transform(df["Compound"].astype(str))

# Features
X = df[
    [
        "LapNumber",
        "Compound",
        "Stint",
        "TyreLife",
        "Position",
        "LapTime (s)",
        "LapTime_Delta",
        "Cumulative_Degradation",
        "RaceProgress",
        "Position_Change",
        "Prev_TyreLife"
    ]
]

# Target
y = df["PitNextLap"]

print("Remaining rows:", len(df))
print("NaNs in target:", y.isna().sum())

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Model accuracy:", accuracy)

# Save model
joblib.dump(model, "model/pitstop_model.pkl")
print("Model saved successfully!")