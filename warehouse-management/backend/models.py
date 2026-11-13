from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional
from datetime import date, datetime


# used in E1, E8 and login: the function fields and HTTPExceptions now live in the model as field requirements
# imports needed: BaseModel and Field
# the not_blank validator strips whitespace and rejects values that are empty after stripping
class PackageCreate(BaseModel):
    name: str = Field(min_length=1)
    destination: str = Field(min_length=1)
    weight: int = Field(gt=0)

    @field_validator("name", "destination")
    @classmethod
    def not_blank(cls, value):
        value = value.strip()
        if value == "":
            raise ValueError("cannot be blank")
        return value

class DispatchBatchCreate(BaseModel):
    destination: str = Field(min_length=1)
    vehicle_number: int = Field(gt=0)

    @field_validator("destination")
    @classmethod
    def not_blank(cls, value):
        value = value.strip()
        if value == "":
            raise ValueError("cannot be blank")
        return value

class LoginRequest(BaseModel):
    username: str
    password: str


# used in E3: the function fields and HTTPExceptions are now handled in the model
# imports required model_validator and Optional from typing
# fields can be None here, so not_blank skips None and only checks values that were actually sent by the user
class PackageUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    destination: Optional[str] = Field(default=None, min_length=1)
    weight: Optional[int] = Field(default=None, gt=0)

    @model_validator(mode="after")
    def something_to_update(self):
        if self.name is None and self.destination is None and self.weight is None:
            raise ValueError("Nothing to update")
        return self

    @field_validator("name", "destination")
    @classmethod
    def not_blank(cls, value):
        if value is None:
            return value
        value = value.strip()
        if value == "":
            raise ValueError("cannot be blank")
        return value


# used in E5 and E6 to validate the package search: the model is called inside the endpoint to check the path params
# for this we need date from datetime
class PackageSearch(BaseModel):
    destination: Optional[str] = None
    status: Optional[str] = None
    arrival_date: Optional[date] = None  # "2027-01-09" becomes a date and wrong string fails

    @field_validator("status")
    @classmethod
    def valid_status(cls, value):
        if value is not None and value not in ["Registered", "Dispatched"]:
            raise ValueError("Invalid status")
        return value

class DispatchBatchSearch(BaseModel):
    destination: Optional[str] = None
    vehicle_number: Optional[int] = None  # "35" becomes 35, "gfyrjtf" fails
    dispatch_status: Optional[str] = None

    @field_validator("dispatch_status")
    @classmethod
    def valid_dispatch_status(cls, value):
        if value is not None and value not in ["Pending", "Dispatched"]:
            raise ValueError("Invalid dispatch status")
        return value

# used in E2, E5 and login: these return an object for display, only the fields in the model are sent, otherwise it's a 500 error
# imports we need datetime
# PackageOut replaces the convert-to-dict helper function from main.py
class PackageOut(BaseModel):
    package_id: int
    name: str
    destination: str
    weight: int
    arrival_date: datetime
    status: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


# used in functions.py where we changed the verify token function
class TokenPayload(BaseModel):
    username: str
    token_type: str

    @field_validator("token_type")
    @classmethod
    def valid_type(cls, value):
        if value not in ["access", "refresh"]:
            raise ValueError("Invalid token type")
        return value