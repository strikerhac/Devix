
from typing import List
from app.schema.base_schema import *
class CustomResponse:
    def __init__(self, message: str, data:None, status: int = 0):
        self.message = message
        self.data = data if data is not None else None
        self.status = status
 
    def as_tuple(self):
        return {"message": self.message, "data": self.data, "status": self.status}, self.status
    


class Response200(BaseSchema):
    data: dict
    message: str