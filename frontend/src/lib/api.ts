export interface CopilotStep {
  step_number: number;
  agent_name: string;
  action: string;
  thought: string;
  observation: string;
}

export interface Citation {
  index: number;
  source_type: string;
  title: string;
  file_path: string;
  section_title: string;
  snippet: string;
  relevance_score: number;
}

export interface CopilotResponse {
  query: string;
  intent: string;
  final_answer: string;
  confidence: number;
  steps: CopilotStep[];
  citations: Citation[];
  execution_time_ms: number;
}

const API_BASE = "http://localhost:8000/api/v1";

export async function sendCopilotQuery(query: string): Promise<CopilotResponse> {
  const res = await fetch(`${API_BASE}/chat/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  const json = await res.json();
  return json.data;
}

export async function fetchIncidents() {
  const res = await fetch(`${API_BASE}/incidents`);
  const json = await res.json();
  return json.data;
}

export async function fetchIncidentRCA(incidentKey: string) {
  const res = await fetch(`${API_BASE}/incidents/${incidentKey}/investigate`);
  const json = await res.json();
  return json.data;
}

export async function runEvaluation() {
  const res = await fetch(`${API_BASE}/evaluations/run`);
  const json = await res.json();
  return json.data;
}
