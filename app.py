import streamlit as st
from engine import RiskAnalysisEngine
from llm import INPUT_SCHEMA

st.set_page_config(page_title="AI Risk Validator", layout="wide")

st.title("🛡️ AI 전략적 리스크 검증 시스템")
st.caption("고정 규격 입력을 통한 계획의 구조적 결함 진단")

# 사이드바 설정 (API 키는 .env에서 가져오지만, 모델 설정 등은 유지)
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo"])
    temp_val = st.slider("비판적 강도", 0.0, 1.0, 0.7)
    st.info(".env 파일의 API 키를 사용 중입니다.")

# 메인 입력 폼
with st.form("plan_form"):
    st.subheader("📋 기획서 작성")
    col1, col2 = st.columns(2)
    user_inputs = {}
    
    for item in INPUT_SCHEMA["project_info"]:
        with col1:
            user_inputs[item["key"]] = st.text_area(item["label"], placeholder=item["placeholder"], height=100)
            
    for item in INPUT_SCHEMA["risk_factors"]:
        with col2:
            user_inputs[item["key"]] = st.text_area(item["label"], placeholder=item["placeholder"], height=100)
            
    submit = st.form_submit_button("리스크 분석 실행")

# 실행 및 결과 출력
if submit:
    try:
        engine = RiskAnalysisEngine(model=model_name, temperature=temp_val)
        with st.spinner("전문가 모드로 리스크를 추출 중입니다..."):
            # 이제 report는 단순 문자열이 아니라 AnalysisReport 객체입니다.
            report = engine.run(user_inputs)
            
            st.markdown("---")
            st.subheader("📊 리스크 검증 리포트")
            
            # 1. 가정 검토 영역
            st.warning("🧐 **기저 가정 타당성 검토**")
            st.write(report.assumptions_check)
            
            # 2. 실패 시나리오 영역 (카드 형태)
            st.write("🚨 **핵심 실패 시나리오**")
            cols = st.columns(3)
            for idx, risk in enumerate(report.failure_scenarios):
                with cols[idx]:
                    st.error(f"**{risk.risk_name}**")
                    st.caption(f"위험도: {risk.severity}/10")
                    st.write(risk.reason)
            
            # 3. 디바이어싱 조언
            st.success("💡 **디바이어싱 전략 조언**")
            st.write(report.debiasing_advice)
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")