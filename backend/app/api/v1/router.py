from fastapi import APIRouter

from app.api.v1 import (
    ai,
    appointments,
    auth,
    dashboard,
    facilities,
    health,
    monitoring,
    patients,
    providers,
    reports,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(providers.router)
api_router.include_router(facilities.router)
api_router.include_router(appointments.router)
api_router.include_router(monitoring.router)
api_router.include_router(ai.router)
api_router.include_router(dashboard.router)
api_router.include_router(reports.router)

# Module routers are added here as each phase lands, per docs/api-spec.md:
#   auth, patients, providers, facilities, reports/registration -> Phase 2 (§2-3) [done]
#   appointments/consultations, providers/{id}/schedule, reports/appointments -> Phase 3 (§4) [done]
#   monitoring  -> Phase 4 (§5) [done]
#   ai          -> Phase 5 (§6) [done]
#   dashboard, reports/executive -> Phase 6 (§7) [done]
