# Process & Workflow Flows

**Related:** `architecture.md` (diagram inventory), `api-spec.md`
**Note:** These flows are the source material for diagrams 4, 5, 6, 7, 12–15, and 17 in `architecture.md` §6.

## 1. Patient Registration Flow

```
Administrator → React (registration form) → FastAPI (/patients) → PostgreSQL (insert)
                                                                 → response → patient summary displayed
```
Explains continuity of care: once registered, a patient's record is visible consistently across appointments, monitoring, and AI assessment rather than fragmented across separate systems.

## 2. Telemedicine Appointment & Consultation Flow

```
Patient/Admin → schedule appointment (FastAPI /appointments) → PostgreSQL
Doctor → conducts virtual consultation → records summary (/consultations) → PostgreSQL
                                                                          → consultation history available to Doctor/Admin/Patient
```

## 3. Remote Monitoring & Alert Flow

```
Simulated device/reading source → FastAPI (/monitoring/readings) → PostgreSQL (health_readings)
                                                                  → threshold check
                                                                        │
                                                            abnormal? ──┼── no  → stored only
                                                                  yes  ▼
                                                          alert created → PostgreSQL (alerts)
                                                                       → Redis (de-dup check)
                                                                       → visible to Doctor/Admin
```

## 4. AI Risk Prediction Flow

```
Doctor requests assessment → FastAPI (/ai/risk-assessment)
        → pulls patient's recent readings (PostgreSQL)
        → preprocessing (Pandas/NumPy)
        → model inference (Scikit-learn)
        → risk category + confidence score
        → stored in predictions table
        → returned with AI-assisted recommendation (human judgement required)
```

## 5. Executive Reporting Flow

```
Executive opens dashboard → FastAPI (/dashboard/overview, /dashboard/trends)
        → aggregate queries against PostgreSQL, cached in Redis where hot
        → React + Plotly renders KPIs, trends, provider activity, workload
```

## 6. End-to-End Sequence (maps to mandatory Sequence Diagram, brief §8.17)

```
Patient/Admin        FastAPI              PostgreSQL         Redis          AI Service        React (Executive)
     │  register patient  │                    │                │                │                    │
     │───────────────────▶│───insert──────────▶│                │                │                    │
     │  schedule appt      │                    │                │                │                    │
     │───────────────────▶│───insert──────────▶│                │                │                    │
     │                     │  consultation done │                │                │                    │
     │                     │───insert──────────▶│                │                │                    │
     │  vitals reading      │                    │                │                │                    │
     │───────────────────▶│───insert──────────▶│                │                │                    │
     │                     │───check abnormal────────────────────▶ dedup check    │                    │
     │                     │◀──alert (if any)────────────────────│                │                    │
     │  request AI risk     │                    │                │                │                    │
     │───────────────────▶│───fetch readings───▶│                │                │                    │
     │                     │────────────────────────────────────────────preprocess+predict────────────▶│
     │                     │◀───────────────────────────────────────────risk+confidence─────────────────│
     │                     │───store prediction─▶│                │                │                    │
     │                     │                    │                │                │  executive views ──▶│
     │                     │◀──aggregate query───│◀──cache────────│                │  dashboard/KPIs      │
```
