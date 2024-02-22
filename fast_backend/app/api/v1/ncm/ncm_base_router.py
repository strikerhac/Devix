from fastapi import APIRouter

from app.api.v1.ncm.routes.ncm_dashboard_routes import router as dashboard_router
from app.api.v1.ncm.routes.ncm_device_routes import router as device_router

routers = APIRouter(
    prefix="/ncm",
    tags=["ncm"],
)

router_list = [dashboard_router, device_router]

for router in router_list:
    routers.include_router(router)


