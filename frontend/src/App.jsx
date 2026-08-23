import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import Login from "./pages/Login";
import DashboardUnified from "./pages/DashboardUnified";
import DashboardExecutive from "./pages/DashboardExecutive";
import DashboardOperations from "./pages/DashboardOperations";
import Patients from "./pages/Patients";
import Appointments from "./pages/Appointments";
import Telemedicine from "./pages/Telemedicine";
import Monitoring from "./pages/Monitoring";
import Analytics from "./pages/Analytics";

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

        {/* Module screens (docs/UIUX.md §4) - gated to match each API's own
            role restrictions (api-spec.md), not just the dashboard roles. */}
        <Route element={<ProtectedRoute roles={["administrator", "doctor"]} />}>
          <Route path="/patients" element={<Patients />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="/analytics" element={<Analytics />} />
        </Route>
        <Route element={<ProtectedRoute roles={["administrator", "doctor", "patient"]} />}>
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/telemedicine" element={<Telemedicine />} />
        </Route>

        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </AuthProvider>
  );
}
