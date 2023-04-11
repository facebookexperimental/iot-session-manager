# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Singleton MQTT Client class

from utils.jwt_helpers import create_server_token
import asyncio_mqtt as aiomqtt
import logging
logger = logging.getLogger()

class AsyncIotClient():
    # Singleton Class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AsyncIotClient, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.servername = "iotserver"
        self.token = create_server_token(self.servername)


    async def run(self):
        try:
            async with aiomqtt.Client(
                hostname="mqtt",
                port=1883,
                transport="tcp",
                username=self.servername,
                password=self.token,
            ) as self.client:
                async with self.client.messages() as messages:
                    await self.client.subscribe("#")
                    #await self.client.subscribe("$SYS/#")
                    async for message in messages:
                        logger.info(f"MQTT Message: {message.topic}: {message.payload}")
        except Exception as e:
            logger.error(f"MQTT Client Error: {e}")
