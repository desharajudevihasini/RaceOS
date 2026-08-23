import joblib
import numpy as np

model = joblib.load("model/pitstop_model.pkl")

def predict_pit_stop(features):
    features = np.array(features).reshape(1, -1)

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    pit_probability = probabilities[1]

    return prediction, pit_probability