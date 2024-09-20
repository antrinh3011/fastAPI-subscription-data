from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class KeywordBase(BaseModel):
    keyword_name: str

class KeywordResponse(BaseModel):
    keyword_id: int
    keyword_name: str

    class Config:
        from_attributes = True

class KeywordSearchVolumeBase(BaseModel):
    created_datetime: datetime
    search_volume: int

class KeywordSearchVolumeResponse(BaseModel):
    keyword_id: int
    created_datetime: datetime
    search_volume: int

    class Config:
        from_attributes  = True

class SubscriptionBase(BaseModel):
    user_id: int
    keyword_id: int
    timing : str
    subscription_start: datetime
    subscription_end: datetime

class SubscriptionResponse(BaseModel):
    user_id: int
    keyword_id: int
    timing : str
    subscription_start: datetime
    subscription_end: datetime

    class Config:
        from_attributes  = True


class UserSubscriptionKeyWordRequest(BaseModel):
    userId: int
    keyword_name: str
    timing: Literal["daily", "hourly"]  # Restrict to 'daily' or 'hourly'
    start_date: datetime  
    end_date: datetime  
class UserSubscriptionKeyWordResponse(BaseModel):
    time: str
    keyword_name: str
    search_volume : int
    