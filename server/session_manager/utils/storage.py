# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import logging

import settings
from utils.boto3_helpers import load_s3_file, save_s3_file

logger = logging.getLogger()

def load_sessions():
    if settings.S3_BUCKET:
        return load_s3_file(settings.SESSION_STORAGE)
    else:
        return load_from_local_file()

def save_sessions(sessions):
    data = json.dumps(sessions, default=lambda o: o.encode(), indent=4)

    if settings.S3_BUCKET:
        return save_s3_file(settings.SESSION_STORAGE, data)
    else:
        return local_file_save_sessions(data)

def load_from_local_file()->dict:
    try:
        with open(settings.SESSION_STORAGE, "w+") as readfile:
            txt = readfile.read()

        return json.loads(txt)
    except Exception:
        return {}

def local_file_save_sessions(data)->bool:
    try:
        with open(settings.SESSION_STORAGE, "w+") as outfile:
            outfile.write(data)
            return True
    except Exception as e:
        logger.warning('Could not save sessions to file')
        logger.warning(e)
        return False
