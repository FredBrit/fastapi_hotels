from pydantic import BaseModel, Field, ConfigDict


class FacilityAdd(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class Facility(FacilityAdd):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int        






