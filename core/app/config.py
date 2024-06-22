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
import json

class Config:
    """
    Read configuration for modules
    """    
    def __init__(self):
        self.core = {}
        self.collector = {}
        self.normalizer = []
        self.fuzer = []

    def read(self):
        with open('config/config.json', 'r') as f:
            config = json.loads(f.read())
        if 'core' in config:
            if type(config['core']) == dict:
                self.core = config['core']
        if 'collector' in config:
            if type(config['collector']) == dict:
                self.collector = config['collector']
        if 'normalizer' in config:
            if type(config['normalizer']) == list:
                self.normalizer = config['normalizer']
        if 'fuzer' in config:
            if type(config['fuzer']) == list:
                self.fuzer = config['fuzer']
