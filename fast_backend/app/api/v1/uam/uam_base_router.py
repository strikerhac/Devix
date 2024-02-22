from app.api.v1.atom.utils.atom_utils import *
from app.api.v1.uam.routes.aps_routes import router as aps_router
from app.api.v1.uam.routes.device_routes import router as device_router
from app.api.v1.uam.routes.license_routes import router as license_router
from app.api.v1.uam.routes.module_routes import router as module_router
from app.api.v1.uam.routes.rack_routes import router as rack_router
from app.api.v1.uam.routes.sfp_routes import router as sfp_router
from app.api.v1.uam.routes.site_routes import router as site_router
from app.api.v1.uam.routes.sntc_routes import router as sntc_router

routers = APIRouter(
    prefix="/uam",
    tags=["uam"],
)

router_list = [
    site_router,
    rack_router,
    device_router,
    module_router,
    license_router,
    sfp_router,
    aps_router,
    sntc_router
]

for router in router_list:
    routers.include_router(router)
