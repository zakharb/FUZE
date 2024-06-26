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
        Classification module for FUZE Core.
        Module takes meta alerts from Fusion and create Incidents.

        Correlator          Classification         Recorder
        ----------          ----------           -----------
           Event    ->           AI        ->      Incident
"""
import json
import asyncio
import logging
import datetime
import logging

# from .repo import AIRepo


class Classifier:
    """
    Takes Alerts from Fuzer and check Incidents using AI.
    """

    def __init__(self, config, alerts, incidents=None, incidents_out=None):
        self.config = config
        self.queue_alerts = alerts
        self.queue_incidents = incidents
        self.queue_incidents_out = incidents_out

    def parse_config(self, config):
        """
        Parse config
        """
        pass

    async def start(self):
        """
        Start a main Task
        Get Alerts from Queue
        Classificate them through AI and remove False Positives
        """
        try:
            self.parse_config(self.config)
            #repo = AIRepo()
            # incidents = await repo.read('incidents')
            data = {}
            rules = self.parse_config(self.config)
            while True:
                alert = await self.queue_incidents.get()
                logging.info('[*] CLAS: got alert', event)
                name = alert['name']
                inc_filter = rules[name]
                positive = True
                for tax, fields in inc_filter.items():
                    event = alert['events'][tax]
                    uniq = name + event['collector'] + event['node']
                    for field in fields:
                        uniq_field = event['fields'].get(field)
                        if uniq_field:
                            uniq += uniq_field
                    if uniq not in incidents:
                        incidents[uniq] = datetime.datetime.now()
                        positive = True
                    else:
                        time_delta = datetime.datetime.now() - datetime.timedelta(days=1)
                        if incidents[uniq] < time_delta:
                            incidents[uniq] = datetime.datetime.now()
                        else:
                            positive = False
                if positive:
                    await self.send_incident(alert)
                incidents_uniq = {}
                for uniq, time in incidents.items():
                    time_delta = datetime.datetime.now() - datetime.timedelta(days=3)
                    if time > time_delta:
                        incidents_uniq[uniq] = time
                incidents = incidents_uniq
                logging.debug(json.dumps(incidents, indent=4, defaut=str))
                # await repo.update('incidents', incidents)
        except Exception as e:
            logging.error(f'[-] CLAS: {repr(e)}')

    async def send_incident(self, alert):
        incident = {
            'time': alert['end_time'],
            'name': alert['name'],
            'desc': alert['desc'],
            'tactic': alert['tactic'],
            'severity': alert['severity'],
            'events': alert['events'],
        }
        await self.queue_incidents_out.put(incident)

    def parse_config(self, config_raw):
        """
        Parse configuration
        """
        rules = {}
        for data in config_raw:
            if ('name' not in data or 
                'events' not in data):
                continue
            rules[data['name']] = {}
            for event in data['events']:
                if 'inc_filter' not in event:
                    continue
                if event['inc_filter']:
                    tax = f"{event['tax_main']}:{event['tax_object']}:{event['tax_action']}"
                    fields = event['inc_filter'].split(',')
                    rules[data['name']][tax] = [x.strip() for x in fields]
        return rules
