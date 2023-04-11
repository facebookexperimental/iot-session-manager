# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import logging
from random import randint

from src.session import Session
from settings import ID_SIZE, PIN_SIZE, SESSION_STORAGE
from utils.jwt_helpers import create_session_token
from utils.storage import load_sessions, save_sessions

logger = logging.getLogger()

'''
Session Manger Class

This class provides the primary application logic manages the instances of the sessions
and provides functions to the API interfaces. The class provides functionality to:
- Create sessions
- Close sessions
- Send Conductor Requests for specific sessions
- Join sessions and validate session ID and Pin for clients.
'''


class SessionManager():
    # Singleton Class
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.sessions = {}
        self.load_sessions()

    '''
    Interface Methods - these are called from the API
    '''
    # Create a new session from session type -> returns session instance
    def create_session(self, session_type: str)->Session:
        new_session = Session(
            self._gen_session_id(), self._gen_session_pin(),  session_type
        )
        self.sessions[new_session.id] = new_session
        logger.info(f"Creating Session: {new_session.id}")
        save_sessions(self.sessions)
        return new_session

    # Close a session from a session id -> returns boolean
    def close_session(self, session_id: str)->bool:
        try:
            del self.sessions[session_id]
            logger.info(f"Deleting session {session_id}")
            save_sessions(self.sessions)
            return True
        except:
            logger.info("Can't close session, session not found")
            return False

    # Conductor requests - passes method name and params to conductor for a given session returns conductor response
    def session_conductor_request(self, session_id:str , method:str , params: str)->str:
        session = self._get_session_from_id(session_id)
        if session:
            return session.conductor_request(method, params)
        else:
            return "Could not locate session"

    # Join a session from a session id and pin, if correct provides a JWT token
    def join_session(self, session_id: str, session_pin: str, client_id: str)->str:
        result = self._validate_session_pin(session_id, session_pin)
        if result:
            logger.info(f"Creating Session Token for client: {client_id} and session {session_id}")
            self._add_client_to_session(session_id, client_id)
            return create_session_token(session_id, client_id)
        else:
            logger.info(f"Could not validate credentials for client: {client_id} and session {session_id}")
            return "Could not validate session credentials"

    '''
    Methods used by app but not exposed to API
    '''
    def load_sessions(self, data=None):
        if not data:
            logger.info("Session Manager loading sessions from file")
            session_data = load_sessions()
        else:
            logger.info("Session Manager loading sessions from data")
            session_data = data
        for session in session_data:
            new_session = Session(session["id"], session["pin"], session["type"])
            self.sessions[new_session.id] = new_session

    def clear_sesssions(self):
        logger.info("Session Manager clearing sessions")
        self.sessions = {}

    '''
    Internal Class Helpers
    '''

    def _get_session_from_id(self, id:str)->Session:
        return self.sessions.get(id)

    def _gen_session_id(self)->str:
        unique = False
        while not unique:
            id = ''.join(["{}".format(randint(0, 9)) for num in range(0, ID_SIZE)])
            if not self._get_session_from_id(id):
                unique = True
        return id

    def _gen_session_pin(self)->str:
        pin = ''.join(["{}".format(randint(0, 9)) for num in range(0, PIN_SIZE)])
        return pin

    def _validate_session_pin(self, session_id: str, session_pin: str)->bool:
        session = self._get_session_from_id(session_id)
        if session:
            if session_pin == session.pin:
                logger.info("Success: Pin validated")
                return True
            else:
                logger.info("Incorrect Session Pin")
                return False
        else:
            logger.info("Could not locate session with that id")
            return False

    def _add_client_to_session(self, session_id: str, client_id: str)->None:
        session = self._get_session_from_id(session_id)
        if client_id not in session.clients:
            session.clients.append(client_id)
            save_sessions(self.sessions)
