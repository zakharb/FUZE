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
        Read the configuration and send it to FUZE

"""
import os
import json

TRANSMITTER_HOST = os.getenv("TRANSMITTER_HOST", '')
TRANSMITTER_PORT = os.getenv("TRANSMITTER_PORT", '')

SYSLOG = os.getenv("SYSLOG", '')
SYSLOG_PORT = os.getenv("SYSLOG_PORT", '')

class Config:
    """
    Read configuration for modules
    """    
    def __init__(self):
        self.collector = {}
        self.transmitter = {}

    def read(self):
        with open('config/config.json', 'r') as f:
            config = json.loads(f.read())
        if 'transmitter' in config:
            transmitter = config['transmitter']
            if type(transmitter) == dict:
                self.transmitter = transmitter
        if 'collector' in config:
            collector = config['collector']
            if type(collector) == list:
                self.collector = collector
