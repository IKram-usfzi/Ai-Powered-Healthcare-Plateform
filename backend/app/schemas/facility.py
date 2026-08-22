from pydantic import BaseModel


class FacilityCreate(BaseModel):
    name: str
    type: str
    location: str


class FacilityRead(BaseModel):
    id: int
    name: str
    type: str
    location: str

    model_config = {"from_attributes": True}
