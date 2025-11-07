
import logging
from typing import Dict
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from ..models.air_data import SensorReading
from ..dependencies import verify_credentials
from ..publisher import MQTTPublisher
from ..sql_client import SQLClient
from rds import RDSConfig
from ..transformer import SensorDataTransformer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter(include_in_schema=True)
mqtt_publisher = MQTTPublisher()

rds_config = RDSConfig()
sql_agent = SQLClient(rds_config=rds_config)

transformer = SensorDataTransformer()


@app.post("/sensor-data",  response_model=None)
async def receive_sensor_data(
    data: SensorReading,
    background_tasks: BackgroundTasks,
    username: str = Depends(verify_credentials)
) -> Dict[str:str,
          str:SensorReading]:
    """Accepts and processes a post request with a predefined typified JSON object.

    Raises:
        HTTPException

    Returns:
        dict: debug data if testing locally.
    """
    try:
        # convert Pydantic model to dict
        result_dict = transformer.transform_to_dict(data)

        try:
            background_tasks.add_task(
                mqtt_publisher.connect
            )
            background_tasks.add_task(
                mqtt_publisher.publish_payload,
                result_dict
            )
            background_tasks.add_task(
                sql_agent.store_payload,
                result_dict
            )
        finally:
            mqtt_publisher.disconnect()

        return {
            "status": "success",
            "message": f"Sensor data received from {username} and will be published to MQTT",
            "data": result_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sensor data: {str(e)}")


@app.get("/", response_model=None)
async def root(username: str = Depends(verify_credentials)) -> Dict[str:str,
                                                                    str:str]:
    """root level path. Requires you to be logged in.

    Returns:
        dict: _description_
    """
    return {
        "message": "Sensor Data API is running. POST your data to /sensor-data/",
        "authenticated_as": username
    }
