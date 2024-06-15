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
        Normalization module for FUZE Core.
        A sensor is required for each type of messages from Collector.
        Searching for necessary Events in Messages.
        Each Event is assigned to a taxonomy:
            object - the object on which the action was performed
                     (application, user, system)
            action - the action that was performed on the object 
                     (start, stop, on, off, delete, add) 
        Then the Events are sent to Fuzer module.

        Collector          Normalizer             Fuzer
        ---------          ----------           --------
         Message     ->      Sensor      ->       Event

"""

import json
import asyncio
import logging
from re import search, sub
from datetime import datetime

import spacy


class Normalizer:
    """
    Takes Messages from Collector and normalize them to Events.
    """
    def __init__(self, config, messages, events, events_out):
        self.config = config
        self.queue_messages = messages
        self.queue_events = events
        self.queue_events_out = events_out
        self.sensor_types = {
            'syslog' : self.normalize_syslog,
        }
        #self.nlp = spacy.load("en_core_web_sm")


    async def start(self):
        """
        Start a main Task
        Get Messages from queue
        Filter them through Sensor's Rules
        """
        try:
            self.loop = asyncio.get_running_loop()
            # self.read_config()
            while True:
                message = await self.queue_messages.get()
                if message['sensor'] in self.sensor_types:
                    sensor = self.sensor_types[message['sensor']]
                    #['sensor_type']
                    #self.alerts = self.config[sensor]['alerts']
                    alert = sensor(message)
                    if alert:
                        await self.queue_events.put(alert)
                        #await self.queue_events_out.put(alert)
        except Exception as e:
            logging.error(f'[-] NORM: {repr(e)}')

    def normalize_syslog(self, message):
        """
        Syslog sensor
        """
        data = {}
        # sensor = self.config[message['sensor']]
        tax_main = 'ids'
        sensor = {
            'Configured': {
                'tax': 'http:request',
            }
        }
        for key, value in sensor.items():
            if key in message['data']:
                data = {
                    'node': message['node'],
                    'src_ip': message['src_ip'],
                    'time': message['time'],
                    'data': message['data'],
                    'collector': message['collector'],
                    'tax': tax_main + ':' + value['tax'],
                }
                return data

        # # Sample text
        # text = "Configured from console by admin on vty0 (192.168.1.100)"

        # # Process the text
        # doc = self.nlp(message['data'])
        # print(doc)
        # # Print entities
        # for ent in doc.ents:
        #     print(ent.text, ent.label_)


        # text = ("When Sebastian Thrun started working on self-driving cars at "
        #         "Google in 2007, few people outside of the company took him "
        #         "seriously. “I can tell you very senior CEOs of major American "
        #         "car companies would shake my hand and turn away because I wasn’t "
        #         "worth talking to,” said Thrun, in an interview with Recode earlier "
        #         "this week.")
        # doc = self.nlp(text)

        # # Analyze syntax
        # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

        # # Find named entities, phrases and concepts
        # for entity in doc.ents:
        #     print(entity.text, entity.label_)

