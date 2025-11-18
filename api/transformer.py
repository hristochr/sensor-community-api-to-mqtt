"""
Data transformation module for sensor data processing.
"""
import json
from .models.air_data import SensorReading
import logging
from typing import Optional
from decimal import Decimal, InvalidOperation
from attrs import define, field, validators


logger = logging.getLogger(__name__)


class DataQualityError(Exception):
    """Raised when sensor data fails any of the data quality checks."""
    pass


@define
class ValidationRanges:
    """Configuration for sensor data validation ranges."""
    temp_min: float = field(default=-50.0, validator=validators.instance_of(float))
    temp_max: float = field(default=85.0, validator=validators.instance_of(float))
    pressure_min: float = field(default=300.0, validator=validators.instance_of(float))
    pressure_max: float = field(default=1100.0, validator=validators.instance_of(float))
    humidity_min: float = field(default=0.0, validator=validators.instance_of(float))
    humidity_max: float = field(default=100.0, validator=validators.instance_of(float))


@define
class SensorDataTransformer:
    """Handles transformation of sensor data into standardized formats."""

    strict_mode: bool = field(default=True, validator=validators.instance_of(bool))
    ranges: ValidationRanges = field(factory=ValidationRanges)

    def _validate_value(self, value: float,
                        min_val: float,
                        max_val: float,
                        field_name: str) -> bool:
        """
        Validate that a sensor value is within the acceptable range.

        Args:
            value: The value to validate
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value
            field_name: Name of the field for error messages

        Returns:
            bool: True if valid

        Raises:
            DataQualityError: If strict_mode=True and validation fails
        """
        if value is None:
            msg = f"{field_name} is None"
            if self.strict_mode:
                raise DataQualityError(msg)
            logger.warning(msg)
            return False

        if not isinstance(value, (int, float)):
            msg = f"{field_name} is not numeric: {type(value)}"
            if self.strict_mode:
                raise DataQualityError(msg)
            logger.warning(msg)
            return False

        if not (min_val <= value <= max_val):
            msg = f"{field_name} out of range: {value} (expected {min_val}-{max_val})"
            if self.strict_mode:
                raise DataQualityError(msg)
            logger.warning(msg)
            return False

        return True

    def _safe_extract_value(self,
                            data: 'SensorReading',
                            index: int,
                            field_name: str) -> Optional[float]:
        """
        Safely extract value from sensordatavalues array.
        Args:
            data: Sensor data model
            index: Index in sensordatavalues array
            field_name: Name of field for error messages

        Returns:
            float or None: Extracted value or None if extraction fails
        """
        try:
            if not data.sensordatavalues or len(data.sensordatavalues) <= index:
                raise IndexError(f"Index {index} out of range")

            value = data.sensordatavalues[index].value
            return float(value)
        except (IndexError, AttributeError, ValueError, TypeError) as e:
            msg = f"Failed to extract {field_name} at index {index}: {e}"
            if self.strict_mode:
                raise DataQualityError(msg)
            logger.error(msg)
            return None

    def transform_to_dict(self,
                          data: 'SensorReading') -> Optional[dict]:
        """
        Transform sensor data model to a dictionary with extracted values.
        Includes data quality validation.

        Args:
            data: Sensor data model object with sensordatavalues array

        Returns:
            dict: Transformed data with Temperature, Pressure, Humidity, and RawData
            None: If validation fails and strict_mode=False

        Raises:
            DataQualityError: If validation fails and strict_mode=True
        """
        try:
            # Extract raw JSON for storage
            sensor_data = data.model_dump_json()
            sensor_data_json = json.loads(sensor_data)

            # Extract and validate Temperature
            temp = self._safe_extract_value(data, 2, 'Temperature')
            if temp is not None:
                self._validate_value(temp,
                                     self.ranges.temp_min,
                                     self.ranges.temp_max, 'Temperature')

            # Extract and validate Humidity
            humidity = self._safe_extract_value(data, 4, 'Humidity')
            if humidity is not None:
                self._validate_value(humidity,
                                     self.ranges.humidity_min,
                                     self.ranges.humidity_max, 'Humidity')

            # Extract and validate Pressure (convert from Pa to hPa)
            pressure_raw = self._safe_extract_value(data, 3, 'Pressure')
            if pressure_raw is not None:
                pressure = pressure_raw / 100.0
                self._validate_value(pressure,
                                     self.ranges.pressure_min,
                                     self.ranges.pressure_max, 'Pressure')
            else:
                pressure = None

            # Check if all required values are present
            if None in (temp, humidity, pressure):
                msg = "Missing required sensor values"
                if self.strict_mode:
                    raise DataQualityError(msg)
                logger.warning(msg)
                return None

            # Convert to Decimal for database precision (matches SQL DECIMAL types)
            result_dict = {
                'Temperature': round(Decimal(str(temp)), 2),
                'Pressure': round(Decimal(str(pressure)), 2),
                'Humidity': round(Decimal(str(humidity)), 2),
                'RawData': sensor_data_json
            }

            logger.debug(f"Successfully transformed sensor data: {result_dict}")
            return result_dict

        except (json.JSONDecodeError, InvalidOperation) as e:
            msg = f"Data transformation error: {e}"
            if self.strict_mode:
                raise DataQualityError(msg)
            logger.error(msg)
            return None

    # future transformation palceholders
    def transform_to_csv(self, data) -> str:
        """Transform sensor data to CSV format."""
        pass

    def transform_to_normalized(self, data) -> dict:
        """Normalize sensor values to standard ranges."""
        pass
