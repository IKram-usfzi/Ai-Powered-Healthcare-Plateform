// Where to land a user after login, or where ProtectedRoute sends them when
// they're denied a route their role can't access. Must never point at a
// route the same role is itself denied - that would create a redirect loop
// (patients don't have dashboard access, so "always send to /dashboard" is
// wrong for them).
export function defaultRouteForRole(role) {
  if (role === "executive") return "/dashboard/executive";
  if (role === "administrator") return "/dashboard";
  // Doctor has no dashboard access (App.jsx gates /dashboard to
  // administrator/executive only) - land on their patient list instead.
  if (role === "doctor") return "/patients";
  if (role === "patient") return "/appointments";
  return "/login";
}
