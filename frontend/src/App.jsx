import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import Login from "./pages/Login";
import DashboardUnified from "./pages/DashboardUnified";
import DashboardExecutive from "./pages/DashboardExecutive";
import DashboardOperations from "./pages/DashboardOperations";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute roles={["administrator", "executive"]} />}>
          <Route path="/dashboard" element={<DashboardUnified />} />
          <Route path="/dashboard/operations" element={<DashboardOperations />} />
        </Route>

        <Route element={<ProtectedRoute roles={["executive"]} />}>
          <Route path="/dashboard/executive" element={<DashboardExecutive />} />
        </Route>

        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </AuthProvider>
  );
}
