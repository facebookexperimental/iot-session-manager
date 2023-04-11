# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import asyncio
import json
import logging

from src.conductor.default_conductor import DefaultConductor

logger = logging.getLogger()

"""
This Active Conductor is an extension of the default conductor that adds one more request method.
The active conductor also creates its own asyncio based event loop that starts and stops with the
conductor requests.

"""

ACTIVE_CONDUCTOR_API = [
    {"method": "state", "params": []},
    {"method": "start", "params": []},
    {"method": "stop", "params": []},
    {"method": "pause", "params": []},
]

class ActiveConductor(DefaultConductor):
    def __init__(self, session_id):
        super().__init__(session_id)
        self.request_api = ACTIVE_CONDUCTOR_API
        self.request_handlers = {
            "state" : self.get_state,
            "start" : self.start,
            "stop" : self.stop,
            "pause" : self.pause
        }

    async def active_loop(self):
        logger.info("Active Loop Starting")
        while True:
            logger.info("Active Conductor Engaged")
            await asyncio.sleep(10)

    def start(self, params):
        logger.info(f"Active Conductor {self.session_id} Starting Loop")
        self.async_loop = asyncio.create_task(self.active_loop())
        return "Started"

    def stop(self, params):
        self.async_loop.cancel()
        return "Stopped"

    def pause(self, params):
        self.async_loop.cancel()
        return "Stopped"
