from pydantic import BaseModel, Field
from typing import List

# https://fastapi.tiangolo.com/features/#pydantic-features


class SensorDataValue(BaseModel):
    value_type: str = Field(..., description="Type of sensor measurement")
    value: str = Field(..., description="Sensor measurement value as string")


class SensorReading(BaseModel):
    esp8266id: str = Field(..., example="6786729", description="Chip id")
    software_version: str = Field(..., example="NRZ-2024-135", description="Software version of the sensor")
    sensordatavalues: List[SensorDataValue] = Field(
        ...,
        description="List of sensor data measurements",
        example=[
            {"value_type": "SDS_P1", "value": "{{ value }}"},
            {"value_type": "SDS_P2", "value": "{{ value }}"},
            {"value_type": "BME280_temperature", "value": "{{ value }}"},
            {"value_type": "BME280_pressure", "value": "{{ value }}"},
            {"value_type": "BME280_humidity", "value": "{{ value }}"},
            {"value_type": "samples", "value": "{{ value }}"},
            {"value_type": "min_micro", "value": "{{ value }}"},
            {"value_type": "max_micro", "value": "{{ value }}"},
            {"value_type": "interval", "value": "{{ value }}"},
            {"value_type": "signal", "value": "{{ value }}"}
        ]
    )
