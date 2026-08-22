import { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export default function App() {
  const [apiStatus, setApiStatus] = useState("checking...");

  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then((res) => res.json())
      .then((data) => setApiStatus(data.status))
      .catch(() => setApiStatus("unreachable"));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-2 bg-slate-50">
      <h1 className="font-heading text-2xl font-bold text-slate-900">GlobalCare</h1>
      <p className="text-slate-600">
        Enterprise Remote Healthcare Management Platform — Phase 0 scaffold
      </p>
      <p className="text-sm text-slate-500">Backend API status: {apiStatus}</p>
    </main>
  );
}
