import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

// Placeholder nav items for screens outside Phase 6's scope (docs/UIUX.md §4) -
// inert, matching the supplied template's own href="#" placeholders.
const PLACEHOLDER_LINKS = ["Patients", "Appointments", "Telemedicine", "Monitoring", "Analytics"];

export default function TopNav({ active }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

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
            <Link to="/dashboard" className={pill(active === "overview")}>
              Overview
            </Link>
            {PLACEHOLDER_LINKS.map((label) => (
              <a
                key={label}
                href="#"
                onClick={(e) => e.preventDefault()}
                className={pill(false)}
              >
                {label}
              </a>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-2 shrink-0">
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
