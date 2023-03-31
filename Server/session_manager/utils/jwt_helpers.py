# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging
import math
import time
from datetime import timedelta
import jwt

import settings

from utils.boto3_helpers import kms_jwt_sign

logger = logging.getLogger()

"""
These JWT Helper functions control the logic to generate the JWT tokens that are used
when clients join IoT sessions.  These tokens are given to clients when the joinSession method
of the Session Manager validates the permissions.

Each JWT token contains a payload which devices the subject, expiration time, and MQTT topic access. This payload
format is custom and defined for the Mosquitto_JWT_auth plugin that is used to deploy the broker.

The tokens vary depending on the deployment mode of the application:
- dev_no_auth
        - there are no real tokens and a placeholder is given of the format 'client_id:session_id'
- dev_jwt_auth
        - local RSA keys are used to sign and generate tokens via the py_jwt library.
- kms_jwt_auth
        - the AWS KMS service is used to store a private key and sign the token.
        - The boto3_helpers file handles this implementation.
"""

def create_session_token_payload(session_id, client_id):
    issued = math.floor(time.time())
    expiration = round(issued + timedelta(days=1).total_seconds())
    acl_payload = {
        "sub": client_id, # This client_id must match what the device uses as the mqtt username
        "iat": issued,
        "exp": expiration,
        "subs": [f"/{session_id}/#"], # Clients are restricted to communicating within their sessions topic.
        "publ": [f"/{session_id}/#"],
    }
    return acl_payload

# Create session token based on the mode set from settings and environment variables during deployment
def create_session_token(session_id, client_id):
    acl_payload = create_session_token_payload(session_id, client_id)
    if settings.JWT_MODE == 'dev_jwt_auth':
        return py_jwt_sign(acl_payload)
    elif settings.JWT_MODE == 'dev_no_auth':
        return f'{client_id}:{session_id}'
    elif settings.JWT_MODE == 'kms_jwt_auth':
        return kms_jwt_sign(acl_payload)

"""
PyJWT token methods for dev_jwt_auth
"""

def py_jwt_sign(acl_payload):
    with open(settings.JWT_PRIVATE_KEY_LOC, 'rb') as privatefile:
        private_key = privatefile.read()
    return jwt.encode(acl_payload, private_key, algorithm="RS256")


def py_jwt_verify(token):
    try:
        logger.info('[TOKEN] Validating Token')
        decoded_payload = jwt.decode(token, get_public_key(), algorithms=["RS256"])
        logger.info('[TOKEN] Token Validated')
        return True
    except:
        logger.info('[TOKEN] FAILURE Token Failed')
        return False


def get_public_key():
    with open(settings.JWT_PUBLIC_KEY_LOC , 'rb') as publicfile:
        return publicfile.read()
