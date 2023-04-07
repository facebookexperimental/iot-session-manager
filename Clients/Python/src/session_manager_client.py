# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import requests

"""
Session Manager Client

This script acts as the admin to the Session Manager application. It is configured with
the data for the server and provides a set of functions that create, close, and send conductor requests
for sessions.
"""

class SessionManagerClient():
    def __init__(self, config) -> None:
        self._config = config

    def create_session(self):
        response = requests.get(f'https://{self._config["server_url"]}/api/createSession?type=default')
        print(response.content)
        session_data = response.json()
        return session_data

    def close_session(self, session_id):
        response = requests.get(f'https://{self._config["server_url"]}/api/closeSession?id={session_id}')
        success = response.json()
        return success

    def conductor_request(self, session_id, method, params):
        response = requests.get(f'https://{self._config["server_url"]}/api/closeSession?id={session_id}&method={method}&params={params}')
        response = response.json()
        return response
