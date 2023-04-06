# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging
import time
import json

from src.iot_client import IotClient
from src.session_manager_client import SessionManagerClient

"""
Server Test Script

This script utilizes an Admin client and IoT client to test the server functionality.
The script creates a session as an admin, and then an IoT client joins that session and
publishes a test message to verify the network is working.
"""
with open('config.json', 'rb') as config_file:
    config_data = config_file.read()
    config = json.loads(config_data)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Configure the Session Manager Admin client IP and Port and generate instance
session_mgr_config = {
    "server_url": config.get('server_url')
}
admin_client = SessionManagerClient(session_mgr_config)

# Utilize admin client to create a session
logger.info('CREATING SESSION: START')
session_data = admin_client.create_session()
logger.info(f'CREATING SESSION RESULT: {session_data}')

# Configure iot_client class with IP and port of the auth url and mqtt broker
iot_client = IotClient(config)

# Connect the IoT client to the MQTT Broker
logger.info(f'IOT CONNECT Start: {session_data}')
iot_client.join_session(session_data["id"], session_data["pin"])

# Wait for connection or timeout in 10s
for timeout in range(20):
    if iot_client.connected:
        break
    time.sleep(0.5)

# If client is connected subscribe and publish to a test topic, the message should
# appear in the logs
def test_callback(payload):
    logger.info(f'Test Callback Recieved Message with payload {payload}')

# Simple function to get command line input to publish a message
def test_publish_input():
    print("Test Publishing Messages:")
    print("Enter Topic:")
    topic = input()
    print("Enter Payload:")
    payload = input()
    iot_client.publish(topic, payload)

if iot_client.connected:
    iot_client.topic_subscribe("test_topic", test_callback)
    iot_client.publish("test_topic", "test_payload")
    while True:
        time.sleep(0.5)
        test_publish_input()
else:
    logger.info('Error: Client timed out while connecting')
