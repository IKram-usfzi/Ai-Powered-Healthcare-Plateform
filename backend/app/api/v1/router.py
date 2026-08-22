from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()
api_router.include_router(health.router)

# Module routers are added here as each phase lands, per docs/api-spec.md:
#   auth        -> Phase 2 (§2)
#   patients    -> Phase 2 (§3)
#   providers   -> Phase 2 (§3)
#   facilities  -> Phase 2 (§3)
#   appointments/consultations -> Phase 3 (§4)
#   monitoring  -> Phase 4 (§5)
#   ai          -> Phase 5 (§6)
#   dashboard   -> Phase 6 (§7)
