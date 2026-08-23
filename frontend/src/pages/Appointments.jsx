import { useEffect, useState } from "react";
import TopNav from "../components/TopNav";
import { useAuth } from "../auth/AuthContext";
import { api, ApiError } from "../api/client";

const STATUS_OPTIONS = ["scheduled", "in_progress", "completed", "cancelled"];

const STATUS_PILL = {
  scheduled: "bg-[#EFF6FF] text-[#1D4ED8]",
  in_progress: "bg-[#FFFBEB] text-[#92400E]",
  completed: "bg-[#DCFCE7] text-[#166534]",
  cancelled: "bg-[#F1F5F9] text-[#64748B]",
};

export default function Appointments() {
  const { token, user } = useAuth();
  const [appointments, setAppointments] = useState(null);
  const [patients, setPatients] = useState(null);
  const [providers, setProviders] = useState(null);
  const [error, setError] = useState("");
  const [showBookForm, setShowBookForm] = useState(false);
  const [bookError, setBookError] = useState("");
  const [form, setForm] = useState({ provider_id: "", scheduled_at: "", patient_id: "" });

  function load() {
    api
      .listAppointments(token)
      .then(setAppointments)
      .catch((err) => setError(err.message));
  }

  useEffect(() => {
    load();
    api.listPatients(token).then(setPatients).catch(() => {});
    api.listProviders(token).then(setProviders).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const patientName = (id) => patients?.find((p) => p.id === id)?.full_name ?? `Patient #${id}`;
  const providerName = (id) => providers?.find((p) => p.id === id)?.full_name ?? `Provider #${id}`;

  async function handleStatusChange(appointmentId, newStatus) {
    try {
      await api.updateAppointmentStatus(token, appointmentId, newStatus);
      load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to update status");
    }
  }

  async function handleBook(e) {
    e.preventDefault();
    setBookError("");
    try {
      const body = {
        provider_id: Number(form.provider_id),
        scheduled_at: new Date(form.scheduled_at).toISOString(),
      };
      if (user.role === "administrator") body.patient_id = Number(form.patient_id);
      await api.createAppointment(token, body);
      setShowBookForm(false);
      setForm({ provider_id: "", scheduled_at: "", patient_id: "" });
      load();
    } catch (err) {
      setBookError(err.message);
    }
  }

  const canBook = user?.role === "patient" || user?.role === "administrator";
  const canUpdateStatus = user?.role === "doctor" || user?.role === "administrator";

  return (
    <div className="min-h-screen bg-[#F4F7FA] text-on-surface">
      <TopNav active="appointments" />
      <main className="px-gutter md:px-margin-desktop py-stack-lg max-w-container-max mx-auto">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-stack-md gap-4">
          <div>
            <h1 className="font-headline-lg text-headline-lg text-on-background mb-1">
              Appointments
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              {appointments
                ? `${appointments.length} appointment${appointments.length === 1 ? "" : "s"}`
                : "Loading…"}
            </p>
          </div>
          {canBook && (
            <button
              onClick={() => setShowBookForm((v) => !v)}
              className="bg-primary text-on-primary font-label-md text-label-md px-5 py-2.5 rounded-full hover:opacity-90 transition-opacity self-start"
            >
              {showBookForm ? "Cancel" : "+ Book Appointment"}
            </button>
          )}
        </div>

        {showBookForm && (
          <form
            onSubmit={handleBook}
            className="bg-white rounded-2xl p-6 shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] mb-stack-md grid grid-cols-1 md:grid-cols-4 gap-4 items-end"
          >
            {user.role === "administrator" && (
              <label className="flex flex-col gap-1">
                <span className="font-label-sm text-label-sm text-on-surface-variant">Patient</span>
                <select
                  required
                  value={form.patient_id}
                  onChange={(e) => setForm({ ...form, patient_id: e.target.value })}
                  className="px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
                >
                  <option value="">Select…</option>
                  {patients?.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name}
                    </option>
                  ))}
                </select>
              </label>
            )}
            <label className="flex flex-col gap-1">
              <span className="font-label-sm text-label-sm text-on-surface-variant">Provider</span>
              {providers ? (
                <select
                  required
                  value={form.provider_id}
                  onChange={(e) => setForm({ ...form, provider_id: e.target.value })}
                  className="px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
                >
                  <option value="">Select…</option>
                  {providers.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name} — {p.specialty}
                    </option>
                  ))}
                </select>
              ) : (
                // GET /providers is Administrator/Executive only (api-spec.md §3) - a
                // patient has no directory to pick from, so this falls back to an ID
                // input rather than fabricating a provider list.
                <input
                  required
                  type="number"
                  min="1"
                  placeholder="Provider ID (ask your care team)"
                  value={form.provider_id}
                  onChange={(e) => setForm({ ...form, provider_id: e.target.value })}
                  className="px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
                />
              )}
            </label>
            <label className="flex flex-col gap-1">
              <span className="font-label-sm text-label-sm text-on-surface-variant">Date &amp; Time</span>
              <input
                required
                type="datetime-local"
                value={form.scheduled_at}
                onChange={(e) => setForm({ ...form, scheduled_at: e.target.value })}
                className="px-3 py-2 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
              />
            </label>
            <button
              type="submit"
              className="bg-primary text-on-primary font-label-md text-label-md px-5 py-2.5 rounded-full hover:opacity-90 transition-opacity"
            >
              Confirm Booking
            </button>
            {bookError && (
              <p className="md:col-span-4 font-body-sm text-body-sm text-error">{bookError}</p>
            )}
          </form>
        )}

        {error && <p className="font-body-sm text-body-sm text-error mb-4">{error}</p>}

        {!appointments ? (
          <p className="font-body-md text-body-md text-on-surface-variant">Loading…</p>
        ) : (
          <div className="bg-white rounded-2xl shadow-[0px_4px_20px_rgba(0,0,0,0.03)] border border-[#EEF3F7] overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="text-left font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wide border-b border-[#EEF3F7]">
                  <th className="py-3 px-6">Patient</th>
                  <th className="py-3 px-6">Provider</th>
                  <th className="py-3 px-6">Scheduled</th>
                  <th className="py-3 px-6">Status</th>
                  {canUpdateStatus && <th className="py-3 px-6">Update</th>}
                </tr>
              </thead>
              <tbody>
                {appointments.length === 0 ? (
                  <tr>
                    <td
                      colSpan={canUpdateStatus ? 5 : 4}
                      className="py-6 px-6 text-center font-body-sm text-body-sm text-on-surface-variant"
                    >
                      No appointments.
                    </td>
                  </tr>
                ) : (
                  appointments.map((a) => (
                    <tr key={a.id} className="border-b border-[#F1F5F9] last:border-0">
                      <td className="py-3 px-6 font-body-sm text-body-sm font-medium">
                        {patients ? patientName(a.patient_id) : `Patient #${a.patient_id}`}
                      </td>
                      <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                        {providers ? providerName(a.provider_id) : `Provider #${a.provider_id}`}
                      </td>
                      <td className="py-3 px-6 font-body-sm text-body-sm text-on-surface-variant">
                        {new Date(a.scheduled_at).toLocaleString()}
                      </td>
                      <td className="py-3 px-6">
                        <span
                          className={`px-2.5 py-1 rounded-full text-[11px] uppercase font-semibold ${
                            STATUS_PILL[a.status] ?? "bg-surface-container"
                          }`}
                        >
                          {a.status.replace("_", " ")}
                        </span>
                      </td>
                      {canUpdateStatus && (
                        <td className="py-3 px-6">
                          <select
                            value={a.status}
                            onChange={(e) => handleStatusChange(a.id, e.target.value)}
                            className="px-2 py-1 rounded-lg border border-[#EEF3F7] font-body-sm text-body-sm"
                          >
                            {STATUS_OPTIONS.map((s) => (
                              <option key={s} value={s}>
                                {s.replace("_", " ")}
                              </option>
                            ))}
                          </select>
                        </td>
                      )}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
