from attrs import define, field
import logging
from dotenv import load_dotenv
from rds import RDSConfig
from api.models.db_model import WeatherData

load_dotenv()
logger = logging.getLogger(__name__)


@define
class SQLClient:
    rds_config: RDSConfig = field(kw_only=True)
    db_engine = field(init=False, default=None)

    def __attrs_post_init__(self):
        self.db_engine = self.rds_config.get_engine()

    def store_payload(self, payload_data: dict):
        try:
            with self.db_engine.connect() as conn:
                data_model = WeatherData(schema_name='dbo')
                data_model.metadata.create_all(self.db_engine)

                conn.execute(data_model.weather_data.insert(), payload_data)
                conn.commit()
                conn.close()

        except Exception as e:
            logger.error(f"Error storing to database: {e}")
