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

    def parse_config(self):
        """
        Parse config
        """
        collectors_map = {}
        for collector in self.config:
            if ('name' not in collector or
                'nodes' not in collector):
                continue
            collector_name = collector['name']
            nodes_map = {}
            nodes = collector['nodes']
            for node in nodes:
                if ('name' not in node or 
                    'sensor' not in node or
                    'src_ip' not in node):
                    logging.debug(f'[-] LOG: not full config, skip node: {node}')
                    continue
                ip = node['src_ip']
                nodes_map[ip] = {
                    'name': node['name'],
                    'sensor': node['sensor']
                }
            collectors_map[collector_name] = nodes_map
        return collectors_map

    async def start(self):
        """
        Start Server to receive Messages from Collectors
        """
        try:
            collectors = self.parse_config()
            loop = asyncio.get_running_loop()
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: EchoServerProtocol(collectors, self.queue_messages),
                local_addr=(self.IP, self.PORT))
            while True:
                await asyncio.sleep(300)
        except Exception as e:
            logging.error(f'[-] COLL: {repr(e)}')


class EchoServerProtocol:
    def __init__(self, collectors, queue_messages):
        self.collectors = collectors
        self.queue_messages = queue_messages
        self.con_lost = False

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            decompressed_data = zlib.decompress(data)
            decompressed_data = decompressed_data.decode('utf-8')
            data = json.loads(decompressed_data)
            if ('collector' not in data or
                'messages' not in data):
                logging.debug(f'[-] LOG: Unknown data format from collector')
                return
            ip = addr[0]
            collector = data['collector']
            raw_messages = data['messages']
            if collector not in self.collectors:
                logging.debug(f'[-] LOG: Unknown collector: {collector}')
                return
            logging.debug(f'[+] LOG: Get data from collector: {collector}')
            for raw_message in raw_messages:
                ip = raw_message['src_ip']
                ips = self.collectors[collector]
                if ip not in ips:
                    logging.debug(f'[-] LOG: Unknown ip: {ip}')
                    return
                node = ips[ip]['name']
                sensor = ips[ip]['sensor']
                message = {
                    'time': raw_message['time'],
                    'sensor': sensor,
                    'collector': collector, 
                    'node': node,
                    'src_ip': raw_message['src_ip'],
                    'data': raw_message['data'],
                }
            self.queue_messages.put_nowait(message)
        except Exception as e:
            logging.error(f'[-] LOG: {repr(e)}')

    def connection_lost(self, b):
        self.con_lost = True
