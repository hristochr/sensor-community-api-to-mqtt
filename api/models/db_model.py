from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    DateTime,
    Index
    )
from sqlalchemy.dialects.mssql import JSON, DECIMAL
from sqlalchemy.sql import text
from attrs import define, field


@define
class WeatherData():
    metadata: MetaData = field(factory=MetaData)
    schema_name: str = field(default='dbo')
    weather_data: Table = field(init=False)

    def __attrs_post_init__(self):
        """Initialize the tables with the given schema."""
        self.weather_data = Table(
            'WeatherData',
            self.metadata,
            Column('Id', Integer, primary_key=True, autoincrement=True),
            Column('Timestamp', DateTime, server_default=text('GETDATE()'), nullable=False),
            Column('Temperature', DECIMAL(5, 2), nullable=False),
            Column('Pressure', DECIMAL(6, 2), nullable=False),
            Column('Humidity', DECIMAL(5, 2), nullable=False),
            Column('RawData', JSON, nullable=False),
            schema=self.schema_name
        )

        Index('ix_weatherdata_timestamp', self.weather_data.c.Timestamp)
        Index('ix_weatherdata_timestamp_temp',
              self.weather_data.c.Timestamp,
              self.weather_data.c.Temperature)
