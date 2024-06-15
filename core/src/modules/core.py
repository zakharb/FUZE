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
        The Core module to start all tasks
"""

import asyncio
import traceback
import logging

from .coll import Collector
from .norm import Normalizer
from .fuze import Fuzer
from .clas import Classifier
from .reco import Recorder


class Core():
    """
    Main class for FUZE Core
    Create coroutines and start them
    """

    def __init__(self, collector=None, normalizer=None, fuzer=None):
        self.collector = collector
        self.normalizer = normalizer
        self.fuzer = fuzer
        self.tasks = {}

    async def start(self):
        """
        Start CORE
        """
        try:
            logging.info(f'[*] CORE: Starting modules')
            await self.create_coroutines()
            await self.start_tasks()
            while True:
                await asyncio.sleep(300)
                await self.check_tasks()
        except Exception as e:
            logging.debug(traceback.format_exc())
            logging.error(f'[-] CORE: {e}')

    async def create_coroutines(self):
        """
        Create coroutines with queues
        """
        messages = asyncio.Queue()
        messages_out = asyncio.Queue()
        events = asyncio.Queue()
        events_out = asyncio.Queue()
        alerts = asyncio.Queue()
        alerts_out = asyncio.Queue()
        incidents = asyncio.Queue()
        incidents_out = asyncio.Queue()
        collector = Collector(
            config=self.collector, messages=messages, 
            messages_out=messages_out, events=events)
        normalizer = Normalizer(
            config=self.normalizer, messages=messages, 
            events=events, events_out=events_out)
        fuzer = Fuzer(
            config=self.fuzer, events=events, alerts=alerts, 
            alerts_out=alerts_out)
        classifier = Classifier(
            config=self.fuzer, alerts=alerts, 
            incidents=incidents, incidents_out=incidents_out)
        # recorder = Recorder(messages_out=messages_out, events_out=events_out, alerts_out=alerts_out, 
        #                     incidents_out=incidents_out)
        self.coroutines = {
            'Collector': collector.start(),
            'Normalizer': normalizer.start(),
            'Fuzer': fuzer.start(),
            'Classifier': classifier.start(),
            # 'Recorder': recorder.start(),
        }

    async def start_tasks(self):
        """
        Create the Tasks
        """
        self.tasks = {}
        for k, v in self.coroutines.items():
            self.tasks[k] = asyncio.create_task(v, name=k)
            logging.info(f'[+] CORE: Start main module: {k}')

    async def check_tasks(self):
        """
        Restart the Task if an Exception occurs
        """
        for k, v in self.tasks.items():
            if v.done():
                logging.error(f'[-] CORE: Stopping, Error in module: {k}')
                loop = asyncio.get_running_loop()
                loop.stop()
                # cor = self.coroutines[k]
                # self.tasks[k] = self.loop.create_task(cor['func'](*cor['args']), name=k)
