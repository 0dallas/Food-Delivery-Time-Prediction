from pydantic import BaseModel

class DeliveryFeatures(BaseModel):
    Distance_km: float
    Weather: int
    Traffic_Level: int
    Time_of_Day: int
    Vehicle_Type: int
    Preparation_Time_min: int
    Courier_Experience_yrs: float

class PredictionResponse(BaseModel):
    predicted_delivery_time_min: float