# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import asyncio
import logging

logger = logging.getLogger()

"""
Main Async Loop Placeholder

Given the async nature of the Tornado HTTP server, it is very easy to add in a separate event loop for the app
to handle the scheduling and implementation of other tasks. This could be used for a variety of tasks, so a placeholder
example is provided below.
"""


async def main_loop():
    while True:
        logger.info("Example Master Event Loop Running")
        await asyncio.sleep(60)
