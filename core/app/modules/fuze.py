"""
    FUZE
    AI Ruleness SIEM for OT/ICS
    Copyright (C) 2022

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
        Fuzer module for FUZE.
        Module takes Events from Normalization and groups them into Alerts.

        Normalization         Fuzer            Classificator
        ----------          ----------          -----------
           Event      ->    Clustering    ->       Alert
"""

import asyncio
import logging
from datetime import timedelta
import logging
import traceback

class Fuzer:
    """
    Takes Events from Normalizer and correlate them into Alerts.
    """

    def __init__(self, config=None, events=None, alerts=None, alerts_out=None):
        self.config = config
        self.queue_events = events
        self.queue_alerts = alerts
        self.queue_alerts_out = alerts_out

    async def start(self):
        """
        Start the main Task
        Get Events from Normalizer
        Correlate and send them to Alerts queue 
        """
        try:
            rules = self.parse_config(self.config)
            while True:
                event = await self.queue_events.get()
                logging.info('[*] FUZE: got event', event)
                if event['tax'] in rules:
                    for rule in rules[event['tax']]:
                        alert = rule(event)
                        if alert:
                            await self.queue_alerts.put(alert)
                            #await self.queue_alerts_out.put(alert)
        except Exception as e:
            logging.debug(traceback.format_exc())
            logging.error(f'[-] FUZE: {repr(e)}')

    def parse_config(self, config_raw):
        """
        Parse config
        """
        rules = []
        for data in config_raw:
            if ('name' not in data
                or 'description' not in data
                or 'events' not in data
                or 'severity' not in data
                or 'tactic' not in data
                or 'timer' not in data):
                continue
            config = {
                'name': data['name'],
                'desc': data['description'],
                'time_window': int(data['timer']),
                'severity': data['severity'],
                'tactic': data['tactic'],
                'taxanomy_set': {},
                'include': {},
            }
            for event in data['events']:
                taxanomy_set = f"{event['tax_main']}:{event['tax_object']}:{event['tax_action']}"
                config['taxanomy_set'] = {
                    taxanomy_set: int(event['count'])
                }
            rule = Rule(config)
            rules.append({
                'taxanomy_set': config['taxanomy_set'],
                'rule': rule,
            })
        rules_map = {}
        for rule in rules:
            for tax in rule['taxanomy_set']:
                if tax in rules_map:
                    rules_map[tax].append(rule['rule'].fuse_event)
                else:
                    rules_map[tax] = [rule['rule'].fuse_event]
        return rules_map


class Rule:
    """
    Rule class for check alerts
    """

    def __init__(self, config):
        self.alerts = {}
        self.name = config['name']
        self.desc = config['desc']
        self.tactic = config['tactic']
        self.include = config['include']
        self.severity = config['severity']
        self.time_window = config['time_window']
        self.taxanomy_set = config['taxanomy_set']
        self.time_delta = timedelta(seconds=config['time_window'])

    def fuse_event(self, event):
        """
        Fuse event to alerts
        """
        alert_id = event['collector'] + event['node']
        # if 'fields' in event:
        #     alert_id += event['fields'].get('src_addr') + \
        #         event['fields'].get('tgt_addr')
        if alert_id not in self.alerts:
            logging.debug('[*] Create new event in alerts')
            count = {event['tax']: 1}
            self.alerts[alert_id] = {
                'init_time': event['time'],
                'end_time': event['time'],
                'taxanomy_set': {event['tax']: 1},
                'events': {
                    event['tax']: event
                }
            }
        else:
            logging.debug('[*] Event in alerts')
            alert = self.alerts[alert_id]
            if event['time'] <= alert['end_time'] + self.time_delta:
                logging.debug('[*] Time is less')
                alert['end_time'] = event['time']
                if event['tax'] in alert['taxanomy_set']:
                    alert['taxanomy_set'][event['tax']] += 1
                else:
                    alert['taxanomy_set'][event['tax']] = 1
                    alert['events'][event['tax']] = event
                logging.debug(
                    f"[*] Adding count to alert: {alert['taxanomy_set'][event['tax']]}")
            else:
                # init alert
                logging.debug('[*] Time is more')
                self.alerts[alert_id] = {
                    'init_time': event['time'],
                    'end_time': event['time'],
                    'taxanomy_set': {event['tax']: 1},
                    'events': {
                        event['tax']: event
                    }
                }
        if self.alerts[alert_id]['taxanomy_set'] == self.taxanomy_set:
            alert = self.alerts[alert_id]
            data = {
                'name': self.name,
                'desc': self.desc,
                'init_time': alert['init_time'],
                'end_time': alert['end_time'],
                'time_window': self.time_window,
                'tactic': self.tactic,
                'severity': self.severity,
                'events': alert['events']
            }
            logging.debug('[+] Got alert')
            logging.debug(data)
            return data
        else:
            logging.debug('[-] Not alert')
            return None
