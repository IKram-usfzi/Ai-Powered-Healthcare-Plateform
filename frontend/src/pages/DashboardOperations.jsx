import { useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api, ApiError } from "../api/client";

const SEVERITY_STYLES = {
  critical: {
    box: "bg-[#FEF2F2] border border-[#FECACA]",
    icon: "text-error",
    title: "text-[#991B1B]",
    body: "text-[#7F1D1D]",
    label: "Critical",
  },
  high: {
    box: "bg-[#FEF2F2] border border-[#FECACA]",
    icon: "text-error",
    title: "text-[#991B1B]",
    body: "text-[#7F1D1D]",
    label: "High",
  },
  medium: {
    box: "bg-[#FFFBEB] border border-[#FDE68A]",
    icon: "text-[#D97706]",
    title: "text-[#92400E]",
    body: "text-[#78350F]",
    label: "Warning",
  },
  low: {
    box: "bg-surface-container-low border border-inverse-primary",
    icon: "text-primary",
    title: "text-on-primary-fixed-variant",
    body: "text-on-primary-fixed",
    label: "Info",
  },
};

export default function DashboardOperations() {
  const { token } = useAuth();
  const [overview, setOverview] = useState(null);
  const [providers, setProviders] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [alertsError, setAlertsError] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    api
      .dashboardOverview(token)
      .then((data) => !cancelled && setOverview(data))
      .catch((err) => !cancelled && setError(err.message));
    api
      .providerActivity(token)
      .then((data) => !cancelled && setProviders(data))
      .catch((err) => !cancelled && setError(err.message));
    api
      .listAlerts(token)
      .then((data) => !cancelled && setAlerts(data))
      .catch((err) => {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 403) {
          setAlertsError("Alert details require Administrator or Doctor access.");
        } else {
          setAlertsError(err.message);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [token]);

  const busiestProviders = providers
    ? [...providers].sort((a, b) => b.appointments_today - a.appointments_today).slice(0, 8)
    : [];

  return (
    <div className="min-h-screen bg-[#F4F7FA] text-on-surface">
      <TopNav active="operations" />
      <main className="px-gutter md:px-margin-desktop py-stack-lg max-w-container-max mx-auto">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-stack-md gap-4">
          <div>
            <h1 className="font-headline-lg text-headline-lg text-on-background mb-1">
              Healthcare Operations
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              Live clinical deployment and resource tracking.
            </p>
          </div>
        </div>

        {error && <p className="font-body-sm text-body-sm text-error mb-4">{error}</p>}

        {!overview || !providers ? (
          <p className="font-body-md text-body-md text-on-surface-variant">Loading…</p>
        ) : (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-gutter mb-stack-md">
              <div className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7]">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined text-[18px]">event</span>
                  </div>
                  <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">
                    Appointments Today
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background">
                  {overview.appointments_today}
                </div>
              </div>
              <div className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7]">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 rounded-full bg-[#DCFCE7] flex items-center justify-center text-[#166534]">
                    <span className="material-symbols-outlined text-[18px]">check_circle</span>
                  </div>
                  <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">
                    Completed
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background">
                  {overview.appointments_today_by_status?.completed ?? 0}
                </div>
              </div>
              <div className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-error-container">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 rounded-full bg-error-container flex items-center justify-center text-error">
                    <span className="material-symbols-outlined text-[18px]">warning</span>
                  </div>
                  <span className="font-label-md text-label-md text-error uppercase tracking-wider">
                    At-Risk Cases
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background">
                  {overview.high_risk_patients}
                </div>
              </div>
              <div className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7]">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined text-[18px]">groups</span>
                  </div>
                  <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">
                    Providers
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background">
                  {providers.length}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
              <div className="lg:col-span-8 xl:col-span-9 space-y-gutter">
                <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
                  <div className="p-6 border-b border-[#EEF3F7] flex justify-between items-center">
                    <h2 className="font-headline-sm text-headline-sm text-on-background">
                      Busiest Providers Today
                    </h2>
                    <p className="font-label-sm text-label-sm text-on-surface-variant">
                      by appointment count
                    </p>
                  </div>
                  <table className="w-full">
                    <thead>
                      <tr className="text-left font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wide border-b border-[#EEF3F7]">
                        <th className="py-3 px-6">Provider</th>
                        <th className="py-3 px-6">Specialty</th>
                        <th className="py-3 px-6">Facility</th>
                        <th className="py-3 px-6 text-right">Today</th>
                        <th className="py-3 px-6 text-right">Next 7 Days</th>
                        <th className="py-3 px-6 text-right">Assigned Patients</th>
                      </tr>
                    </thead>
                    <tbody>
                      {busiestProviders.length === 0 ? (
                        <tr>
                          <td colSpan={6} className="py-6 px-6 text-center font-body-sm text-body-sm text-on-surface-variant">
                            No appointments scheduled today.
                          </td>
                        </tr>
                      ) : (
                        busiestProviders.map((p) => (
                          <tr key={p.provider_id} className="border-b border-[#F1F5F9] last:border-0">
                            <td className="py-3 px-6 font-body-sm text-body-sm font-medium">{p.full_name}</td>
                            <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                              {p.specialty}
                            </td>
                            <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                              {p.facility_name}
                            </td>
                            <td className="py-3 px-6 font-body-sm text-body-sm text-right">
                              {p.appointments_today}
                            </td>
                            <td className="py-3 px-6 font-body-sm text-body-sm text-right">
                              {p.upcoming_appointments_7_days}
                            </td>
                            <td className="py-3 px-6 font-body-sm text-body-sm text-right">
                              {p.assigned_patients}
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="lg:col-span-4 xl:col-span-3 space-y-gutter flex flex-col">
                <div className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7]">
                  <h3 className="font-headline-sm text-headline-sm text-on-background mb-4">
                    Important Alerts
                  </h3>
                  {alertsError && (
                    <p className="font-body-sm text-body-sm text-on-surface-variant">{alertsError}</p>
                  )}
                  {!alertsError && !alerts && (
                    <p className="font-body-sm text-body-sm text-on-surface-variant">Loading…</p>
                  )}
                  {alerts && alerts.length === 0 && (
                    <p className="font-body-sm text-body-sm text-on-surface-variant">
                      No active alerts.
                    </p>
                  )}
                  {alerts && alerts.length > 0 && (
                    <div className="space-y-3">
                      {alerts.slice(0, 6).map((alert) => {
                        const style = SEVERITY_STYLES[alert.severity] ?? SEVERITY_STYLES.low;
                        return (
                          <div key={alert.id} className={`${style.box} rounded-lg p-3 flex gap-3 items-start`}>
                            <span className={`material-symbols-outlined mt-0.5 ${style.icon}`}>
                              {alert.severity === "critical" || alert.severity === "high"
                                ? "error"
                                : "warning"}
                            </span>
                            <div>
                              <h4 className={`font-label-sm text-label-sm uppercase tracking-wider mb-1 ${style.title}`}>
                                {style.label} — Patient #{alert.patient_id}
                              </h4>
                              <p className={`font-body-sm text-body-sm ${style.body}`}>
                                Abnormal reading recorded, status: {alert.status}.
                              </p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                <div className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] flex-1">
                  <h3 className="font-headline-sm text-headline-sm text-on-background mb-4">
                    Provider Roster
                  </h3>
                  <div className="space-y-4">
                    {providers.slice(0, 6).map((p) => (
                      <div key={p.provider_id} className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center text-primary font-bold text-sm">
                            {p.full_name
                              .split(" ")
                              .map((n) => n[0])
                              .join("")
                              .slice(0, 2)}
                          </div>
                          <div>
                            <div className="font-body-sm text-body-sm font-medium text-on-background">
                              {p.full_name}
                            </div>
                            <div className="font-label-sm text-label-sm text-on-surface-variant">
                              {p.specialty} • {p.assigned_patients} patients
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
