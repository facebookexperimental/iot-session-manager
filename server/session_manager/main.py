# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import asyncio

from src.async_loop import main_loop
from src.http_server import (
    start_admin_async_server,
    start_iot_async_server,
)
from src.async_mqtt_client import AsyncIotClient

"""
Main Application Entrypoint:

When, run this file gathers tasks from the program and starts an asyncio event loop.

This configuration demonstrates how to setup the required IoT server and Admin server.
It also provides a placeholder for a separate asyncio based event loop that is read from the 'async_loop' file.
"""


async def main():
    await asyncio.gather(
        start_iot_async_server(),
        start_admin_async_server(),
        main_loop(),
        AsyncIotClient().run()
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
