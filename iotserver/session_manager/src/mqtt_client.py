# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Singleton MQTT Client class

from utils.jwt_helpers import create_server_token

class AsyncIotClient():
    # Singleton Class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AsyncIotClient, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.hostname = "host"
        self.token = create_server_token(self.hostname)

    # TODO set timer to refresh token before expiration
