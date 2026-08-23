import { useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

const RISK_PILL_CLASS = {
  high: "status-pill-high",
  moderate: "status-pill-med",
  low: "status-pill-low",
};

export default function Analytics() {
  const { token, user } = useAuth();
  const [metadata, setMetadata] = useState(null);
  const [metadataError, setMetadataError] = useState("");
  const [patients, setPatients] = useState(null);
  const [selectedPatientId, setSelectedPatientId] = useState("");
  const [predictions, setPredictions] = useState(null);
  const [predictionsError, setPredictionsError] = useState("");
  const [assessing, setAssessing] = useState(false);
  const [assessError, setAssessError] = useState("");

  useEffect(() => {
    api
      .modelMetadata(token)
      .then(setMetadata)
      .catch((err) => setMetadataError(err.message));
    api.listPatients(token).then(setPatients).catch(() => {});
  }, [token]);

  async function loadPredictions(patientId) {
    setSelectedPatientId(patientId);
    setPredictions(null);
    setPredictionsError("");
    if (!patientId) return;
    try {
      const data = await api.predictionHistory(token, patientId);
      setPredictions(data);
    } catch (err) {
      setPredictionsError(err.message);
    }
  }

  async function handleRunAssessment() {
    setAssessError("");
    setAssessing(true);
    try {
      await api.runRiskAssessment(token, Number(selectedPatientId));
      await loadPredictions(selectedPatientId);
    } catch (err) {
      setAssessError(err.message);
    } finally {
      setAssessing(false);
    }
  }

  const isDoctor = user?.role === "doctor";

  return (
    <div className="min-h-screen bg-[#F4F7FA] text-on-surface">
      <TopNav active="analytics" />
      <main className="px-gutter md:px-margin-desktop py-stack-lg max-w-container-max mx-auto">
        <div className="mb-stack-md">
          <h1 className="font-headline-lg text-headline-lg text-on-background mb-1">
            Analytics &amp; AI Risk Assessment
          </h1>
          <p className="font-body-sm text-body-sm text-on-surface-variant">
            Real model performance and per-patient risk predictions — no fabricated metrics.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
          <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] p-6">
            <h2 className="font-headline-sm text-headline-sm text-on-background mb-4">
              Model Performance
            </h2>
            {metadataError && (
              <p className="font-body-sm text-body-sm text-on-surface-variant">
                Model metadata requires Administrator access.
              </p>
            )}
            {!metadata && !metadataError && (
              <p className="font-body-sm text-body-sm text-on-surface-variant">Loading…</p>
            )}
            {metadata && (
              <div className="space-y-3">
                <p className="font-body-sm text-body-sm">
                  <span className="text-on-surface-variant">Algorithm:</span> {metadata.algorithm} (
                  {metadata.model_version})
                </p>
                <p className="font-body-sm text-body-sm">
                  <span className="text-on-surface-variant">Trained on:</span> {metadata.n_samples}{" "}
                  readings ({metadata.n_train} train / {metadata.n_test} test)
                </p>
                <div className="grid grid-cols-4 gap-3 pt-2">
                  {[
                    ["Accuracy", metadata.accuracy],
                    ["Precision", metadata.precision_macro],
                    ["Recall", metadata.recall_macro],
                    ["F1", metadata.f1_macro],
                  ].map(([label, value]) => (
                    <div key={label} className="bg-surface-container-lowest rounded-lg p-3 text-center">
                      <p className="font-display-kpi text-headline-sm text-on-background">
                        {(value * 100).toFixed(1)}%
                      </p>
                      <p className="font-label-sm text-label-sm text-on-surface-variant uppercase">
                        {label}
                      </p>
                    </div>
                  ))}
                </div>
                <p className="font-label-sm text-label-sm text-on-surface-variant pt-1">
                  Label distribution: {Object.entries(metadata.label_distribution).map(([k, v]) => `${k}: ${v}`).join(" · ")}
                </p>
              </div>
            )}
          </div>

          <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] p-6">
            <h2 className="font-headline-sm text-headline-sm text-on-background mb-4">
              Patient Risk Predictions
            </h2>
            <select
              value={selectedPatientId}
              onChange={(e) => loadPredictions(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm mb-4"
            >
              <option value="">Select a patient…</option>
              {patients?.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.full_name}
                </option>
              ))}
            </select>

            {isDoctor && selectedPatientId && (
              <button
                onClick={handleRunAssessment}
                disabled={assessing}
                className="mb-4 bg-primary text-on-primary font-label-md text-label-md px-4 py-2 rounded-full hover:opacity-90 transition-opacity disabled:opacity-50"
              >
                {assessing ? "Running…" : "Run New Assessment"}
              </button>
            )}
            {assessError && <p className="font-body-sm text-body-sm text-error mb-3">{assessError}</p>}

            {predictionsError && (
              <p className="font-body-sm text-body-sm text-error">{predictionsError}</p>
            )}
            {predictions && predictions.length === 0 && (
              <p className="font-body-sm text-body-sm text-on-surface-variant">
                No predictions recorded for this patient yet.
              </p>
            )}
            {predictions && predictions.length > 0 && (
              <ul className="space-y-2">
                {predictions
                  .slice()
                  .reverse()
                  .map((pr) => (
                    <li
                      key={pr.id}
                      className="flex items-center justify-between border border-[#EEF3F7] rounded-lg p-3"
                    >
                      <div>
                        <span
                          className={`px-2.5 py-1 rounded-full text-[11px] uppercase font-semibold mr-2 ${
                            RISK_PILL_CLASS[pr.risk_category] ?? "status-pill-low"
                          }`}
                        >
                          {pr.risk_category}
                        </span>
                        <span className="font-body-sm text-body-sm text-on-surface-variant">
                          {(pr.confidence_score * 100).toFixed(0)}% confidence
                        </span>
                      </div>
                      <span className="font-label-sm text-label-sm text-on-surface-variant">
                        {new Date(pr.created_at).toLocaleDateString()}
                      </span>
                    </li>
                  ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
