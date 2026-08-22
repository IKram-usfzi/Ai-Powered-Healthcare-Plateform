import { useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import KpiCard from "../components/KpiCard";
import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

function deltaLabel(today, yesterday) {
  const diff = today - yesterday;
  if (diff === 0) return "Same as yesterday";
  return `${diff > 0 ? "+" : ""}${diff} vs yesterday`;
}

export default function DashboardUnified() {
  const { token, user } = useAuth();
  const [overview, setOverview] = useState(null);
  const [error, setError] = useState("");
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    let cancelled = false;
    api
      .dashboardOverview(token)
      .then((data) => !cancelled && setOverview(data))
      .catch((err) => !cancelled && setError(err.message));
    return () => {
      cancelled = true;
    };
  }, [token]);

  async function handleExport() {
    setError("");
    setExporting(true);
    try {
      const report = await api.executiveReport(token);
      const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `globalcare-executive-report-${new Date().toISOString().slice(0, 10)}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setExporting(false);
    }
  }

  const firstName = user?.email?.split("@")[0] ?? "there";

  return (
    <div className="min-h-screen bg-[#F4F7FA]">
      <TopNav active="overview" />
      <main className="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-stack-lg">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-stack-lg gap-4">
          <div>
            <h1 className="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface mb-2">
              Welcome back, {firstName}!
            </h1>
            <p className="font-body-lg text-body-lg text-on-surface-variant">
              Here&apos;s today&apos;s healthcare operations overview.
            </p>
          </div>
          {user?.role === "executive" && (
            <button
              onClick={handleExport}
              disabled={exporting}
              className="bg-surface-container-lowest border border-outline-variant text-on-surface px-4 py-2 rounded-lg font-label-md text-label-md flex items-center gap-2 hover:bg-surface-container-low transition-colors whitespace-nowrap disabled:opacity-60"
            >
              <span className="material-symbols-outlined text-sm">download</span>
              {exporting ? "Exporting…" : "Export Data"}
            </button>
          )}
        </div>

        {error && (
          <p className="font-body-sm text-body-sm text-error mb-4">{error}</p>
        )}

        {!overview ? (
          <p className="font-body-md text-body-md text-on-surface-variant">Loading…</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter">
            <KpiCard
              icon="group"
              label="Total Patients"
              value={overview.total_patients.toLocaleString()}
              deltaLabel={`+${overview.patients_registered_last_7_days} this week`}
            />
            <KpiCard
              icon="calendar_month"
              label="Today's Appointments"
              value={overview.appointments_today.toLocaleString()}
              deltaLabel={deltaLabel(overview.appointments_today, overview.appointments_yesterday)}
            />
            <KpiCard
              icon="monitor_heart"
              label="Active Monitoring"
              value={overview.active_monitoring_patients.toLocaleString()}
              deltaLabel="last 24 hours"
            />
            <KpiCard
              icon="warning"
              label="High Risk Patients"
              value={overview.high_risk_patients.toLocaleString()}
              deltaLabel={`${overview.critical_alerts} critical alerts`}
              accent
            />
          </div>
        )}
      </main>
    </div>
  );
}
