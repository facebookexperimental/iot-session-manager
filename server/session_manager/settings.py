# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
This Settings file configures the project by setting variables and other configurations.
For certain settings, the file checks for environment variables that enable the application
to be configured during deployment from env variables provided by docker.
"""


import logging
import os
import json
from logging.handlers import TimedRotatingFileHandler

# BASE PATH can be set from enviornment variables if the app is run from a different directory than source
if os.environ.get("BASE_PATH"):
    BASE_DIR = os.getcwd() + str(os.environ.get("BASE_PATH"))
else:
    BASE_DIR = os.getcwd()

logging.basicConfig(level="INFO")
logger = logging.getLogger()


# File Logging will only be used if the FILE_LOGGING env variable is set, otherwise console logging will be used.
if os.environ.get("FILE_LOGGING"):
    time_handler = TimedRotatingFileHandler(
        BASE_DIR + "/logs/serverlogs.log", when="d", interval=1, backupCount=5
    )
    logger.addHandler(time_handler)


# Tornado app port setup. The IoT and Admin servers utilized differnet ports to enable separate access permissions
IOT_PORT = 8888
ADMIN_PORT = 50001

# Session Manager settings
# configures the number of digits in the session ID and PIN to balance usability and security.
ID_SIZE = 6
PIN_SIZE = 3

# Session storage will be written to a file named SESSION_STORAGE. If S3_BUCKET variable is set, S3 will be used for storage.
SESSION_STORAGE = 'session_data.json'
S3_BUCKET = os.environ.get('S3_BUCKET')
S3_DATA_ROOT = 'session_manager/'


# MQTT JWT authentication setup
JWT_MODE = os.environ.get('MQTT_AUTH_MODE')  # Provided from docker compose from .env file - dev_no_auth, dev_jwt_auth, kms_jwt_auth

# If no environmental variable is set, no authentication will be used
if not JWT_MODE:
    JWT_MODE = 'dev_no_auth'
    JWT_PRIVATE_KEY_LOC = ''
    JWT_PUBLIC_KEY_LOC = ''
elif JWT_MODE == 'dev_jwt_auth':
    # For dev_jwt_auth, a local pair of private and public keys are necessary. The location of those keys is set below:
    JWT_PRIVATE_KEY_LOC = './local_mqtt_keys/private_key.pem'
    JWT_PUBLIC_KEY_LOC = './local_mqtt_keys/public_key.pem'
elif JWT_MODE == 'kms_jwt_auth':
    with open('mqtt_pub_key_info.json', 'rb') as pubdata:
        public_key_data = pubdata.read()
        pub_dict = json.loads(public_key_data)
        AWS_JWT_KEY_ARN = pub_dict["KeyId"]

AWS_REGION = os.environ.get("AWS_REGION")

# Conductor Interfaces - map the Conudctor class to a type name in the dictionary below
from src.conductor.default_conductor import DefaultConductor
from src.conductor.active_conductor import ActiveConductor

CONDUCTOR_INTERFACES = {
    "default" : DefaultConductor,
    "active" : ActiveConductor
}
