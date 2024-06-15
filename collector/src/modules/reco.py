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

import asyncio
import logging
from .repo import MessageRepo, AlertRepo, EventRepo, IncidentRepo


class Recorder:
    """
    Module takes Messages, Events, Alerts, Incidents from Modules and write them to DB.
    """
    def __init__(self, messages=None, events=None, 
                 alerts=None, incidents=None):
        self.queue_messages = messages
        self.queue_events = events
        self.queue_alerts = alerts
        self.queue_incidents = incidents
        self.coros = {
            'REPO-write-messages': self.write_messages(),
            'REPO-write-events': self.write_events(),
            'REPO-write-alerts': self.write_alerts(),
            'REPO-write-incidents': self.write_incidents(),
        }

    async def start(self):
        try:
            self.loop = asyncio.get_running_loop()
            self.create_tasks()
            while True:
                await asyncio.sleep(60)
                await self.check_loop()
        except Exception as e:
            logging.error(f'Repo: {e}')

    def create_tasks(self):
        self.tasks = {}
        for coro in self.coros:
            self.tasks[coro] = self.loop.create_task(
                self.coros[coro], name=coro)

    async def check_loop(self):
        for name, task in self.tasks.items():
            if task.done():
                coro = self.coros[name]
                self.tasks[name] = self.loop.create_task(
                    coro['function'](*coro['args']), name=name)
                logging.error('[-] REPO: Restart task: ' + name)

    async def write_messages(self):
        repo = MessageRepo()
        while True:
            try:
                await asyncio.sleep(5)
                data = []
                while not self.queue_messages.empty():
                    data.append(await self.queue_messages.get())
                if data:
                    await repo.write(data)
            except Exception as e:
                logging.error(f'[-] REPO: Write messages: {e}')

    async def write_events(self):
        repo = AlertRepo()
        while True:
            try:
                await asyncio.sleep(10)
                data = []
                while not self.queue_events.empty():
                    data.append(await self.queue_events.get())
                if data:
                    await repo.write(data)
            except Exception as e:
                logging.error(f'Repo: {e}')

    async def write_alerts(self):
        repo = MetaeventRepo()
        while True:
            try:
                await asyncio.sleep(15)
                data = []
                while not self.queue_alerts.empty():
                    data.append(await self.queue_alerts.get())
                if data:
                    await repo.write(data)
            except Exception as e:
                logging.error(f'Repo: {e}')

    async def write_incidents(self):
        repo = IncidentRepo()
        while True:
            try:
                await asyncio.sleep(15)
                data = []
                while not self.queue_incidents.empty():
                    data.append(await self.queue_incidents.get())
                if data:
                    await repo.write(data)
            except Exception as e:
                logging.error(f'Repo: {e}')
