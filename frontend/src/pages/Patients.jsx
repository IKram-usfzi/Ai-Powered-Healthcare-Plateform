import { Fragment, useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

const RISK_PILL_CLASS = {
  critical: "status-pill-high",
  high: "status-pill-high",
  medium: "status-pill-med",
  moderate: "status-pill-med",
  low: "status-pill-low",
};

export default function Patients() {
  const { token } = useAuth();
  const [patients, setPatients] = useState(null);
  const [providers, setProviders] = useState(null);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [expandedId, setExpandedId] = useState(null);
  const [detail, setDetail] = useState(null);
  const [detailError, setDetailError] = useState("");

  useEffect(() => {
    let cancelled = false;
    api
      .listPatients(token)
      .then((data) => !cancelled && setPatients(data))
      .catch((err) => !cancelled && setError(err.message));
    api
      .listProviders(token)
      .then((data) => !cancelled && setProviders(data))
      .catch(() => {
        /* Doctors can't list all providers (admin/executive only) — provider
           name lookup just falls back to showing the id, no crash. */
      });
    return () => {
      cancelled = true;
    };
  }, [token]);

  const providerName = (providerId) => {
    if (!providerId) return "Unassigned";
    const provider = providers?.find((p) => p.id === providerId);
    return provider ? provider.full_name : `Provider #${providerId}`;
  };

  async function toggleExpand(patient) {
    if (expandedId === patient.id) {
      setExpandedId(null);
      return;
    }
    setExpandedId(patient.id);
    setDetail(null);
    setDetailError("");
    try {
      const [readings, consultations, predictions] = await Promise.all([
        api.readingHistory(token, patient.id),
        api.consultationHistory(token, patient.id),
        api.predictionHistory(token, patient.id),
      ]);
      setDetail({ readings, consultations, predictions });
    } catch (err) {
      setDetailError(err.message);
    }
  }

  const filtered = patients
    ? patients.filter((p) => p.full_name.toLowerCase().includes(search.toLowerCase()))
    : [];

  return (
    <div className="min-h-screen bg-[#F4F7FA] text-on-surface">
      <TopNav active="patients" />
      <main className="px-gutter md:px-margin-desktop py-stack-lg max-w-container-max mx-auto">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-stack-md gap-4">
          <div>
            <h1 className="font-headline-lg text-headline-lg text-on-background mb-1">Patients</h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              {patients ? `${patients.length} patient${patients.length === 1 ? "" : "s"}` : "Loading…"}
            </p>
          </div>
          <input
            type="text"
            placeholder="Search by name…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full md:w-72 px-4 py-2 rounded-full border border-[#EEF3F7] bg-white font-body-sm text-body-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
          />
        </div>

        {error && <p className="font-body-sm text-body-sm text-error mb-4">{error}</p>}

        {!patients ? (
          <p className="font-body-md text-body-md text-on-surface-variant">Loading…</p>
        ) : (
          <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="text-left font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wide border-b border-[#EEF3F7]">
                  <th className="py-3 px-6">Name</th>
                  <th className="py-3 px-6">Date of Birth</th>
                  <th className="py-3 px-6">Gender</th>
                  <th className="py-3 px-6">Assigned Provider</th>
                  <th className="py-3 px-6">Registered</th>
                </tr>
              </thead>
              <tbody>
                {filtered.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-6 px-6 text-center font-body-sm text-body-sm text-on-surface-variant">
                      No patients match &quot;{search}&quot;.
                    </td>
                  </tr>
                ) : (
                  filtered.map((p) => (
                    <Fragment key={p.id}>
                      <tr
                        onClick={() => toggleExpand(p)}
                        className="border-b border-[#F1F5F9] last:border-0 cursor-pointer hover:bg-surface-container-low"
                      >
                        <td className="py-3 px-6 font-body-sm text-body-sm font-medium">{p.full_name}</td>
                        <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                          {p.date_of_birth}
                        </td>
                        <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                          {p.gender}
                        </td>
                        <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                          {providerName(p.assigned_provider_id)}
                        </td>
                        <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                          {new Date(p.registered_at).toLocaleDateString()}
                        </td>
                      </tr>
                      {expandedId === p.id && (
                        <tr>
                          <td colSpan={5} className="bg-surface-container-lowest px-6 py-5">
                            {detailError && (
                              <p className="font-body-sm text-body-sm text-error">{detailError}</p>
                            )}
                            {!detail && !detailError && (
                              <p className="font-body-sm text-body-sm text-on-surface-variant">
                                Loading…
                              </p>
                            )}
                            {detail && (
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <div>
                                  <h4 className="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-2">
                                    Recent Vitals ({detail.readings.length})
                                  </h4>
                                  {detail.readings.length === 0 ? (
                                    <p className="font-body-sm text-body-sm text-on-surface-variant">
                                      No readings recorded.
                                    </p>
                                  ) : (
                                    <ul className="space-y-1">
                                      {detail.readings.slice(-3).reverse().map((r) => (
                                        <li key={r.id} className="font-body-sm text-body-sm">
                                          HR {r.heart_rate} · BP {r.systolic_bp}/{r.diastolic_bp} · SpO2{" "}
                                          {r.spo2}% ·{" "}
                                          <span className="text-on-surface-variant">
                                            {new Date(r.recorded_at).toLocaleString()}
                                          </span>
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                                <div>
                                  <h4 className="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-2">
                                    Consultations ({detail.consultations.length})
                                  </h4>
                                  {detail.consultations.length === 0 ? (
                                    <p className="font-body-sm text-body-sm text-on-surface-variant">
                                      None recorded.
                                    </p>
                                  ) : (
                                    <ul className="space-y-1">
                                      {detail.consultations.slice(-3).reverse().map((c) => (
                                        <li key={c.id} className="font-body-sm text-body-sm">
                                          {c.summary}
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                                <div>
                                  <h4 className="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant mb-2">
                                    AI Risk Predictions ({detail.predictions.length})
                                  </h4>
                                  {detail.predictions.length === 0 ? (
                                    <p className="font-body-sm text-body-sm text-on-surface-variant">
                                      None recorded.
                                    </p>
                                  ) : (
                                    <ul className="space-y-1">
                                      {detail.predictions.slice(-3).reverse().map((pr) => (
                                        <li key={pr.id} className="font-body-sm text-body-sm flex items-center gap-2">
                                          <span
                                            className={`px-2 py-0.5 rounded-full text-[11px] uppercase font-semibold ${
                                              RISK_PILL_CLASS[pr.risk_category] ?? "status-pill-low"
                                            }`}
                                          >
                                            {pr.risk_category}
                                          </span>
                                          {(pr.confidence_score * 100).toFixed(0)}% confidence
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              </div>
                            )}
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
