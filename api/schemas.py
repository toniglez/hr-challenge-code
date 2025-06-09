from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ----------- LOAD SCHEMAS -----------

class LoadBase(BaseModel):
    origin_county: str
    origin_state: str
    destination_county: str
    destination_state: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: Optional[str] = None
    loadboard_rate: Optional[float] = None
    max_loadboard_rate: Optional[float] = None
    notes: Optional[str] = None
    weight: Optional[float] = None
    commodity_type: Optional[str] = None
    num_of_pieces: Optional[int] = None
    miles: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None

class LoadCreate(LoadBase):
    pass

class LoadRead(LoadBase):
    load_id: int

    class Config:
        orm_mode = True


# ----------- CALL SCHEMAS -----------

class CallBase(BaseModel):
    timestamp: Optional[datetime] = None
    created_at: Optional[datetime] = None
    carrier_mc_number: Optional[str] = None
    authorized: Optional[bool] = False
    origin_state: Optional[str] = None
    weight_max: Optional[float] = None
    call_outcome: Optional[str] = None
    sentiment: Optional[str] = None
    summary: Optional[str] = None
    negotiation_attempts: Optional[int] = 0
    original_price: Optional[float] = None
    final_offer: Optional[float] = None
    selected_load_id: Optional[int] = None
    transcript: Optional[str] = None
    notes: Optional[str] = None

class CallCreate(CallBase):
    pass

class CallRead(CallBase):
    id: int

    class Config:
        orm_mode = True
class CallUpdate(BaseModel):
    carrier_mc_number: Optional[str] = None
    authorized: Optional[bool] = None
    origin_state: Optional[str] = None
    weight_max: Optional[float] = None
    call_outcome: Optional[str] = None
    sentiment: Optional[str] = None
    summary: Optional[str] = None
    negotiation_attempts: Optional[int] = None
    original_price: Optional[float] = None
    final_offer: Optional[float] = None
    selected_load_id: Optional[int] = None
    transcript: Optional[str] = None
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True