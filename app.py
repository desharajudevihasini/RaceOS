import streamlit as st
import os
from predictor import predict_pit_stop

st.set_page_config(page_title="RaceOS", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1 {
    color: #ff4b4b;
    text-align: center;
}
.stButton > button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}
div[data-testid="metric-container"] {
    background-color: #1c1f26;
    border: 1px solid #ff4b4b;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ RaceOS — AI Powered F1 Strategy Assistant")
st.caption("Predict optimal pit stop windows using race telemetry and AI")

driver = st.selectbox(
    "Select Driver",
    ["Verstappen", "Hamilton", "Leclerc", "Norris", "Russell"]
)

uploaded_video = st.file_uploader("Upload Race Video", type=["mp4", "mov"])

if uploaded_video:
    os.makedirs("uploads", exist_ok=True)
    video_path = os.path.join("uploads", uploaded_video.name)

    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    st.video(video_path)
    st.success("Video uploaded successfully!")

    st.subheader("📥 Enter Race Telemetry")

    lap_number = st.number_input(
        "Lap Number",
        min_value=1,
        max_value=70,
        value=40
    )

    compound_name = st.selectbox(
        "Tyre Compound",
        ["Soft", "Medium", "Hard"]
    )

    compound_map = {
        "Soft": 2,
        "Medium": 1,
        "Hard": 0
    }

    tyre_life = st.number_input(
        "Tyre Life",
        min_value=1,
        max_value=40,
        value=20
    )

    position = st.number_input(
        "Current Position",
        min_value=1,
        max_value=20,
        value=5
    )

    if st.button("Predict Pit Stop"):
        with st.spinner("Analyzing race strategy..."):

            compound = compound_map[compound_name]
            degradation = tyre_life * 0.5
            race_progress = int((lap_number / 70) * 100)

            features = [
                lap_number,
                compound,
                2,
                tyre_life,
                position,
                88.0,
                0.8,
                degradation,
                race_progress,
                0,
                max(tyre_life - 1, 0)
            ]

            # ML backend prediction
            ml_prediction, ml_probability = predict_pit_stop(features)

            # Rule-based scoring
            score = 0

            if lap_number > 50:
                score += 40
            elif lap_number > 30:
                score += 20

            if tyre_life > 25:
                score += 30
            elif tyre_life > 15:
                score += 15

            if compound_name == "Soft":
                score += 20
            elif compound_name == "Medium":
                score += 10

            if position <= 5:
                score += 10

            probability_percent = min(score, 100)

            if probability_percent >= 60:
                prediction = 1
            else:
                prediction = 0

            st.subheader("📊 Race Strategy Dashboard")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Driver", driver)
                st.metric("Pit Probability", f"{probability_percent}%")

            with col2:
                if prediction == 1:
                    risk = "HIGH"
                    strategy = "Aggressive Undercut"
                else:
                    risk = "LOW"
                    strategy = "Long Stint Strategy"

                st.metric("Risk Level", risk)
                st.metric("Strategy", strategy)

            st.progress(probability_percent)

            st.subheader("🧠 AI Insights")
            st.write(f"✓ Lap Number: {lap_number}")
            st.write(f"✓ Tyre Life: {tyre_life}")
            st.write(f"✓ Position: P{position}")
            st.write(f"✓ Compound: {compound_name}")

            st.subheader("🏁 Final Prediction")

            if prediction == 1:
                st.success(f"Pit Stop Likely ✅ ({probability_percent}%)")
                st.write("Recommendation: Prepare pit crew in next 1–2 laps.")
            else:
                st.error(f"No Pit Stop Likely ❌ ({probability_percent}%)")
                st.write("Recommendation: Continue current strategy.")