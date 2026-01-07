import os
import json
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
        
        self.client = instructor.patch(OpenAI(api_key=api_key))
        self.model = model
        self.temperature = temperature
        # JSON 데이터 로드
        self.failure_db = self._load_failure_db()

    def _load_failure_db(self):
        file_path = "failure_cases.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _get_context_examples(self, project_name):
        examples_str = ""
        for case in self.failure_db[:3]:  # 상위 3개 사용
            examples_str += f"\n- 사례: {case['project_name']} ({case['industry']})\n"
            examples_str += f"  실패 원인: {case['failure_reason']}\n"
            examples_str += f"  요약: {case['summary']}\n"
        return examples_str

    def run(self, data: dict) -> AnalysisReport:
        reference_cases = self._get_context_examples(data.get('project_name'))

        report = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_model=AnalysisReport,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n\n다음은 당신이 참고할 수 있는 실제 스타트업 실패 사례들입니다:" + reference_cases},
                {"role": "user", "content": f"""
                [분석 대상 계획서]
                - 프로젝트명: {data.get('project_name')}
                - 핵심 목표: {data.get('target_goal')}
                - 자원 계획: {data.get('resource_plan')}
                - 기저 가정: {data.get('key_assumptions')}
                - 실행 프로세스: {data.get('process_flow')}
                - 낙관적 전망: {data.get('optimistic_view')}
                
                위의 실제 실패 사례들과 비교하여, 이 계획의 치명적인 결함을 분석하고 리포트를 작성하세요.
                """}
            ]
        )
        return report