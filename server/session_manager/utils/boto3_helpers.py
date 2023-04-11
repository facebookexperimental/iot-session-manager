# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import base64
import json
import logging

import boto3

import settings

logger = logging.getLogger()

'''
    Helper functions for using AWS KMS & BOTO3 to sign and validate JWT tokens
'''

# AWS KMS Sign API: https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html
def kms_jwt_sign(payload):
    header = {"alg":"RS256", "typ":"JWT"}
    token_components = {
        "header": base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("="),
        "payload": base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("="),
    }
    message = f'{token_components.get("header")}.{token_components.get("payload")}'
    logger.info('[KMS] Starting KMS JWT Signing')
    client = boto3.client('kms', region_name=settings.AWS_REGION)
    response = client.sign(
        KeyId = settings.AWS_JWT_KEY_ARN,
        Message = message.encode(),#Base64 encoded binary data object
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256" #String From list of options in KWS API
    )
    logger.info('[KMS] Ending KMS JWT Signing')
    token_components["signature"] = base64.urlsafe_b64encode(response["Signature"]).decode().rstrip("=")
    return f'{token_components.get("header")}.{token_components.get("payload")}.{token_components["signature"]}'


def kms_verify_token(token):
    logger.info('[KMS] Verifying Token')
    client = boto3.client('kms', region_name=settings.AWS_REGION)
    message = f"{token.split('.')[0]}.{token.split('.')[1]}"
    signature_string = token.split('.')[2]+'='
    signature = base64.urlsafe_b64decode(signature_string)
    response = client.verify(
        KeyId=settings.AWS_JWT_KEY_ARN,
        Message=message.encode(),
        MessageType='RAW',
        Signature=signature,
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256"
        )
    valid = response.get('SignatureValid')
    logger.info(f'[KMS] Token Verified: {valid}')
    return valid


def save_s3_file(file_path, data):
    try:
        s3 = boto3.client('s3')
        s3.put_object(
        Body=data,
        Bucket=settings.S3_BUCKET,
        Key= settings.S3_DATA_ROOT + file_path
        )
    except Exception as e:
        logger.error(f'Failed to save file to s3 {file_path}: {e}')
        return {}


def load_s3_file(file_path):
    try:
        s3 = boto3.client('s3')
        obj = s3.get_object(
            Bucket=settings.S3_BUCKET,
            Key=settings.S3_DATA_ROOT + file_path)
        file_content = obj['Body'].read().decode('utf-8')
        return json.loads(file_content)
    except Exception as e:
        logger.error(f'Failed to load file from s3 {file_path}: {e}')
        return {}
