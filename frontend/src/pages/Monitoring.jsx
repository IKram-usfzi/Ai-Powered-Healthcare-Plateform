import { useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api, ApiError } from "../api/client";

const SEVERITY_STYLES = {
  critical: { box: "bg-[#FEF2F2] border border-[#FECACA]", icon: "text-error", label: "Critical" },
  high: { box: "bg-[#FEF2F2] border border-[#FECACA]", icon: "text-error", label: "High" },
  medium: { box: "bg-[#FFFBEB] border border-[#FDE68A]", icon: "text-[#D97706]", label: "Medium" },
  low: { box: "bg-surface-container-low border border-inverse-primary", icon: "text-primary", label: "Low" },
};

export default function Monitoring() {
  const { token, user } = useAuth();
  const [alerts, setAlerts] = useState(null);
  const [alertsError, setAlertsError] = useState("");
  const [patients, setPatients] = useState(null);
  const [selectedPatientId, setSelectedPatientId] = useState("");
  const [readings, setReadings] = useState(null);
  const [readingsError, setReadingsError] = useState("");

  function loadAlerts() {
    api
      .listAlerts(token)
      .then((data) => {
        setAlerts(data);
        setAlertsError("");
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 403) {
          setAlertsError("Alert details require Administrator or Doctor access.");
        } else {
          setAlertsError(err.message);
        }
      });
  }

  useEffect(() => {
    loadAlerts();
    api.listPatients(token).then(setPatients).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function handleAcknowledge(alertId) {
    try {
      await api.acknowledgeAlert(token, alertId);
      loadAlerts();
    } catch (err) {
      setAlertsError(err.message);
    }
  }

  async function handleSelectPatient(id) {
    setSelectedPatientId(id);
    setReadings(null);
    setReadingsError("");
    if (!id) return;
    try {
      const data = await api.readingHistory(token, id);
      setReadings(data);
    } catch (err) {
      setReadingsError(err.message);
    }
  }

  const isDoctor = user?.role === "doctor";

  return (
    <div className="min-h-screen bg-[#F4F7FA] text-on-surface">
      <TopNav active="monitoring" />
      <main className="px-gutter md:px-margin-desktop py-stack-lg max-w-container-max mx-auto">
        <div className="mb-stack-md">
          <h1 className="font-headline-lg text-headline-lg text-on-background mb-1">
            Remote Patient Monitoring
          </h1>
          <p className="font-body-sm text-body-sm text-on-surface-variant">
            Live vitals alerts and per-patient reading history.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
          <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
            <div className="p-6 border-b border-[#EEF3F7]">
              <h2 className="font-headline-sm text-headline-sm text-on-background">
                Active Alerts {alerts ? `(${alerts.length})` : ""}
              </h2>
            </div>
            <div className="p-6 space-y-3">
              {alertsError && (
                <p className="font-body-sm text-body-sm text-on-surface-variant">{alertsError}</p>
              )}
              {!alertsError && !alerts && (
                <p className="font-body-sm text-body-sm text-on-surface-variant">Loading…</p>
              )}
              {alerts && alerts.length === 0 && (
                <p className="font-body-sm text-body-sm text-on-surface-variant">No active alerts.</p>
              )}
              {alerts &&
                alerts.map((alert) => {
                  const style = SEVERITY_STYLES[alert.severity] ?? SEVERITY_STYLES.low;
                  return (
                    <div key={alert.id} className={`${style.box} rounded-lg p-4 flex justify-between items-start gap-3`}>
                      <div className="flex gap-3">
                        <span className={`material-symbols-outlined ${style.icon}`}>
                          {alert.severity === "critical" || alert.severity === "high" ? "error" : "warning"}
                        </span>
                        <div>
                          <p className="font-label-sm text-label-sm uppercase tracking-wider mb-1">
                            {style.label} — Patient #{alert.patient_id}
                          </p>
                          <p className="font-body-sm text-body-sm text-on-surface-variant">
                            Status: {alert.status} · {new Date(alert.created_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                      {isDoctor && alert.status !== "acknowledged" && (
                        <button
                          onClick={() => handleAcknowledge(alert.id)}
                          className="font-label-sm text-label-sm text-primary hover:underline whitespace-nowrap"
                        >
                          Acknowledge
                        </button>
                      )}
                    </div>
                  );
                })}
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
            <div className="p-6 border-b border-[#EEF3F7]">
              <h2 className="font-headline-sm text-headline-sm text-on-background mb-3">
                Vitals History
              </h2>
              <select
                value={selectedPatientId}
                onChange={(e) => handleSelectPatient(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
              >
                <option value="">Select a patient…</option>
                {patients?.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.full_name}
                  </option>
                ))}
              </select>
            </div>
            <div className="p-6">
              {readingsError && (
                <p className="font-body-sm text-body-sm text-error">{readingsError}</p>
              )}
              {!selectedPatientId && !readingsError && (
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Select a patient to view their vitals history.
                </p>
              )}
              {selectedPatientId && readings && readings.length === 0 && (
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  No readings recorded for this patient.
                </p>
              )}
              {readings && readings.length > 0 && (
                <table className="w-full">
                  <thead>
                    <tr className="text-left font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wide border-b border-[#EEF3F7]">
                      <th className="py-2">HR</th>
                      <th className="py-2">BP</th>
                      <th className="py-2">SpO2</th>
                      <th className="py-2">Temp</th>
                      <th className="py-2">Glucose</th>
                      <th className="py-2">Recorded</th>
                    </tr>
                  </thead>
                  <tbody>
                    {readings
                      .slice()
                      .reverse()
                      .map((r) => (
                        <tr key={r.id} className="border-b border-[#F1F5F9] last:border-0 font-body-sm text-body-sm">
                          <td className="py-2">{r.heart_rate}</td>
                          <td className="py-2">
                            {r.systolic_bp}/{r.diastolic_bp}
                          </td>
                          <td className="py-2">{r.spo2}%</td>
                          <td className="py-2">{r.temperature}°C</td>
                          <td className="py-2">{r.glucose}</td>
                          <td className="py-2 text-on-surface-variant">
                            {new Date(r.recorded_at).toLocaleString()}
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
