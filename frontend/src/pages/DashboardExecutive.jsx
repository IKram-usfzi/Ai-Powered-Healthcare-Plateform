import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

const RISK_BADGE_CLASS = {
  high: "bg-error-container text-error",
  moderate: "bg-surface-variant text-on-surface-variant",
  low: "bg-[#DCFCE7] text-[#166534]",
};
const RISK_PILL_CLASS = {
  high: "status-pill-high",
  moderate: "status-pill-med",
  low: "status-pill-low",
};

function TrendChart({ trends }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!trends || !canvasRef.current) return undefined;

    const labels = trends.days.map((d) =>
      new Date(d.date).toLocaleDateString(undefined, { weekday: "short" })
    );

    chartRef.current?.destroy();
    chartRef.current = new Chart(canvasRef.current.getContext("2d"), {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Vitals Readings (RPM)",
            data: trends.days.map((d) => d.readings_count),
            borderColor: "#0058be",
            backgroundColor: "rgba(0, 88, 190, 0.1)",
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: "#0058be",
            pointBorderColor: "#ffffff",
            pointBorderWidth: 2,
            pointRadius: 4,
          },
          {
            label: "Clinical Alerts",
            data: trends.days.map((d) => d.alerts_count),
            borderColor: "#dfe8ff",
            borderWidth: 2,
            tension: 0.4,
            borderDash: [5, 5],
            pointRadius: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
            align: "end",
            labels: { usePointStyle: true, boxWidth: 8, font: { family: "Inter", size: 12 } },
          },
          tooltip: {
            backgroundColor: "#111c2d",
            titleFont: { family: "Inter", size: 12 },
            bodyFont: { family: "Manrope", size: 14, weight: "bold" },
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
          },
        },
        scales: {
          y: { beginAtZero: true, grid: { color: "#f0f3ff" }, ticks: { maxTicksLimit: 5 } },
          x: { grid: { display: false } },
        },
      },
    });

    return () => chartRef.current?.destroy();
  }, [trends]);

  return <canvas ref={canvasRef} />;
}

export default function DashboardExecutive() {
  const { token } = useAuth();
  const [overview, setOverview] = useState(null);
  const [trends, setTrends] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    Promise.all([api.dashboardOverview(token), api.dashboardTrends(token)])
      .then(([ov, tr]) => {
        if (cancelled) return;
        setOverview(ov);
        setTrends(tr);
      })
      .catch((err) => !cancelled && setError(err.message));
    return () => {
      cancelled = true;
    };
  }, [token]);

  const byStatus = overview?.appointments_today_by_status ?? {};
  const scheduled = byStatus.scheduled ?? 0;
  const completed = byStatus.completed ?? 0;
  const cancelled = byStatus.cancelled ?? 0;

  return (
    <div className="min-h-screen bg-background text-on-background">
      <TopNav active="executive" />
      <main className="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-8 md:py-12 flex flex-col gap-stack-lg">
        {error && <p className="font-body-sm text-body-sm text-error">{error}</p>}

        {!overview || !trends ? (
          <p className="font-body-md text-body-md text-on-surface-variant">Loading…</p>
        ) : (
          <>
            <section aria-label="Key Performance Indicators" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter">
              <div className="glass-card flex flex-col gap-2 relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Total Patients</h3>
                  <span className="material-symbols-outlined text-primary bg-primary-fixed p-2 rounded-full">
                    monitoring
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background mt-4">
                  {overview.total_patients.toLocaleString()}
                </div>
                <div className="font-body-sm text-body-sm text-outline mt-1">
                  +{overview.patients_registered_last_7_days} registered this week
                </div>
              </div>
              <div className="glass-card flex flex-col gap-2">
                <div className="flex justify-between items-start">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Active Providers</h3>
                  <span className="material-symbols-outlined text-secondary bg-secondary-fixed p-2 rounded-full">
                    groups
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background mt-4">
                  {overview.active_monitoring_patients.toLocaleString()}
                </div>
                <div className="font-body-sm text-body-sm text-outline mt-1">
                  patients under active remote monitoring
                </div>
              </div>
              <div className="glass-card flex flex-col gap-2">
                <div className="flex justify-between items-start">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">Open Alerts</h3>
                  <span className="material-symbols-outlined text-error bg-error-container p-2 rounded-full">
                    notifications_active
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background mt-4">
                  {overview.open_alerts.toLocaleString()}
                </div>
                <div className="font-body-sm text-body-sm text-outline mt-1 flex items-center gap-1">
                  <span className="text-error font-medium">{overview.critical_alerts} Critical</span>
                  require action
                </div>
              </div>
              <div className="glass-card flex flex-col gap-2">
                <div className="flex justify-between items-start">
                  <h3 className="font-headline-sm text-headline-sm text-on-surface">AI Risk Alerts</h3>
                  <span className="material-symbols-outlined text-tertiary bg-tertiary-fixed p-2 rounded-full">
                    psychology
                  </span>
                </div>
                <div className="font-display-kpi text-display-kpi text-on-background mt-4">
                  {overview.high_risk_patients.toLocaleString()}
                </div>
                <div className="font-body-sm text-body-sm text-outline mt-1">
                  Flagged for review by the AI risk classifier
                </div>
              </div>
            </section>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
              <section aria-label="Clinical Activity Trend" className="lg:col-span-8 glass-card flex flex-col">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="font-headline-md text-headline-md text-on-surface">
                      Clinical Activity &amp; RPM
                    </h2>
                    <p className="font-body-md text-body-md text-outline">
                      Facility-wide vitals monitoring, last 7 days
                    </p>
                  </div>
                </div>
                <div className="flex-grow relative h-72 w-full mt-4">
                  <TrendChart trends={trends} />
                </div>
              </section>

              <section aria-label="AI Health Risk Assessment" className="lg:col-span-4 glass-card flex flex-col">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="font-headline-md text-headline-md text-on-surface">AI Risk Assessment</h2>
                </div>
                {overview.top_risk_patients.length === 0 ? (
                  <p className="font-body-sm text-body-sm text-outline">
                    No patients currently flagged as high risk.
                  </p>
                ) : (
                  <div className="flex flex-col gap-4 overflow-y-auto pr-2" style={{ maxHeight: 400 }}>
                    {overview.top_risk_patients.map((p) => (
                      <div
                        key={p.patient_id}
                        className="bg-surface border border-surface-container rounded-xl p-4 flex items-center justify-between"
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`h-10 w-10 rounded-full flex items-center justify-center font-bold ${RISK_BADGE_CLASS[p.risk_category]}`}
                          >
                            {Math.round(p.confidence_score * 100)}
                          </div>
                          <div>
                            <h4 className="font-headline-sm text-body-md font-bold text-on-surface">
                              {p.full_name}
                            </h4>
                          </div>
                        </div>
                        <span className={RISK_PILL_CLASS[p.risk_category]}>{p.risk_category}</span>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </div>

            <section aria-label="Operational Efficiency">
              <h2 className="font-headline-lg text-headline-lg text-on-surface mb-6">
                Operational Efficiency
              </h2>
              <div className="glass-card">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-headline-md text-headline-md text-on-surface">
                      Appointment Scheduling
                    </h3>
                    <p className="font-body-sm text-body-sm text-outline mt-1">
                      Today&apos;s throughput status
                    </p>
                  </div>
                  <span className="material-symbols-outlined text-secondary bg-secondary-fixed p-2 rounded-full">
                    calendar_today
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4 mt-4">
                  <div className="bg-surface p-4 rounded-xl border border-surface-container">
                    <div className="font-body-sm text-label-sm text-outline uppercase tracking-wide">
                      Scheduled
                    </div>
                    <div className="font-headline-lg text-headline-lg text-on-background mt-1">
                      {scheduled}
                    </div>
                  </div>
                  <div className="bg-surface p-4 rounded-xl border border-surface-container">
                    <div className="font-body-sm text-label-sm text-outline uppercase tracking-wide">
                      Completed
                    </div>
                    <div className="font-headline-lg text-headline-lg text-on-background mt-1">
                      {completed}
                    </div>
                  </div>
                  <div className="bg-surface p-4 rounded-xl border border-surface-container border-l-4 border-l-error">
                    <div className="font-body-sm text-label-sm text-error uppercase tracking-wide">
                      Cancelled
                    </div>
                    <div className="font-headline-lg text-headline-lg text-error mt-1">
                      {cancelled}
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}
