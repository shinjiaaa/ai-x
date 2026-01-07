from pydantic import BaseModel, Field
from typing import List

INPUT_SCHEMA = {
    "project_info": [
        {"key": "project_name", "label": "1. 프로젝트명", "placeholder": "예: AI 기반 개인 맞춤형 학습 플랫폼"},
        {"key": "target_goal", "label": "2. 핵심 목표", "placeholder": "성공의 기준과 정량적 목표를 입력하세요"},
        {"key": "resource_plan", "label": "3. 자원 및 예산", "placeholder": "인력, 시간, 자금 계획을 입력하세요"}
    ],
    "risk_factors": [
        {"key": "key_assumptions", "label": "4. 기저 가정", "placeholder": "성공을 위해 반드시 참이어야 하는 전제 조건"},
        {"key": "process_flow", "label": "5. 주요 프로세스", "placeholder": "실행 단계별 핵심 마일스톤"},
        {"key": "optimistic_view", "label": "6. 낙관적 시나리오", "placeholder": "기획자가 기대하는 최상의 결과"}
    ]
}

class RiskFactor(BaseModel):
    risk_name: str = Field(..., description="위험 요소 명칭")
    severity: int = Field(..., description="위험도 (1-10)")
    reason: str = Field(..., description="실패할 것으로 예상되는 구체적 논리")

class AnalysisReport(BaseModel):
    assumptions_check: str = Field(..., description="기저 가정의 타당성 비판")
    failure_scenarios: List[RiskFactor] = Field(..., description="3가지 핵심 실패 시나리오")
    debiasing_advice: str = Field(..., description="기획자의 편향을 교정하기 위한 조언")

# 3. 페르소나 설정
SYSTEM_PROMPT = """
당신은 전략적 의사결정을 돕는 '디바이어싱(Debiasing) 전문가'입니다.
사용자의 계획에서 '낙관적 편향'을 제거하고, 숨겨진 구조적 한계와 리스크를 식별하는 것이 임무입니다.
냉철하고 비판적인 시각으로 '사전 부검(Pre-mortem)'을 수행하세요.
"""