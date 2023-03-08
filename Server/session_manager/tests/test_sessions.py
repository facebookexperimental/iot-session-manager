# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import pytest

from settings import ID_SIZE, PIN_SIZE, SESSION_STORAGE
from src.session_manager import SessionManager
from session_test_data import example_sessions
from utils.jwt_helpers import py_jwt_verify

# Create session manager instance
manager = SessionManager()
manager.clear_sesssions()


@pytest.fixture(autouse=True)
def setup_session_data():
    manager.clear_sesssions()
    manager.load_sessions(data=example_sessions)


def test_load_sessions():
    assert len(manager.sessions) == len(example_sessions)

def test_save_sessions():
    response = manager._save_sessions()
    assert response

def test_get_session_from_id():
    session = manager._get_session_from_id(example_sessions[0]["id"])
    assert session.id == example_sessions[0]["id"]
    assert session.pin == example_sessions[0]["pin"]

def test_gen_unique_session_id():
    id = manager._gen_session_id()
    assert len(id) == ID_SIZE

def test_create_session():
    session = manager.create_session('default')
    assert len(session.pin) == PIN_SIZE
    assert len(manager.sessions) == len(example_sessions)+1

def test_close_session():
    success = manager.close_session(example_sessions[0]["id"])
    assert success

def test_close_session_fail():
    success = manager.close_session(123459)
    assert not success


def test_join_session():
    client_id = 'testClient'
    token = manager.join_session(example_sessions[1]["id"], example_sessions[1]["pin"], client_id)
    assert token == f'{client_id}:{example_sessions[1]["id"]}'

def test_join_session_bad_pin():
    token = manager.join_session(example_sessions[1]["id"], 000, 'testClient')
    assert token == "Could not validate session credentials"

def test_join_session_bad_session():
    token = manager.join_session(000, 000, 'testClient')
    assert token == "Could not validate session credentials"
