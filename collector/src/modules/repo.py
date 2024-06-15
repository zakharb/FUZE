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
        Repository module to work with DB.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_URI = os.getenv("DATABASE_URI", "mongodb://root:root@localhost:27017/")

class BaseRepo:
    """
    Write Data to the Database.
    """
    def __init__(self):
        client = AsyncIOMotorClient(DATABASE_URI)
        self.db = client['db']

    async def dropdb(self):
        await self.db.drop_collection('messages')
        await self.db.create_collection(
            'messages',
            timeseries={
                'timeField': 'time',
                'metaField': 'node',
                'granularity': 'seconds',
            },
            expireAfterSeconds=31536000)
        await self.db.drop_collection('events')
        await self.db.create_collection(
            'events',
            timeseries={
                'timeField': 'time',
                'metaField': 'node',
                'granularity': 'seconds',
            },
            expireAfterSeconds=31536000)
        await self.db.drop_collection('alerts')
        await self.db.create_collection(
            'alerts',
            timeseries={
                'timeField': 'time',
                'granularity': 'seconds',
            },
            expireAfterSeconds=31536000)
        await self.db.drop_collection('incidents')
        await self.db.create_collection(
            'incidents',
            timeseries={
                'timeField': 'time',
                'granularity': 'seconds',
            },
            expireAfterSeconds=2592000)
        await self.db.drop_collection('ml')
        await self.db.drop_collection('ai')


class MessageRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    async def write(self, data):
        """
        Write messages to the database.
        """
        logging.debug(f'[+] REPO: Writing messages to DB: {len(data)}')
        await self.db['messages'].insert_many(data)


class EventRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    async def write(self, data):
        """
        Write events to the database.
        """
        logging.debug(f'[+] REPO: Write events to DB: {len(data)}')
        await self.db['events'].insert_many(data)


class AlertRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    async def write(self, data):
        """
        Write meta events to the database.
        """
        logging.debug(f'[+] REPO: Write meta events to DB: {len(data)}')
        await self.db['alerts'].insert_many(data)


class IncidentRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    async def write(self, data):
        """
        Write incidents to the database.
        """
        logging.debug(f'[+] REPO: Write incidents to DB: {len(data)}')
        await self.db['incidents'].insert_many(data)

class AIRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    async def write(self, data):
        """
        Write incidents to the database.
        """
        logging.debug(f'[+] REPO: Write AI models to DB: {len(data)}')
        await self.db['ai'].insert_many(data)
