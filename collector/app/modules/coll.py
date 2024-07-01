"""
    FUZE
    AI Ruleness SIEM for OT/ICS
    Copyright (C) Zakhar Bernhardt 2022

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Description:
        Collector module for FUZE Core.
        Get Messages from Remote Collectors.
        Send messages to next module Normalizator.
"""

import json
import asyncio
import logging
from datetime import datetime
from .collector.syslog import SyslogServer
from .tran import Transmitter

class Collector:
    """
    Module takes Data from Collectors and create Messages.
    """
    def __init__(self, config, messages):
        self.config = config
        self.queue_messages = messages
        self.coroutines = {}

    async def start(self):
        """
        Start Server to receive Messages from Collectors
        """
        try:
            await self.create_coroutines()
            await self.start_tasks()
            while True:
                await asyncio.sleep(300)
                await self.restart_tasks()
        except Exception as e:
            logging.error(f'[-] COLL: {repr(e)}')

    async def create_coroutines(self):
        """
        Create coroutines with queues
        """
        for module in self.config:
            module_name = module['name']
            module_config = module['config']
            if module_name == 'syslog':
                syslog = SyslogServer(module_config, self.queue_messages)
                self.coroutines['syslog'] = syslog.start()

    async def start_tasks(self):
        """
        Create the Tasks
        """
        self.tasks = {}
        for k, v in self.coroutines.items():
            self.tasks[k] = asyncio.create_task(v, name=k)
            logging.info(f'[*] COLL: Start module: {k}')

    async def restart_tasks(self):
        """
        Restart the Task if an Exception occurs
        """
        for k, v in self.tasks.items():
            if v.done():
                logging.error(f'[-] COL: Restart module: {k}')
                cor = self.coroutines[k]
                self.tasks[k] = self.loop.create_task(cor, name=k)
