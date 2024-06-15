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

class Collector:
    """
    Module takes Data from Collectors and create Messages.
    """
    def __init__(self, config, messages, messages_out, events):
        self.config = config
        self.queue_messages = messages
        self.queue_messages_out = messages_out
        self.queue_events = events
        self.IP = "0.0.0.0"
        self.PORT = 514

    async def start(self):
        """
        Start Server to receive Messages from Collectors
        """
        try:
            # self.create_coroutines()
            # self.start_tasks()
            loop = asyncio.get_running_loop()
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: EchoServerProtocol(self.config, self.queue_messages),
                local_addr=(self.IP, self.PORT))
            while True:
                await asyncio.sleep(3)
                print('col 3 sec')
                # await self.restart_tasks()
        except Exception as e:
            logging.error(f'[-] COLL: {e}')

    def create_coroutines(self):
        """
        Create coroutines with queues
        """
        server = SyslogServer(self.config, self.queue_messages)
        self.coroutines = {
            'server': server.start()
        }

    def start_tasks(self):
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

class EchoServerProtocol:
    def __init__(self, config, queue_messages):
        self.config = config
        self.queue_messages = queue_messages
        self.con_lost = False

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            data = data[:1024].decode('utf-8')
            ip = addr[0]
            if ip in '127.0.0.1':
                node = 'localhost'
                message = {
                    'time': datetime.now()
                    'sensor':'syslog',
                    'collector': 'collector1', 
                    'node': 'node1',
                    'src_ip': '127.0.0.1',
                    'data': data,
                }
            logging.debug(message)
            self.queue_messages.put_nowait(message)
        except Exception as e:
            logging.error(f'[-] LOG: {e}')

    def connection_lost(self, b):
        self.con_lost = True
