from datetime import datetime
from enum import Enum

from pydantic import Field

from app.application.pydantic_model import BaseSchema


class HardwareConnectionStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class UserHardwareConnection(BaseSchema):
    display: HardwareConnectionStatus
    camera: HardwareConnectionStatus
