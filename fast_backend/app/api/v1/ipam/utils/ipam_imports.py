from app.models.ipam_models import *
from app.api.v1.ipam.utils import *
from app.api.v1.ipam.routes.device_routes import *
from app.api.v1.ipam.utils.ipam_utils import *
import sys
import traceback
from app.schema.base_schema import *
# from app.schema.
from app.schema.ipam_schema import *
from app.core.config import configs
from app.models.atom_models import *
from app.utils.db_utils import *
import threading
import subprocess
# from ping3 import ping, verbose_ping
import os
from subprocess import *
import re
import gzip
import json
from fastapi.responses import JSONResponse
import base64
import socket
import nmap
from netaddr import IPNetwork
import platform
from app.models.uam_models import *
# from app.ipam_scripts.f5 import F5
# from app.ipam_scripts.fortigate_vip import FORTIGATEVIP
# from app.ipam_scripts.ipam import IPAM
# from app.ipam_scripts.ipam_physical_mapping import IPAMPM