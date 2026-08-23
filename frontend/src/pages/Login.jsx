import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { defaultRouteForRole } from "../auth/defaultRoute";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const me = await login(email, password);
      navigate(defaultRouteForRole(me.role));
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="bg-background text-on-surface min-h-screen w-full flex font-body-md">
      {/* Left: brand messaging (UIUX Design/s24) */}
      <div className="hidden lg:flex flex-col w-[55%] bg-surface-container-low h-full relative overflow-hidden px-margin-desktop py-stack-lg">
        <div className="flex items-center gap-2 mb-16 z-10">
          <span className="material-symbols-outlined text-primary text-3xl">ecg_heart</span>
          <span className="font-headline-sm text-headline-sm text-primary font-bold">
            GlobalCare
          </span>
        </div>
        <div className="max-w-xl z-10 mt-12">
          <h1 className="font-display-kpi text-display-kpi text-on-background mb-6">
            Connected healthcare.
            <br />
            Better decisions.
          </h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant leading-relaxed">
            Manage patients, consultations, remote monitoring and healthcare operations from one
            unified platform. Engineered for clinical precision.
          </p>
        </div>
      </div>

      {/* Right: login card */}
      <div className="w-full lg:w-[45%] flex items-center justify-center p-margin-mobile lg:p-margin-desktop bg-surface-container-lowest relative">
        <div className="absolute top-margin-mobile left-margin-mobile lg:hidden flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-2xl">ecg_heart</span>
          <span className="font-headline-sm text-headline-sm text-primary font-bold">
            GlobalCare
          </span>
        </div>
        <div className="w-full max-w-[440px] bg-surface-container-lowest rounded-xl shadow-[0px_12px_32px_rgba(0,0,0,0.08)] border border-outline-variant p-8">
          <div className="mb-stack-md">
            <h2 className="font-headline-md text-headline-md text-on-background mb-2">
              Welcome back
            </h2>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Sign in to your GlobalCare account.
            </p>
          </div>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label
                className="block font-label-md text-label-md text-on-surface mb-2"
                htmlFor="email"
              >
                Email Address
              </label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline text-[20px]">
                  mail
                </span>
                <input
                  id="email"
                  type="email"
                  required
                  autoComplete="username"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="clinician@globalcare-demo.com"
                  className="block w-full pl-10 pr-3 py-2 border border-outline-variant rounded-lg bg-surface-container-lowest text-on-surface font-body-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-shadow"
                />
              </div>
            </div>
            <div>
              <label
                className="block font-label-md text-label-md text-on-surface mb-2"
                htmlFor="password"
              >
                Password
              </label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline text-[20px]">
                  lock
                </span>
                <input
                  id="password"
                  type="password"
                  required
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="block w-full pl-10 pr-3 py-2 border border-outline-variant rounded-lg bg-surface-container-lowest text-on-surface font-body-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-shadow"
                />
              </div>
            </div>
            {error && <p className="font-body-sm text-body-sm text-error">{error}</p>}
            <div className="pt-2">
              <button
                type="submit"
                disabled={submitting}
                className="w-full flex justify-center py-3 px-4 rounded-full font-label-md text-label-md text-on-primary bg-primary hover:bg-secondary-container focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors disabled:opacity-60"
              >
                {submitting ? "Signing in…" : "Sign In"}
              </button>
            </div>
          </form>
          <div className="mt-8 flex items-center justify-center gap-1.5 opacity-70">
            <span className="material-symbols-outlined text-[16px] text-tertiary">
              shield_lock
            </span>
            <span className="font-label-sm text-label-sm text-tertiary uppercase tracking-wider">
              Secure Enterprise Platform
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
