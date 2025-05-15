import streamlit as st

# 루트별 근육 가중치 정의
weights = {
    "C4": {"Levator scapulae": 0.549, "Trapezius (upper)": 0.451},
    "C5": {"Deltoid": 0.395, "Supraspinatus": 0.339, "Rhomboids": 0.266},
    "C6": {"Biceps": 0.500, "Wrist extensors (ECRL/B)": 0.300, "Supinator": 0.200},
    "C7": {"Triceps": 0.476, "Wrist flexors": 0.286, "Finger extensors": 0.238},
    "C8": {"Finger flexors (FDP/FDS)": 0.476, "Thumb extensors (EPL/EPB)": 0.262, "Thenar muscles": 0.262},
    "T1": {"Interossei": 0.531, "Hypothenar": 0.469}
}

st.title("🧠 Weighted Myotome Radiculopathy Predictor")
st.markdown("근육별 MMT 점수를 입력하면, 루트별 가중치를 반영해 **가장 약화된 루트(점수 낮음)**를 병변 루트로 예측합니다.")

scores = {}
for root, muscles in weights.items():
    st.subheader(f"{root} 루트 근육 평가")
    root_score = 0
    total_weight = sum(muscles.values())
    for muscle, weight in muscles.items():
        mmt = st.slider(f"{muscle} (0~5점)", 0, 5, 5, key=f"{root}_{muscle}")
        root_score += mmt * weight
    normalized_score = root_score / total_weight if total_weight > 0 else 0
    scores[root] = round(normalized_score, 2)

if st.button("예측하기"):
    min_score = min(scores.values())
    candidates = [root for root, score in scores.items() if score == min_score]
    result = ", ".join(candidates)
    st.error(f"🚨 예측된 병변 루트: **{result}**")
    st.subheader("루트별 정규화 점수")
    st.json(scores)
