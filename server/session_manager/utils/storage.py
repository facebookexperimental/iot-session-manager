# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import logging

import settings
from utils.boto3_helpers import load_s3_file, save_s3_file

logger = logging.getLogger()

# Session specific storage helpers

def load_sessions_file():
    if settings.S3_BUCKET:
        return load_s3_file(settings.SESSION_STORAGE)
    else:
        return load_from_local_file(settings.SESSION_STORAGE)


def save_sessions(sessions):
    data = json.dumps(sessions, default=lambda o: o.encode(), indent=4)
    if settings.S3_BUCKET:
        return save_s3_file(settings.SESSION_STORAGE, data)
    else:
        return save_local_file(settings.SESSION_STORAGE, data)

# Local file storage helpers

def load_from_local_file(file_path)->dict:
    try:
        with open(file_path) as readfile:
            txt = readfile.read()
            logger.info(f"Read session data text {txt}")
            return json.loads(txt)

    except Exception as e:
        logger.info(f'Could not load sessions from local file: {file_path}:{e}')
        return {}

def save_local_file(file_path, data)->bool:
    try:
        logger.info('Saving local file')
        with open(file_path, "w+") as outfile:
            outfile.write(data)
            return True
    except Exception as e:
        logger.warning(f'Could not save local file with path ${file_path}')
        logger.warning(e)
        return False
