import { useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api } from "../api/client";

export default function Telemedicine() {
  const { token, user } = useAuth();
  const [appointments, setAppointments] = useState(null);
  const [patients, setPatients] = useState(null);
  const [error, setError] = useState("");
  const [openFormFor, setOpenFormFor] = useState(null);
  const [form, setForm] = useState({ summary: "", recommendations: "" });
  const [formError, setFormError] = useState("");

  function load() {
    api
      .listAppointments(token)
      .then(setAppointments)
      .catch((err) => setError(err.message));
  }

  useEffect(() => {
    load();
    api.listPatients(token).then(setPatients).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const patientName = (id) => patients?.find((p) => p.id === id)?.full_name ?? `Patient #${id}`;

  const pending = appointments
    ? appointments
        .filter((a) => a.status === "scheduled" || a.status === "in_progress")
        .sort((a, b) => new Date(a.scheduled_at) - new Date(b.scheduled_at))
    : [];
  const completed = appointments ? appointments.filter((a) => a.status === "completed") : [];

  async function handleRecord(e, appointmentId) {
    e.preventDefault();
    setFormError("");
    try {
      await api.createConsultation(token, {
        appointment_id: appointmentId,
        summary: form.summary,
        recommendations: form.recommendations,
      });
      setOpenFormFor(null);
      setForm({ summary: "", recommendations: "" });
      load();
    } catch (err) {
      setFormError(err.message);
    }
  }

  const isDoctor = user?.role === "doctor";

  return (
    <div className="min-h-screen bg-[#F4F7FA] text-on-surface">
      <TopNav active="telemedicine" />
      <main className="px-gutter md:px-margin-desktop py-stack-lg max-w-container-max mx-auto">
        <div className="mb-stack-md">
          <h1 className="font-headline-lg text-headline-lg text-on-background mb-1">Telemedicine</h1>
          <p className="font-body-sm text-body-sm text-on-surface-variant">
            Consultation queue and history — real appointment/consultation data, no simulated video-call UI.
          </p>
        </div>

        {error && <p className="font-body-sm text-body-sm text-error mb-4">{error}</p>}

        {!appointments ? (
          <p className="font-body-md text-body-md text-on-surface-variant">Loading…</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
            <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
              <div className="p-6 border-b border-[#EEF3F7]">
                <h2 className="font-headline-sm text-headline-sm text-on-background">
                  Awaiting Consultation ({pending.length})
                </h2>
              </div>
              <div className="p-6 space-y-4">
                {pending.length === 0 && (
                  <p className="font-body-sm text-body-sm text-on-surface-variant">
                    Nothing pending.
                  </p>
                )}
                {pending.map((a) => (
                  <div key={a.id} className="border border-[#EEF3F7] rounded-xl p-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-body-sm text-body-sm font-medium">
                          {patients ? patientName(a.patient_id) : `Patient #${a.patient_id}`}
                        </p>
                        <p className="font-label-sm text-label-sm text-on-surface-variant">
                          {new Date(a.scheduled_at).toLocaleString()} · {a.status.replace("_", " ")}
                        </p>
                      </div>
                      {isDoctor && (
                        <button
                          onClick={() => {
                            setOpenFormFor(openFormFor === a.id ? null : a.id);
                            setFormError("");
                          }}
                          className="font-label-sm text-label-sm text-primary hover:underline"
                        >
                          {openFormFor === a.id ? "Cancel" : "Record Consultation"}
                        </button>
                      )}
                    </div>
                    {openFormFor === a.id && (
                      <form onSubmit={(e) => handleRecord(e, a.id)} className="mt-4 space-y-2">
                        <textarea
                          required
                          placeholder="Summary"
                          value={form.summary}
                          onChange={(e) => setForm({ ...form, summary: e.target.value })}
                          className="w-full px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
                          rows={2}
                        />
                        <textarea
                          required
                          placeholder="Recommendations"
                          value={form.recommendations}
                          onChange={(e) => setForm({ ...form, recommendations: e.target.value })}
                          className="w-full px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
                          rows={2}
                        />
                        {formError && (
                          <p className="font-body-sm text-body-sm text-error">{formError}</p>
                        )}
                        <button
                          type="submit"
                          className="bg-primary text-on-primary font-label-md text-label-md px-4 py-2 rounded-full hover:opacity-90 transition-opacity"
                        >
                          Save Consultation
                        </button>
                      </form>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
              <div className="p-6 border-b border-[#EEF3F7]">
                <h2 className="font-headline-sm text-headline-sm text-on-background">
                  Completed ({completed.length})
                </h2>
              </div>
              <div className="p-6 space-y-3">
                {completed.length === 0 && (
                  <p className="font-body-sm text-body-sm text-on-surface-variant">None yet.</p>
                )}
                {completed
                  .sort((a, b) => new Date(b.scheduled_at) - new Date(a.scheduled_at))
                  .map((a) => (
                    <div key={a.id} className="flex justify-between items-center border-b border-[#F1F5F9] last:border-0 pb-3 last:pb-0">
                      <div>
                        <p className="font-body-sm text-body-sm font-medium">
                          {patients ? patientName(a.patient_id) : `Patient #${a.patient_id}`}
                        </p>
                        <p className="font-label-sm text-label-sm text-on-surface-variant">
                          {new Date(a.scheduled_at).toLocaleDateString()}
                        </p>
                      </div>
                      <span className="status-pill-low px-2.5 py-1 rounded-full text-[11px] uppercase font-semibold">
                        Completed
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
