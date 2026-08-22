from fastapi import APIRouter

from app.api.v1 import auth, facilities, health, patients, providers, reports

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(providers.router)
api_router.include_router(facilities.router)
api_router.include_router(reports.router)

# Module routers are added here as each phase lands, per docs/api-spec.md:
#   auth, patients, providers, facilities, reports/registration -> Phase 2 (§2-3) [done]
#   appointments/consultations -> Phase 3 (§4)
#   monitoring  -> Phase 4 (§5)
#   ai          -> Phase 5 (§6)
#   dashboard   -> Phase 6 (§7)
