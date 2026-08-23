import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

// docs/UIUX.md §4 module screens, promoted from inert placeholders to real
// routes. `roles` mirrors each route's own ProtectedRoute gate in App.jsx -
// kept in sync here so the nav never shows a link a role would just get
// bounced back from.
const MODULE_LINKS = [
  { label: "Patients", to: "/patients", key: "patients", roles: ["administrator", "doctor"] },
  {
    label: "Appointments",
    to: "/appointments",
    key: "appointments",
    roles: ["administrator", "doctor", "patient"],
  },
  {
    label: "Telemedicine",
    to: "/telemedicine",
    key: "telemedicine",
    roles: ["administrator", "doctor", "patient"],
  },
  { label: "Monitoring", to: "/monitoring", key: "monitoring", roles: ["administrator", "doctor"] },
  { label: "Analytics", to: "/analytics", key: "analytics", roles: ["administrator", "doctor"] },
];

export default function TopNav({ active }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const visibleLinks = MODULE_LINKS.filter((link) => link.roles.includes(user?.role));
  const canSeeOverview = user?.role === "administrator" || user?.role === "executive";
  const canSeeExecutive = user?.role === "executive";
  const canSeeOperations = user?.role === "administrator" || user?.role === "executive";

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const pill = (isActive) =>
    `px-4 py-1.5 rounded-full font-label-md text-label-md transition-colors whitespace-nowrap ${
      isActive
        ? "bg-on-surface text-on-primary"
        : "text-on-surface-variant hover:bg-surface-container-low"
    }`;

  return (
    <header className="bg-surface-container-lowest shadow-[0px_4px_20px_rgba(0,0,0,0.03)] sticky top-0 z-50">
      <div className="flex justify-between items-center w-full px-6 md:px-margin-desktop h-16 max-w-container-max mx-auto gap-4">
        <div className="flex items-center gap-8 min-w-0">
          <div className="text-headline-sm font-headline-sm font-bold text-on-surface shrink-0">
            GlobalCare
          </div>
          <nav className="hidden md:flex items-center gap-1 overflow-x-auto">
            {canSeeOverview && (
              <Link to="/dashboard" className={pill(active === "overview")}>
                Overview
              </Link>
            )}
            {visibleLinks.map(({ label, to, key }) => (
              <Link key={key} to={to} className={pill(active === key)}>
                {label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {canSeeExecutive && (
            <Link
              to="/dashboard/executive"
              className={`hidden sm:inline-block px-4 py-2 rounded-full font-label-md text-label-md transition-colors ${
                active === "executive"
                  ? "bg-primary text-on-primary shadow-sm"
                  : "bg-surface-container text-on-surface hover:bg-surface-container-high"
              }`}
            >
              Executive
            </Link>
          )}
          {canSeeOperations && (
            <Link
              to="/dashboard/operations"
              className={`hidden sm:inline-block px-4 py-2 rounded-full font-label-md text-label-md transition-colors ${
                active === "operations"
                  ? "bg-primary text-on-primary shadow-sm"
                  : "bg-surface-container text-on-surface hover:bg-surface-container-high"
              }`}
            >
              Operations
            </Link>
          )}
          <div className="flex items-center gap-2 border-l border-outline-variant pl-3 ml-1">
            <div className="text-right hidden lg:block">
              <p className="font-label-sm text-label-sm text-on-surface font-semibold truncate max-w-[160px]">
                {user?.email}
              </p>
              <p className="font-label-sm text-[10px] text-on-surface-variant capitalize">
                {user?.role}
              </p>
            </div>
            <button
              onClick={handleLogout}
              aria-label="Log out"
              className="text-on-surface-variant hover:text-error hover:bg-surface-container-low transition-colors p-2 rounded-full"
            >
              <span className="material-symbols-outlined text-[20px]">logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
