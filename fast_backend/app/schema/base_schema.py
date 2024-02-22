from pydantic import BaseModel,Field,constr,validator
from typing import List, Optional, Union
from datetime import datetime




class BaseSchema(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        return setattr(self, key, value)


class SummeryResponseSchema(BaseSchema):
    data: list[dict]
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class DeleteResponseSchema(BaseSchema):
    data: dict
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class ListtDeleteResponseSchema(BaseSchema):
    data: list[int]
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

    # successlist: List[Message]
    # errorlist: List[Message]
    # successlen: int
    # errorlen: int


class NameValueListOfDictResponseSchema(BaseSchema):
    name: str
    value: int


class NameValueDictResponseSchema(BaseSchema):
    name: list[str  | None]
    value: list[int| None]


class IpAddressRequestSchema(BaseSchema):
    ip_address: str


class ModelBaseInfo(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class FindBase(BaseModel):
    ordering: Optional[str]
    page: Optional[int]
    page_size: Optional[Union[int, str]]


class SearchOptions(FindBase):
    total_count: Optional[int]


class FindResult(BaseModel):
    founds: Optional[List]
    search_options: Optional[SearchOptions]


class FindDateRange(BaseModel):
    created_at__lt: str
    created_at__lte: str
    created_at__gt: str
    created_at__gte: str


class Blank(BaseModel):
    pass



class SortSeverity(BaseSchema):
    name : str
    value : int


class DeviceType(BaseSchema):
    name : str
    value : int        