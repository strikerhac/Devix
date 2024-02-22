from fastapi import APIRouter
from app.api.v1.main.routes.main_dashboard_routes import router as main_dashboard_router


routers =APIRouter(
    prefix = "/main",
    tags = ["main"]
)

router_list = [
    main_dashboard_router
]

for router in router_list:
    routers.include_router(router)


