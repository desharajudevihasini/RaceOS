# RaceOS 🏎️
RaceOS is an F1 pit stop strategy project I made to experiment with using machine learning for race decisions.
## What it does
You enter some basic race information:
- Driver
- Lap number
- Tyre compound
- Tyre life
- Current position
RaceOS then gives a pit stop recommendation along with a probability, risk level and suggested strategy.
 link to git:https://raceosf1-nufin4hinpnixgatyzjst7.streamlit.app/
## How it works
I trained a Random Forest model using pit stop data.
There is also some rule-based scoring in the app based on things like lap number, tyre life, tyre compound and position.
The app is made with Streamlit.

## Files
- `app.py` - main Streamlit app
- `predictor.py` - loads the trained model and makes predictions
- `train_model.py` - trains the Random Forest model
- `requirements.txt` - Python libraries needed
- `.gitignore` - files to ignore
## Tech used

Python  
Streamlit  
Pandas  
NumPy  
scikit-learn  
Joblib

## Status

Completed prototype.
This was mainly a project for learning how machine learning could be used for F1 strategy.
## What I want to improve
I would like to use more race data, make the predictions more realistic and eventually connect the system to actual race telemetry.
