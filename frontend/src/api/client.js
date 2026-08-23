const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

async function request(path, { method = "GET", body, token } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new ApiError(response.status, data?.error?.message ?? response.statusText);
  }
  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  login: (email, password) =>
    request("/auth/login", { method: "POST", body: { email, password } }),
  me: (token) => request("/auth/me", { token }),
  dashboardOverview: (token) => request("/dashboard/overview", { token }),
  dashboardTrends: (token) => request("/dashboard/trends", { token }),
  providerActivity: (token) => request("/dashboard/provider-activity", { token }),
  executiveReport: (token) => request("/reports/executive", { token }),
  listAlerts: (token) => request("/monitoring/alerts", { token }),
  acknowledgeAlert: (token, alertId) =>
    request(`/monitoring/alerts/${alertId}/acknowledge`, { method: "PATCH", token }),
  listPatients: (token) => request("/patients", { token }),
  getPatient: (token, patientId) => request(`/patients/${patientId}`, { token }),
  listProviders: (token) => request("/providers", { token }),
  listAppointments: (token) => request("/appointments", { token }),
  createAppointment: (token, body) => request("/appointments", { method: "POST", body, token }),
  updateAppointmentStatus: (token, appointmentId, appointmentStatus) =>
    request(`/appointments/${appointmentId}/status`, {
      method: "PATCH",
      body: { status: appointmentStatus },
      token,
    }),
  createConsultation: (token, body) => request("/consultations", { method: "POST", body, token }),
  consultationHistory: (token, patientId) => request(`/consultations/${patientId}`, { token }),
  readingHistory: (token, patientId) => request(`/monitoring/readings/${patientId}`, { token }),
  submitReading: (token, body) => request("/monitoring/readings", { method: "POST", body, token }),
  predictionHistory: (token, patientId) => request(`/ai/predictions/${patientId}`, { token }),
  runRiskAssessment: (token, patientId) =>
    request("/ai/risk-assessment", { method: "POST", body: { patient_id: patientId }, token }),
  modelMetadata: (token) => request("/ai/model/metadata", { token }),
};
