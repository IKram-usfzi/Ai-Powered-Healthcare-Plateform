import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { defaultRouteForRole } from "./defaultRoute";

export default function ProtectedRoute({ roles }) {
  const { user, token, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center font-body-md text-on-surface-variant">
        Loading…
      </div>
    );
  }
  if (!token || !user) return <Navigate to="/login" replace />;
  // Redirect to this role's own default route, not a hardcoded "/dashboard" -
  // some roles (doctor, patient) don't have dashboard access at all, so that
  // would loop right back through this same check.
  if (roles && !roles.includes(user.role)) {
    return <Navigate to={defaultRouteForRole(user.role)} replace />;
  }

  return <Outlet />;
}
