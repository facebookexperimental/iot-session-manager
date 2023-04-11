# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import asyncio
import json
import logging

import tornado.web

from src.session_manager import SessionManager
from settings import IOT_PORT, ADMIN_PORT


"""
Tornado HTTP Server

This file provides two http servers:
- Admin server for creating/closing sessions and performing conductor requests.
- IoT server for connecting clients to session via session ID and Pin
"""

logger = logging.getLogger()

manager = SessionManager() # Creates referance to the singleton SessionManager class

"""
Session Manager Admin Server:

The admin server is intended to be used by trusted clients for the control of
sessions. This server is published to a different port than the IoT server and provides
API requests for creating and closing sessions, as well as submitting requests to the
active conductor for that session.
"""

# Returns tornado application with routes and respective handlers
def make_admin_app():
    return tornado.web.Application(
        [
            (r"/api/createSession", CreateSessionHandler),
            (r"/api/closeSession", CloseSessionHandler),
            (r"/api/conductorRequest", ConductorRequestHandler),
        ]
    )


# Creates the asyncio based tornado server listening on the specified port
async def start_admin_async_server():
    admin_app = make_admin_app()
    logger.info(f"Starting admin tornado server on port: {ADMIN_PORT}")
    admin_app.listen(ADMIN_PORT)
    await asyncio.Event().wait()

# Custom Decorator Authentication
# An example of how this could work to restrict access based on the request
def example_auth_decorator(func):
    def wrapper_decorator(*args, **kwargs):
        request = args[0].request
        # Do something with request
        if request:
            value = func(*args, **kwargs)
            return value
        else:
            logger.warn(f'Error: Request rejected from auth decorator')
    return wrapper_decorator


"""
    Route: /createSession
    Input:
        -type: string - the session type which dictates what type of conductor will be used
    Outputs:
        -id: string - session ID generated by app
        -pin: string - the pin for the session
        -type: string - same session type as above
"""
class CreateSessionHandler(tornado.web.RequestHandler):
    @example_auth_decorator
    def get(self):
        session_type = self.get_argument('type')
        session = manager.create_session(session_type)
        self.write(json.dumps(session,default=lambda o: o.encode()))


"""
    Route: /closeSession
    Input:
        -id: string - the session id for the session that will be closed
    Outputs:
        -success: string - Success or Error message
"""
class CloseSessionHandler(tornado.web.RequestHandler):
    def get(self):
        session_id = self.get_argument('id')
        closed= manager.close_session(session_id)
        self.write(json.dumps("Success" if closed else "Error"))


"""
    Route: /conductorRequest
    Input:
        -id: string - the session id for the session to recieve the request
        -method: string - the method name that will be sent to the conductor
        -params: string - json formatted parameters for the method
    Outputs:
        -response: string - json encoded response dictionary returned from the conductor
"""
class ConductorRequestHandler(tornado.web.RequestHandler):
    def get(self):
        session_id = self.get_argument('id')
        method = self.get_argument('method')
        params = self.get_argument('params',default=None)
        response = manager.session_conductor_request(session_id, method, params)
        self.write(json.dumps(response))


"""
Session Manager IoT Node Entrypoint Server:

This server provides any client with access to join a session, given a session ID and Pin.
It is intended that this endpoint is available more broadly than the admin server.
"""

# Returns tornado application with routes and respective handlers
def make_iot_app():
    return tornado.web.Application(
        [
            (r"/api/joinSession", JoinSessionHandler),
        ]
    )


# Creates the asyncio based tornado server listening on the specified port
async def start_iot_async_server():
    iot_app = make_iot_app()
    logger.info(f"Starting iot tornado server on port: {IOT_PORT}")
    iot_app.listen(IOT_PORT)
    await asyncio.Event().wait()


"""
    Route: /joinSession
    Input:
        -id: string - the session id for the session to recieve the request
        -pin: string - the session pin for the session, used for authenticating
        -client: string - the client id that will be added to the JWT token
    Outputs:
        -token: string - JWT token or placeholder returned from the API
"""
class JoinSessionHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self, *args):
        self.set_status(204)
        self.finish()

    def post(self):
        try:
            data = json.loads(self.request.body)
            session_id = data.get('id')
            session_pin = data.get('pin')
            client = data.get('client')
            token = manager.join_session(session_id, session_pin, client)
            logger.info(f"Client {client} Joining Session: {session_id}")
            response = {"token":token}
            self.write(json.dumps(response))
        except Exception:
            logger.info(f'Error decoding request body:')
            logger.info(self.request.body)
            self.write(json.dumps('Error decoding request body:'))
