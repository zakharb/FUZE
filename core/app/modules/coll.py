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
import zlib

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
        self.PORT = 55514

    async def start(self):
        """
        Start Server to receive Messages from Collectors
        """
        try:
            loop = asyncio.get_running_loop()
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: EchoServerProtocol(self.config, self.queue_messages),
                local_addr=(self.IP, self.PORT))
            while True:
                await asyncio.sleep(3)
                print('col 3 sec')
        except Exception as e:
            logging.error(f'[-] COLL: {repr(e)}')


class EchoServerProtocol:
    def __init__(self, config, queue_messages):
        self.config = config
        self.queue_messages = queue_messages
        self.con_lost = False

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            decompressed_data = zlib.decompress(data)  # Decompress the data
            decompressed_data = decompressed_data.decode('utf-8')
            data = json.loads(decompressed_data)
            if ('collector' not in data or
                'messages' not in data):
                return
            ip = addr[0]
            collector = data['collector']
            raw_messages = data['messages']
            logging.debug(f'[+] LOG: Get data from collector: {collector}')
            for raw_message in raw_messages:
                message = {
                    'time': raw_message['time'],
                    'sensor': raw_message['sensor'],
                    'collector': collector, 
                    'node': raw_message['node'],
                    'src_ip': raw_message['src_ip'],
                    'data': raw_message['data'],
                }
            self.queue_messages.put_nowait(message)
        except Exception as e:
            logging.error(f'[-] LOG: {repr(e)}')

    def connection_lost(self, b):
        self.con_lost = True
