from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    DateTime
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
            Column('Timestamp', DateTime, server_default=text('GETDATE()')),
            Column('Temperature', DECIMAL(5, 2), primary_key=True, nullable=False),
            Column('Pressure', DECIMAL(10, 2), nullable=False),
            Column('Humidity', DECIMAL(5, 2), nullable=False),
            Column('RawData', JSON, nullable=False),
            schema=self.schema_name
        )
