# UI/UX Design Reference

**Status: Template received.** Source: `UIUX Design/` folder (25 screens + 2 design-system files) supplied by the student. This document details the **Dashboard (Module 5)** in full, and catalogues the remaining 21 screens for the phases that will use them.
**Related:** `deccission.md` (ADR-010, ADR-012), `impmemnentaion-plan.md` Phase 6, `api-spec.md` §7, `flow.md` §5.

---

## 1. Design System — "Clinical Precision"

Two design-system files ship with the template:

- **`DESIGN.md`** — *"Clinical Precision"*: the enterprise/desktop system used by every staff-facing screen (Admin, Doctor, Executive, Operations).
- **`DESIGN2.md`** — *"Clinical Precision Mobile"*: a variant for the patient-facing mobile app (screen `s25`), same foundation, touch-optimized.

**Brand personality:** "authoritative yet empathetic" — high-end minimalism, white-space-first, low cognitive load, calm/trustworthy "Medical Blue" palette. Reds/oranges reserved strictly for clinical alerts to avoid alert fatigue.

**Colors (desktop):** background/surface `#f9f9ff` (or `#F4F7FA` canvas per component CSS), card surface `#ffffff`, primary `#0058be` (buttons often render as `#3B82F6`), secondary `#0051d5`, error `#ba1a1a` with `#ffdad6` container, text `on-surface` `#111c2d` / `on-surface-variant` `#424754`. Full token set (including `-fixed`, `-container`, `-dim` variants) is in `DESIGN.md`.

**Typography:** dual-font — **Manrope** (headings, `display-kpi` numbers) + **Inter** (body copy, labels, tables), loaded via Google Fonts. Key scale: `display-kpi` 48px/700, `headline-lg` 32px/600, `headline-md` 24px/600, `headline-sm` 20px/600, `body-md` 16px/400, `label-md` 12px/500 (uppercase, tracked).

**Layout & spacing:** 12-column grid, max-width 1440px, 8px base spacing unit, 24px gutter, 40px desktop side margin / 16px mobile. Breakpoints: desktop ≥1024px (12 col), tablet 768–1023px (8 col), mobile <767px (4 col).

**Elevation:** cards use soft ambient shadows, not heavy borders — Level 1 (cards) `0px 4px 20px rgba(0,0,0,0.03)`; Level 2 (modals/dropdowns) `0px 12px 32px rgba(0,0,0,0.08)`. Hover state lifts a card -2px with a deeper shadow.

**Shape:** inputs/buttons 8px radius; large dashboard cards 16–24px radius (`rounded-lg`/`rounded-xl`/`rounded-2xl`); navigation pills and status chips fully rounded (9999px).

**Implementation stack confirmed from the template (ADR-012):** Tailwind CSS (via CDN utility classes in the template; a standard Tailwind build in the real app), Material Symbols Outlined icon set, Chart.js for interactive charts. This supplements — doesn't replace — the brief's Plotly/Matplotlib, which are reserved for Python-side report/analysis outputs (see `deccission.md` ADR-012).

---

## 2. Screen Inventory (all 25 screens)

| # | Screen title | Maps to |
|---|---|---|
| s1 | Patients | Module 1 |
| s2 | **Executive Overview** | **Module 5 — Dashboard** |
| s3 | Telemedicine & Remote Monitoring Hub | Module 2 / 3 (combined hub) |
| s4 | Analytics & AI Risk Assessment | Module 4 |
| s5 | **Unified Healthcare Dashboard** | **Module 5 — Dashboard (home/landing)** |
| s6 | Patient Directory | Module 1 |
| s7 | Patient 360° Profile | Module 1 |
| s8 | Appointments | Module 2 |
| s9 | Telemedicine Waiting Room | Module 2 |
| s10 | Telemedicine | Module 2 |
| s11 | Active Telemedicine Consultation | Module 2 |
| s12 | Remote Patient Monitoring | Module 3 |
| s13 | Alerts & Triage | Module 3 |
| s14 | AI Health Risk Assessment | Module 4 |
| s15 | AI Risk Assessment Detail | Module 4 |
| s16 | Healthcare Insights | Module 5 (trend analytics) |
| s17 | **Healthcare Operations Dashboard** | **Module 5 — Dashboard (operations)** |
| s18 | Healthcare Provider Management | Module 1 |
| s19 | System Monitoring | Cross-cutting (Prometheus/Grafana-adjacent) |
| s20 | Security & Audit Center | Cross-cutting (Security) |
| s21 | Users & Roles | Cross-cutting (Auth/RBAC, Admin) |
| s22 | Documents | Not in the 5 mandatory modules — optional/out of scope unless useful |
| s23 | Settings | Cross-cutting |
| s24 | Login | Auth |
| s25 | GlobalCare Patient Mobile App | Patient-facing mobile (uses "Clinical Precision Mobile", `DESIGN2.md`) — not required by the brief; flag as out of scope unless the student wants it as a stretch item |

The three bolded screens together form the **Executive Healthcare Operations Dashboard** required by Module 5 — detailed below. The other 21 will get the same level of detail as their implementation phase (Phase 2–5, 7) approaches.

---

## 3. Dashboard (Module 5) — Detailed Spec

The brief's single "Executive Healthcare Operations Dashboard" module is realized in the template as **three cooperating views**, reached from the same top navigation:

- **`s5` Unified Healthcare Dashboard** — default landing/home view after login.
- **`s2` Executive Overview** — a more analytical, chart-and-risk-focused view (nav highlights "Overview").
- **`s17` Healthcare Operations Dashboard** — an operations/staffing/scheduling-focused view (nav highlights "Operations").

Recommended routing: `/dashboard` (Unified, default), `/dashboard/executive`, `/dashboard/operations`, all under one "Dashboard" section, switchable via the top-nav Overview/Operations toggle already present in the template. Role defaults can point different personas at different views (e.g., Executive → `/dashboard/executive`, Administrator/Ops staff → `/dashboard/operations`) while all three remain reachable to any authorized staff role.

### 3.1 Shared layout (all three views)

- **Top nav bar:** "GlobalCare" logo (left), primary nav — Overview, Patients, Appointments, Telemedicine, Monitoring, Analytics, (AI Risk on the Operations screen) — search input, notification bell, settings gear, user avatar + name + role label (e.g., "Clinical Director", "Chief of Surgery"), and an "Operations" pill/button that stays visible as a shortcut into the operations view.
- **Canvas:** max-width 1440px, centered; page background `#f9f9ff`/`#F4F7FA`; content cards white with soft shadow.
- **Responsive:** KPI card rows collapse 4-col → 2-col (tablet) → 1-col (mobile); side-by-side panels stack vertically below `lg` breakpoint.

### 3.2 `s5` — Unified Healthcare Dashboard (home/landing)

- Personalized header: **"Welcome back, Dr. {Name}!"** + subtitle ("Here's today's healthcare operations overview.") + a date-range selector (Today / Yesterday / Last 7 Days) + an **Export Data** button.
- Row of 4 KPI stat cards: **Total Patients** (8,240, +8.4%), **Today's Appointments** (1,284, +12.4%), **Active Monitoring** (1,240, +6.2%), **High Risk Patients** (126, -4.1%, red accent bar). Each card: icon chip, uppercase tracked label, large `display-kpi` number, trend chip with up/down arrow.
- **API mapping:** `GET /dashboard/overview` for the four KPIs; **Export Data** → `GET /reports/executive`.

### 3.3 `s2` — Executive Overview

- Row of 4 KPI cards: **Total Patients** (1,492, +12%), **Bed Occupancy** (87%, "45 beds available"), **Remote Alerts** (24, "5 Critical require action"), **AI Risk Alerts** (18, "Flagged for review today").
- **Clinical Activity & RPM** panel (8/12 columns): a Chart.js line chart of "Active RPM Sessions" vs. "In-Patient Alerts" across the week, with a Today/Week toggle. → `GET /dashboard/trends`.
- **AI Risk Assessment** panel (4/12 columns): scrollable list of top at-risk patients, each row showing a circular risk-score badge (0–100, red for Critical / neutral for Elevated), patient first-name + initial, specialty, and a status pill; "View All Assessments" button. → `GET /ai/predictions/{patientId}` (aggregated top-N view) / Module 4.
- **Operational Efficiency** section (full width, two cards):
  - *Appointment Scheduling* — Scheduled / Completed / No-Shows counts for today. → Module 2 appointment endpoints.
  - *Telemedicine* — Waiting Patients count, Avg Wait Time, "Manage Queue" button. → Module 2 telemedicine endpoints.

### 3.4 `s17` — Healthcare Operations Dashboard

- Page header: **"Healthcare Operations"** + subtitle + a Department filter (All / Cardiology / Neurology / Emergency) + a date filter (defaults to "Today").
- Row of 4 summary cards: **Appointments Today** (1,284), **Completed** (842), **At-Risk Cases** (126, red-flagged), **Available Providers** (184).
- **Provider Schedule** (8–9/12 columns): a Gantt-style timeline — rows are providers, columns are hourly slots (08:00–16:00), color-coded activity blocks for Consult / Telemedicine / Break. → aggregated `GET /providers/{id}/schedule` across all providers for the selected day/department.
- Right sidebar (3–4/12 columns):
  - **Important Alerts** — severity-coded cards: Critical (red, e.g. "High-Risk Patient — Immediate clinical review required in ER"), Warning (amber, e.g. staffing shortage), Info (blue, e.g. "Remote monitoring device offline"). → `GET /monitoring/alerts` plus operational/staffing-alert sources.
  - **Provider Availability** — avatar with presence dot (green/amber/gray), name, specialty + workload %, quick-call action button, "View Full Roster" link. → `GET /providers` combined with workload/schedule data.

### 3.5 Reusable component inventory (dashboard-relevant)

| Component | Notes |
|---|---|
| KPI stat card | Icon chip + uppercase `label-md` + `display-kpi` value + optional trend chip |
| "Glass card" container | White/near-white surface, 16–24px radius, soft ambient shadow, hover lift |
| Status pill/chip | Pill-shaped, tinted background + darker text (Critical/Elevated/Scheduled/Completed/etc.) |
| Risk-score badge | Circular badge with numeric score, color-coded by severity band |
| Timeline/Gantt row | Operations view only — per-provider hourly schedule |
| Chart.js line chart | Primary/secondary line colors, minimal gridlines, legend top-right, no axis clutter |
| Top navigation bar | Identical structure across every staff-facing screen in the template |

### 3.6 Accessibility & responsive notes

- Status/severity is always paired with an icon **and** a text label, never color alone.
- Icons are monochrome by default; color is reserved for semantic/status icons.
- Minimum interactive touch target 44×44px (carried over from the mobile system; worth applying consistently for keyboard/touch users on desktop too).
- KPI rows and multi-column panels must reflow cleanly at the tablet/mobile breakpoints defined in §1.

---

## 4. Other Module Screens

| Phase | Screens | Status |
|---|---|---|
| Post-completion (§6 below) | s1/s6 Patients (list + inline detail, merged rather than a separate s7 profile page), s8 Appointments, s12 Remote Patient Monitoring (alerts + reading history, merged rather than a separate s13 Alerts & Triage page), s4/s14 Analytics & AI Risk Assessment | **Built** — see §6 |
| Not built (deliberately simplified away) | s7 Patient 360° Profile (folded into the Patients list's inline expand instead of a separate page), s9 Telemedicine Waiting Room / s11 Active Telemedicine Consultation (no real-time video-call backend exists — the Telemedicine screen focuses on the real, working part: the consultation queue and recording form), s15 AI Risk Assessment Detail (folded into Analytics' prediction list), s18 Healthcare Provider Management (no dedicated screen; providers are managed via the API/admin-guide.md) | Not built |
| Phase 7 (Security/Observability) | s19 System Monitoring, s20 Security & Audit Center, s21 Users & Roles | Not built — Prometheus/Grafana (Phase 7) cover the observability need directly; no in-app screen was required |
| Cross-cutting | s23 Settings, s24 Login (built) | Login built; Settings not built |
| Out of scope (flagged) | s22 Documents (not a mandatory module), s25 Patient Mobile App (mobile is not required by the brief) | Out of scope |
| Analytics | s16 Healthcare Insights (supplements the Dashboard's trend-analytics requirement) | Not built — `GET /dashboard/trends` on the Executive Overview covers this |

---

## 5. Open Items — resolved (Phase 6, 2026-08-22)

1. **Dashboard routing: RESOLVED — 3-route approach adopted**, exactly as recommended (`/dashboard`, `/dashboard/executive`, `/dashboard/operations`), all reachable via the top-nav Overview/Operations toggle from the template.
2. **s16 "Healthcare Insights": RESOLVED — not built in Phase 6.** Module 5's "healthcare trend analytics" requirement (`api-spec.md` §7, `GET /dashboard/trends`) is satisfied by the Executive Overview's Clinical Activity & RPM chart. `impmemnentaion-plan.md` Phase 6's exit criteria only requires the three documented dashboard views reflecting live data — s16 remains catalogued in §4 as a future enhancement, not a Phase 6 requirement.
3. **s22 Documents / s25 Mobile App: RESOLVED — confirmed out of scope**, per this document's own original recommendation (neither maps to one of the 5 mandatory modules). No implementation time spent on either.

**Additional Phase 6 note — honest data only:** several of the template's mock KPIs have no backing data model in this project (e.g. "Bed Occupancy," per-provider real-time presence/workload-%, appointment wait-time tracking — none of these are tracked anywhere in `backend-schema.md`). Rather than fabricate numbers for these, Phase 6 substitutes real, computable equivalents (e.g. Active Providers count instead of Bed Occupancy) and keeps the template's exact visual language (cards, colors, typography, layout) while every number shown is a real query result — consistent with every other phase's "no fabricated data" standard. See `impmemnentaion-plan.md` Phase 6 status for the specific substitutions.

## 6. Post-completion enhancement — Patients/Appointments/Telemedicine/Monitoring/Analytics screens

After the 10-phase roadmap was already complete, the user tested the deployed app and flagged that the top nav's Patients/Appointments/Telemedicine/Monitoring/Analytics links were inert placeholder text (`onClick={(e) => e.preventDefault()}`, matching the original Phase 6 scope decision that only the Dashboard was mandated for the frontend). Given the choice between leaving them inert, visually disabling them, removing them, or building real screens, the user chose to build real screens — genuinely expanding frontend scope beyond the exam brief's minimum.

Each new screen is built directly on that module's real, already-tested backend API (no new endpoints were added) — see `user-guide.md` and `admin-guide.md` for what each role can do on each screen. Two real bugs were found and fixed while building and testing this:

- **A latent redirect-loop bug**, dormant since Phase 6: `ProtectedRoute`'s denial path and `Login.jsx`'s post-login redirect both hard-coded `/dashboard` as the fallback, but Doctor and Patient roles have no dashboard access — logging in as either would have looped forever. Never surfaced before because no Doctor/Patient demo login existed until this work needed one. Fixed with a shared `frontend/src/auth/defaultRoute.js` helper mapping each role to a route it can actually reach (Doctor → `/patients`, Patient → `/appointments`).
- **A real UX gap**: a Patient booking an appointment has no way to browse the provider directory (`GET /providers` is Administrator/Executive only, per `api-spec.md` §3) — the booking form's provider dropdown was empty for that role. Fixed by falling back to a plain provider-ID input for roles without directory access, rather than fabricating a provider list the API doesn't actually grant them.

`backend/scripts/seed_dev_users.py` was extended to also create a Doctor (`doctor@globalcare-demo.com`) and Patient (`patient@globalcare-demo.com`, assigned to that doctor) demo login — previously only Administrator/Executive had seeded credentials, meaning half the platform's role-scoped actions had no way to be demoed at all.
