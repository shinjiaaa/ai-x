import os
import instructor
from openai import OpenAI
from dotenv import load_dotenv
from llm import SYSTEM_PROMPT, AnalysisReport

load_dotenv()

class RiskAnalysisEngine:
    def __init__(self, model="gpt-4o", temperature=0.7):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API Key가 .env 파일에 설정되지 않았습니다.")
        
        # Instructor로 OpenAI 클라이언트 래핑
        self.client = instructor.patch(OpenAI(api_key=api_key))
        self.model = model
        self.temperature = temperature

    def run(self, data: dict) -> AnalysisReport:
        # Pydantic 모델을 사용하여 구조화된 데이터 요청
        report = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_model=AnalysisReport,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""
                [분석 대상 계획서]
                - 프로젝트명: {data.get('project_name')}
                - 핵심 목표: {data.get('target_goal')}
                - 자원 계획: {data.get('resource_plan')}
                - 기저 가정: {data.get('key_assumptions')}
                - 실행 프로세스: {data.get('process_flow')}
                - 낙관적 전망: {data.get('optimistic_view')}
                """}
            ]
        )
        return report