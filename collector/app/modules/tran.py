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
        Save Messages, Events, Alerts, Incidents from Modules to DB
"""

import json
import asyncio
import logging
import socket
import zlib

class Transmitter:
    """
    Module takes Messages from Modules and send them to another FUZE Collector.
    """
    def __init__(self, config, messages=None):
        self.config = config
        self.queue_messages = messages
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def parse_config(self, config):
        """
        Parse config
        """
        rules = []
        if ('host' not in config or
            'port' not in config or
            'collector_name' not in config):
            raise Exception('[-] TRAN: Bad configuration file, exiting')
        self.server_host = config['host']
        self.server_port = int(config['port'])
        self.collector_name = config['collector_name']

    async def start(self):
        try:
            self.parse_config(self.config)
            while True:
                await asyncio.sleep(5)
                raw_messages = []
                while not self.queue_messages.empty():
                    raw_messages.append(await self.queue_messages.get())
                if raw_messages:
                    messages = await self.agregate_messages(raw_messages)
                    await self.send_messages(messages)
        except Exception as e:
            logging.error(f'TRAN: {repr(e)}')

    async def agregate_messages(self, raw_messages):
        logging.debug(f'[+] TRAN: agregating {len(raw_messages)}')
        messages_map = {}
        for raw_message in raw_messages:
            uniq = raw_message['src_ip'] + raw_message['data']
            if uniq in messages_map:
                messages_map[uniq]['count'] += 1
            else:
                raw_message['count'] = 1
                messages_map[uniq] = raw_message
        messages = [ x for x in messages_map.values() ]
        return messages

    async def send_messages(self, messages):
        logging.debug(f'[+] TRAN: sending {len(messages)}')
        logging.debug(json.dumps(messages, indent=4, default=str))
        data = {
            'collector': self.collector_name,
            'messages': messages
        }
        data = json.dumps(data, default=str).encode('utf-8')
        compressed_data = zlib.compress(data)
        logging.debug(f'[+] TRAN: sending to {self.server_host}:{self.server_port}')
        self.sock.sendto(compressed_data, (self.server_host, self.server_port))
