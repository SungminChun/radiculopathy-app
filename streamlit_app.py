# 📌 Streamlit 앱 기반 Myotome-Based Radiculopathy Prediction Tool (C4–T1)
# 기준: Kendall + Furukawa + Chiba 등 임상 논문 기반 가중치 적용

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Radiculopathy Predictor", layout="centered")
st.title("🧠 Myotome-Based Radiculopathy Prediction (C4–T1)")
st.markdown("---")

# ✅ 근육 목록 (입력 순서 고정)
muscles = [
    'Levator Scapulae', 'Deltoid', 'Biceps', 'Brachioradialis', 'ECRL', 'ECRB',
    'Pronator Teres', 'Triceps', 'FCR', 'ED', 'FCU',
    'FDP', 'Abductor Pollicis Brevis', 'First Dorsal Interossei'
]

st.subheader("🔢 근육별 MMT 점수를 입력하세요 (0~5)")
mmt_scores = {}
with st.form("mmt_form"):
    cols = st.columns(2)
    for i, muscle in enumerate(muscles):
        mmt_scores[muscle] = cols[i % 2].slider(muscle, 0, 5, 5)
    submitted = st.form_submit_button("🔍 결과 확인")

if submitted:
    # ✅ 각 근육별 지배 root 및 가중치 설정
    weights = {
        'Levator Scapulae': {'C4': 1.0},
        'Deltoid': {'C5': 1.0},
        'Biceps': {'C5': 0.9, 'C6': 0.1},
        'Brachioradialis': {'C5': 1.0, 'C6': 0.3},
        'ECRL': {'C5': 0.5, 'C6': 0.5},
        'ECRB': {'C6': 1.0, 'C7': 0.5},
        'Pronator Teres': {'C6': 1.0, 'C7': 0.3},
        'Triceps': {'C7': 1.0, 'C6': 0.3},
        'FCR': {'C7': 1.0, 'C6': 0.3},
        'ED': {'C7': 0.5, 'C8': 0.5},
        'FCU': {'C8': 1.0, 'T1': 0.3},
        'FDP': {'C8': 1.0, 'T1': 0.3},
        'Abductor Pollicis Brevis': {'T1': 1.0},
        'First Dorsal Interossei': {'T1': 1.0}
    }

    # ✅ 루트 초기화 (C4–T1)
    root_scores = {f'C{i}': 0 for i in range(4, 9)}
    root_scores['T1'] = 0

    # ✅ 알고리즘 실행: (5 - MMT 점수) × root별 가중치 누적
    for muscle, mmt in mmt_scores.items():
        weakness = 5 - mmt
        for root, weight in weights.get(muscle, {}).items():
            root_scores[root] += weakness * weight

    # ✅ 루트별 최대 이론 점수 계산 (모든 MMT가 0일 때 누적 최대치)
    max_possible = {f'C{i}': 0 for i in range(4, 9)}
    max_possible['T1'] = 0
    for muscle in muscles:
        for root, weight in weights.get(muscle, {}).items():
            max_possible[root] += weight * 5

    # ✅ 정규화된 점수 계산
    normalized_scores = {}
    for root in root_scores:
        if max_possible[root] > 0:
            normalized_scores[root] = root_scores[root] / max_possible[root]
        else:
            normalized_scores[root] = 0.0

    # ✅ 결과 표 생성 및 출력
    df = pd.DataFrame({
        "Root": list(root_scores.keys()),
        "Raw Score": [root_scores[r] for r in root_scores],
        "Normalized Score (%)": [f"{normalized_scores[r]*100:.1f}%" for r in root_scores]
    }).sort_values(by="Normalized Score (%)", ascending=False)

    st.markdown("---")
    st.subheader("📊 분석 결과")
    st.dataframe(df.set_index("Root"))

    # ✅ 최종 결과 출력
    most_likely = max(normalized_scores.items(), key=lambda x: x[1])
    st.markdown(f"""
    ### ✅ 최종 예측 결과:
    **'{most_likely[0]}' 신경근 병변 가능성이 가장 높습니다.**  
    정규화 점수: **{most_likely[1]:.2%}**
    """)
