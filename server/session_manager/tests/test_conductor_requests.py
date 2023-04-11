# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import pytest

from src.session_manager import SessionManager
from settings import SESSION_STORAGE
from session_test_data import example_sessions, example_session_data

# Create session manager
manager = SessionManager()


@pytest.fixture(autouse=True)
def setup_session_data():
    manager.clear_sesssions()
    manager.load_sessions(data=example_session_data)

def test_state_request():
    result = manager.session_conductor_request(example_sessions[0]["id"],method='state',params='d')
    assert result == "State" #Base conductor just returns 'State'

def test_start_request():
    result = manager.session_conductor_request(example_sessions[0]["id"],method='start',params='d')
    assert result == "Start" #Base conductor just returns 'Start'

def test_stop_request():
    result = manager.session_conductor_request(example_sessions[0]["id"],method='stop',params='d')
    assert result == "Stop" #Base conductor just returns 'Stop'
