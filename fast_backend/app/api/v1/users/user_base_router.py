import traceback
from fastapi import APIRouter
from app.api.v1.users.routes.license_routes import router as license_router
from app.api.v1.users.routes.user_routes import router as user_router
from app.api.v1.users.routes.failed_devices_routes import router as failed_devices_router
from app.api.v1.users.routes.user_list_routes import router as user_list_router
from app.api.v1.users.routes.auth import router as user_auth_router
import sys



routers = APIRouter(
    prefix="/users",
    tags=["users"]
)

router_list = [
    user_router,
    license_router,
    failed_devices_router,
    user_list_router,
    user_auth_router
]
print("router list for user is:::", router_list, file=sys.stderr)
for router in router_list:
    print("router in router list is::::::::", router, file=sys.stderr)
    routers.include_router(router)




