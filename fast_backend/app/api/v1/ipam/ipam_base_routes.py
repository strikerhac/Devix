from fastapi import APIRouter
# from app.api.v1.ipam.utils.ipam_utils import *
# from app.api.v1.ipam.utils.ipam_imports import *
from app.api.v1.ipam.routes.device_routes import router as devices_router
from app.api.v1.ipam.routes.ipam_dashboard_routes import router as ipam_dashboard_router


routers =APIRouter(
    prefix = "/ipam",
    tags = ["ipam"]
)

router_list = [
    devices_router,ipam_dashboard_router
]

for router in router_list:
    routers.include_router(router)

