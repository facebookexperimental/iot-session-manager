# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging

logger = logging.getLogger()


"""
This Default Conductor is an example of a session conductor that can be attached to a running session.
This class is meant to be sub-classed to provide real-time advanced functionality of the session.

This primary function of the conductor class is to provide request methods to the admin server via the
/conductorRequest route.

Each conductor class should expose a serializable API that describes which
reqeust methods it recieves, and what parameters are required for those methods.
The conductor class should then register function handlers for these requests in the request_handlers
method.

"""


BASE_API = [
    {"method": "state", "params": []},
    {"method": "start", "params": []},
    {"method": "stop", "params": []},
]

class DefaultConductor():
    def __init__(self, session):
        self.session_id = session.id
        self.request_api = BASE_API
        self.request_handlers = {
            "state" : self.get_state,
            "start" : self.start,
            "stop" : self.stop
        }
        logger.info(f"Starting Conductor for session {self.session_id}")

    # request method does not need to be overwritten by extended classes
    def request(self, method, params):
        logger.info(f"Conductor request recieved for {method} with params {params}")
        fnc = self.request_handlers.get(method)
        if fnc:
            return fnc(params)
        else:
            logger.warn(f"No handler function registered for method: {method}")
            return f"Error: No handler function registered for method: {method}"

    def print_api(self):
        return json.dumps(self.request_api)

    """
    The default conductor does not do anything significant here, but these methods can be
    overwritten to provide greater functionality.
    """
    def get_state(self, params):
        return "State"

    def start(self, params):
       return "Start"

    def stop(self, params):
        return "Stop"
