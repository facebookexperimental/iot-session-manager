# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json

from tornado.testing import AsyncHTTPTestCase

from src.session_manager import SessionManager
from src.http_server import make_admin_app, make_iot_app
from session_test_data import example_sessions

class TestAdminApp(AsyncHTTPTestCase):
    def get_app(self):
        return make_admin_app()

    def test_createSession(self):
        session_type = 'default'
        response = self.fetch(f'/api/createSession?type={session_type}')
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data["type"], 'default')

    def test_createActiveSession(self):
        session_type = 'active'
        response = self.fetch(f'/api/createSession?type={session_type}')
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data["type"], 'active')

    def test_close_session(self):
        manager = SessionManager()
        manager.load_sessions(data=example_sessions)
        session_id = example_sessions[1]["id"]
        response = self.fetch(f'/api/closeSession?id={session_id}')
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data, 'Success')

    def test_http_conductor_request_no_params(self):
        manager = SessionManager()
        manager.load_sessions(data=example_sessions)
        session_id = example_sessions[1]["id"]
        response = self.fetch(f'/api/conductorRequest?id={session_id}&method=start')
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data, 'Start')

class TestIoTApp(AsyncHTTPTestCase):
    def get_app(self):
        return make_iot_app()

    def test_joinSession(self):
        manager = SessionManager()
        manager.load_sessions(data=example_sessions)
        session_id = example_sessions[1]["id"]
        session_pin = example_sessions[1]["pin"]
        client_id = 'testClient'
        body_data = {
            "client": client_id,
            "id": session_id,
            "pin": session_pin
        }
        response = self.fetch(f'/api/joinSession', method="POST", body=json.dumps(body_data))
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data["token"], f'{client_id}')

    def test_joinSessionNoPin(self):
        manager = SessionManager()
        manager.load_sessions(data=example_sessions)
        session_id = example_sessions[1]["id"]
        session_pin = example_sessions[1]["pin"]
        client_id = 'testClient'
        body_data = {
            "client": client_id,
            "id": session_id,
        }
        response = self.fetch(f'/api/joinSession', method="POST", body=json.dumps(body_data))
        data = json.loads(response.body)
        self.assertEqual(data["token"],"Could not validate session credentials" )
