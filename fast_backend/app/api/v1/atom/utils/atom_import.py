import sys
import traceback
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.utils.db_utils import *
from app.utils.static_list import *
from app.models.atom_models import *
from app.models.site_rack_models import *
from app.schema.atom_schema import *

# from app.models.auto_discovery_models import *
# from app.models.uam_models import *
# from app.models.monitoring_models import *

from app.schema.validation_schema import *
from sqlalchemy import inspect
# from app.schema.response_schema import Response200