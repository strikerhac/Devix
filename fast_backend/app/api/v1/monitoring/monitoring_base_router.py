from fastapi import APIRouter

from app.api.v1.monitoring.device.monitoring_dashboard_routes import router as dashboard_routes
from app.api.v1.monitoring.device.monitoring_device_dashboard_routes import \
    router as device_dashboard_routes
from app.api.v1.monitoring.device.monitoring_device_routes import router as monitoring_device_routes
from app.api.v1.monitoring.device.monitoring_alert_routes import router as monitoring_alert_routes
from app.api.v1.monitoring.device.monitoring_credentials_routes import router as monitoring_credentials_routes
from app.api.v1.monitoring.networks.monitoring_networks_routes import router as monitoring_network_routes
from app.api.v1.monitoring.servers.moniotring_servers_routes import router as monitoring_server_routes
from app.api.v1.monitoring.clouds.aws_routes import router as monitoring_cloud_routes
from app.api.v1.monitoring.device.monitoring_scheduler import router as monitoring_scheduler_router
from app.api.v1.monitoring.device.monitoring_static_list import router as monitoring_static_router
# monitoring_scheduler_router
routers = APIRouter(
    prefix="/monitoring",
    tags=["monitoring"]
)
router_list = [dashboard_routes, monitoring_device_routes, device_dashboard_routes,
               monitoring_alert_routes, monitoring_credentials_routes,monitoring_network_routes,monitoring_server_routes,monitoring_cloud_routes,monitoring_static_router,monitoring_scheduler_router]

for router in router_list:
    routers.include_router(router)



