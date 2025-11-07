"""
Data transformation module for sensor data processing.
"""
import json
from .models.air_data import SensorReading


class SensorDataTransformer:
    """Handles transformation of sensor data into standardized formats."""

    def transform_to_dict(self,
                          data: SensorReading) -> dict[str:float, str:float, str, float, str:dict]:
        """
        Transform sensor data model to a dictionary with extracted values.

        Args:
            data: Sensor data model object with sensordatavalues array

        Returns:
            dict: Transformed data with Temperature, Pressure, Humidity, and RawData
        """
        result_dict = {}
        sensor_data = data.model_dump_json()
        sensor_data_json = json.loads(sensor_data)

        # Extract specific sensor values
        sensor_data_temp = data.sensordatavalues[2].value
        sensor_data_hum = data.sensordatavalues[4].value
        sensor_data_pres = float(data.sensordatavalues[3].value) / 100.0

        result_dict = {
            'Temperature': sensor_data_temp,
            'Pressure': sensor_data_pres,
            'Humidity': sensor_data_hum,
            'RawData': sensor_data_json
        }
        return result_dict

    # Add future transformation methods here
    def transform_to_csv(self, data) -> str:
        """Transform sensor data to CSV format."""
        pass

    def transform_to_normalized(self, data) -> dict:
        """Normalize sensor values to standard ranges."""
        pass
