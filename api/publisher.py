import os
import ssl
import json
import asyncio
from typing import Optional
import paho.mqtt.client as mqtt
import logging
from abc import ABC
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class DefaultPublisher(ABC):
    pass


class MQTTPublisher(DefaultPublisher):
    def __init__(self):
        self.client: Optional[mqtt.Client] = None
        self.broker = os.getenv('BROKER_HIVE', '')
        self.port = 8883
        self.username = os.getenv('MQTT_USERNAME', '')
        self.password = os.getenv('MQTT_PASSWORD', '')
        self.topic = os.getenv('MQTT_TOPIC', 'sensor_data')
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("Connected to MQTT broker")
        else:
            logger.error(f"Failed to connect to MQTT broker: {rc}")

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.info("Disconnected from MQTT broker")

    def on_publish(self, client, userdata, mid):
        logger.debug(f"Message published with mid: {mid}")

    async def connect(self):
        """Initialize and connect to MQTT broker"""
        if not self.broker:
            logger.warning("MQTT broker not configured, skipping MQTT setup")
            return False

        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_publish = self.on_publish

            # Setup TLS
            self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
            self.client.username_pw_set(self.username, self.password)

            # Connect to broker
            self.client.connect_async(self.broker, self.port, 60)
            self.client.loop_start()

            # Wait for connection with timeout
            for _ in range(50):  # 5 second timeout
                if self.connected:
                    return True
                await asyncio.sleep(0.1)

            logger.error("Timeout waiting for MQTT connection")
            return False

        except Exception as e:
            logger.error(f"Error connecting to MQTT broker: {e}")
            return False

    def publish_payload(self, payload_data: dict):
        """Publish payload to MQTT topic"""
        if not self.client or not self.connected:
            logger.warning("MQTT client not connected, skipping publish")
            return

        try:
            # Convert payload to JSON string
            json_payload = json.dumps(payload_data, default=str)

            # Publish with QoS 1 for guaranteed delivery
            result = self.client.publish(self.topic,
                                         json_payload,
                                         qos=1,
                                         retain=True)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Payload published to {self.topic}")
            else:
                logger.error(f"Failed to publish payload: {result.rc}")

        except Exception as e:
            logger.error(f"Error publishing to MQTT: {e}")

    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
