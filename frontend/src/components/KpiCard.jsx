// KPI stat card (docs/UIUX.md §3.5). `deltaLabel` is plain, honest text
// (e.g. "+3 vs yesterday") rather than a fabricated percentage - Phase 6
// only shows numbers this project can actually compute from real data.
export default function KpiCard({ icon, label, value, deltaLabel, accent = false }) {
  return (
    <div className="glass-card flex flex-col justify-between relative overflow-hidden">
      {accent && <div className="absolute top-0 right-0 w-2 h-full bg-error" />}
      <div className="flex justify-between items-start mb-4">
        <div
          className={`w-12 h-12 rounded-full flex items-center justify-center ${
            accent ? "bg-error-container text-error" : "bg-secondary-fixed text-primary"
          }`}
        >
          <span className="material-symbols-outlined">{icon}</span>
        </div>
        {deltaLabel && (
          <span className="bg-surface-container text-on-surface-variant font-label-sm text-label-sm px-2 py-1 rounded-full whitespace-nowrap">
            {deltaLabel}
          </span>
        )}
      </div>
      <div>
        <p className="font-label-md text-label-md text-on-surface-variant mb-1 uppercase tracking-wider">
          {label}
        </p>
        <p className="font-display-kpi text-display-kpi text-on-surface">{value}</p>
      </div>
    </div>
  );
}
