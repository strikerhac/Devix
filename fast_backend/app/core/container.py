from dependency_injector import containers, providers
from app.core.config import configs
from app.core.database import Database
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository

#from app.services.rack_service import RackService
#from app.repository.rack_repository import RackRepository

from app.repository.blacklisted_token_repository import BlacklistedTokenRepository
from influxdb_client import InfluxDBClient, Point, WritePrecision


from dotenv import load_dotenv

load_dotenv()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            # "app.api.v1.endpoints.auth",
            # "app.api.v1.endpoints.post",
            # "app.api.v1.endpoints.tag",
            "app.api.v1.users.routes.auth",
            "app.api.v1.routes",
            "app.api.v1.users.routes.user_routes",
            # "app.api.v2.endpoints.auth",
            # "app.api.v2.endpoints.site",
            #"app.api.v2.endpoints.rack",

            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URL)

    # influxdb_client = providers.Singleton(
    #     InfluxDBClient,
    #     url=configs.INFLUXDB_URL,
    #     token=configs.INFLUXDB_TOKEN,
    #     org=configs.INFLUXDB_ORG)

    # influxdb_repository = providers.Factory(
    #     client=influxdb_client,
    #     bucket=configs.INFLUXDB_BUCKET,
    #     org=configs.INFLUXDB_ORG,
    #     token=configs.INFLUXDB_TOKEN
    # )
    # device_service = providers.Factory(DeviceService, influxdb_repository=influxdb_repository)

    # site_repo = providers.Factory(SiteRepository, session_factory=db.provided.session)
    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    #rack_repository = providers.Factory(RackRepository, session_factory=db.provided.session)
    blacklisted_token_repository = providers.Factory(
        BlacklistedTokenRepository,
        session_factory=db.provided.session
    )

    auth_service = providers.Factory(AuthService, user_repository=user_repository,
                                     blacklisted_token_repository=blacklisted_token_repository)
    # site_service = providers.Factory(SiteService, site_repository=site_repo)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    #rack_service = providers.Factory(RackService, rack_repository=rack_repository)
