const INPUT_SCHEMA = {
  project_info: [
    {
      key: "project_name",
      label: "1. 프로젝트명",
      placeholder: "예: AI 기반 개인 맞춤형 학습 플랫폼",
    },
    {
      key: "target_goal",
      label: "2. 핵심 목표",
      placeholder: "성공의 기준과 정량적 목표를 입력하세요",
    },
    {
      key: "resource_plan",
      label: "3. 자원 및 예산",
      placeholder: "인력, 시간, 자금 계획을 입력하세요",
    },
  ],
  risk_factors: [
    {
      key: "key_assumptions",
      label: "4. 기저 가정",
      placeholder: "성공을 위해 반드시 참이어야 하는 전제 조건",
    },
    {
      key: "process_flow",
      label: "5. 주요 프로세스",
      placeholder: "실행 단계별 핵심 마일스톤",
    },
    {
      key: "optimistic_view",
      label: "6. 낙관적 시나리오",
      placeholder: "기획자가 기대하는 최상의 결과",
    },
  ],
};

const FAILURE_CASES = [
  {
    project_name: "Quibi",
    failure_reason: "Product-Market Misfit",
    summary: "모바일 전용 숏폼 가설이 상황 변화와 경쟁 환경에 부합하지 않음.",
  },
  {
    project_name: "ScaleFactor",
    failure_reason: "Automation Fallacy",
    summary: "자동화라고 주장했으나 실제로는 수동 처리 비중이 큼.",
  },
  {
    project_name: "Fast",
    failure_reason: "Extreme Burn Rate",
    summary: "성장 대비 고정 비용이 폭증해 현금 흐름이 붕괴됨.",
  },
  {
    project_name: "Theranos",
    failure_reason: "Scientific Fraud & Ethics",
    summary: "핵심 기술의 검증 실패가 지속되었으나 리스크가 은폐됨.",
  },
  {
    project_name: "Katerra",
    failure_reason: "Scale Complexity",
    summary: "수직 통합 시도가 복잡성을 감당하지 못하고 붕괴됨.",
  },
];

const projectCol = document.getElementById("projectCol");
const riskCol = document.getElementById("riskCol");
const form = document.getElementById("planForm");
const resetBtn = document.getElementById("resetBtn");
const assumptionsText = document.getElementById("assumptionsText");
const adviceText = document.getElementById("adviceText");
const scenarioList = document.getElementById("scenarioList");
const resultsCard = document.getElementById("results");
const tempRange = document.getElementById("tempRange");
const tempValue = document.getElementById("tempValue");
const modelSelect = document.getElementById("modelSelect");
const reportMeta = document.getElementById("reportMeta");

const fieldState = new Map();

const buildField = (item) => {
  const wrapper = document.createElement("div");
  wrapper.className = "input-group";

  const label = document.createElement("label");
  label.setAttribute("for", item.key);
  label.textContent = item.label;

  const textarea = document.createElement("textarea");
  textarea.id = item.key;
  textarea.name = item.key;
  textarea.placeholder = item.placeholder;
  textarea.addEventListener("input", () => {
    fieldState.set(item.key, textarea.value.trim());
  });

  wrapper.appendChild(label);
  wrapper.appendChild(textarea);
  return wrapper;
};

const renderFields = () => {
  projectCol.innerHTML = "";
  riskCol.innerHTML = "";
  INPUT_SCHEMA.project_info.forEach((item) => projectCol.appendChild(buildField(item)));
  INPUT_SCHEMA.risk_factors.forEach((item) => riskCol.appendChild(buildField(item)));
};

const pickRandomCases = (count) => {
  const pool = [...FAILURE_CASES].sort(() => Math.random() - 0.5);
  return pool.slice(0, count);
};

const buildAssumptionsText = (data) => {
  const project = data.project_name || "해당 프로젝트";
  const goal = data.target_goal || "목표";
  const resource = data.resource_plan || "자원 계획";
  const assumptions = data.key_assumptions || "핵심 가정";

  return `${project}의 ${goal}이 ${resource}과 일치한다는 근거가 부족합니다. 특히 ${assumptions}이 깨질 경우, 전략이 즉시 붕괴할 수 있으므로 검증 기준과 대체 플랜을 명확히 해야 합니다.`;
};

const buildAdviceText = (data) => {
  const optimistic = data.optimistic_view || "낙관적 시나리오";
  const process = data.process_flow || "주요 프로세스";

  return `현재 ${optimistic}에 대한 기대가 높게 설정되어 있습니다. ${process}의 각 단계에서 실패 가능성을 수치로 추정하고, 조기 경보 지표(KRI)를 설정해 편향을 줄여야 합니다. 또한 불확실성 구간에서 의사결정을 멈출 수 있는 가드레일을 마련하세요.`;
};

const renderScenarios = () => {
  const cases = pickRandomCases(3);
  scenarioList.innerHTML = "";

  cases.forEach((item, idx) => {
    const severity = 6 + idx + Math.floor(Math.random() * 3);
    const card = document.createElement("div");
    card.className = "scenario-card";

    card.innerHTML = `
      <h4>${item.failure_reason}</h4>
      <p>${item.project_name} 사례처럼 ${item.summary}</p>
      <div class="severity"><span class="dot"></span>위험도: ${severity}/10</div>
    `;

    scenarioList.appendChild(card);
  });
};

const updateMeta = () => {
  reportMeta.textContent = `Model: ${modelSelect.value} · 강도: ${tempRange.value}`;
};

form.addEventListener("submit", (event) => {
  event.preventDefault();
  resultsCard.classList.add("loading");

  const data = {};
  fieldState.forEach((value, key) => {
    data[key] = value;
  });

  updateMeta();

  setTimeout(() => {
    assumptionsText.textContent = buildAssumptionsText(data);
    adviceText.textContent = buildAdviceText(data);
    renderScenarios();
    assumptionsText.classList.remove("muted");
    adviceText.classList.remove("muted");
    resultsCard.classList.remove("loading");
  }, 700);
});

resetBtn.addEventListener("click", () => {
  form.reset();
  fieldState.clear();
  assumptionsText.textContent = "입력 후 분석을 실행하면 결과가 표시됩니다.";
  adviceText.textContent = "입력 후 분석을 실행하면 결과가 표시됩니다.";
  assumptionsText.classList.add("muted");
  adviceText.classList.add("muted");
  scenarioList.innerHTML = "";
  updateMeta();
});

tempRange.addEventListener("input", () => {
  tempValue.textContent = tempRange.value;
  updateMeta();
});

modelSelect.addEventListener("change", updateMeta);

renderFields();
updateMeta();
