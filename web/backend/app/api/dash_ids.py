from fastapi import APIRouter, Request
from app.db import db
import datetime

router = APIRouter()


@router.get("/severity", response_description="Severity chart")
async def severity(request: Request, timeframe: str = None):
    end_date = datetime.datetime.utcnow()
    if timeframe == '1d':
        start_date = end_date - datetime.timedelta(minutes=1440)
    elif timeframe == '8h':
        start_date = end_date - datetime.timedelta(minutes=480)
    else:
        start_date = end_date - datetime.timedelta(minutes=60)
    query = {"$and": [
        {'time': {'$gte': start_date}}, 
        {'time': {'$lt': end_date}}
    ]}
    parsers = (
            'TCP', 'UDP', 'ICMP', 'HTTP', 'HTTP/JSON', 'HTTP/XML', 'DNS', 'TLSv1', 'TLSv1.2', 'TLSv1.3', 'QUIC', 
            'WireGuard', 'SSH', 'DHCP', 'Modbus/TCP'
    ) 
    unknown = 0
    new = 0
    known_map = []
    unknown_map = []
    messages = await db["messages"].find(query).sort("_id", -1).to_list(length=1000)
    packets = await db["packets"].find(query).sort("_id", -1).to_list(length=1000)
    for message in messages:
        if message['code'] == 'new-002':
            new += 1
    for packet in packets:
        if packet['proto'] not in parsers:
            if packet['proto'] not in unknown_map:
                unknown_map.append(packet['proto'])
        else:
            if packet['proto'] not in known_map:
                known_map.append(packet['proto'])
    known = len(known_map)
    unknown = len(unknown_map)
    total = new + known + unknown
    known = total - new - unknown
    color = (new / total * 5 + unknown / total * 2 + known / total * 1) / 8 * 100 if total != 0 else 0
    data = {
        'bar': {
            'value': severity,
            'color': color,
        },
        'values': [
            {
                'title': 'New',
                'data': new,
                'color': 'text-danger',
            },
            {
                'title': 'Unknown',
                'data': unknown,
                'color': 'text-warning',
            },
            {
                'title': 'Known',
                'data': known,
                'color': 'text-secondary',
            },
        ]
    }
    return data


@router.get("/bubble", response_description="Protocols chart")
async def bubble(request: Request, timeframe: str = None):
    data_map = {}
    data = []
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(minutes=1440)
    query = {"$and": [
        {'time': {'$gte': start_date}}, 
        {'time': {'$lt': end_date}}]
    }
    parsers = (
            'TCP', 'UDP', 'ICMP', 'HTTP', 'HTTP/JSON', 'HTTP/XML', 'DNS', 'TLSv1', 'TLSv1.2', 'TLSv1.3', 'QUIC', 
            'WireGuard', 'SSH', 'DHCP', 'Modbus/TCP'
    ) 
    known_map = {}
    new_map = {}
    unknown_map = {}
    packets = await db["packets"].find(query).sort("_id", -1).to_list(length=1000)
    messages = await db["messages"].find(query).sort("_id", -1).to_list(length=1000)
    for message in messages:
        proto = message['proto']
        if message['code'] == 'new-002':
            if proto not in new_map:
                new_map[proto] = 1
            else:
                new_map[proto] += 1
        else:
            if proto not in known_map:
                known_map[proto] = 1
            else:
                known_map[proto] += 1
    for packet in packets:
        proto = packet['proto']
        if proto in new_map:
            new_map[proto] += 1
            continue
        if proto not in parsers:
            if proto not in unknown_map:
                unknown_map[proto] = 1
            else:
                unknown_map[proto] += 1
    for proto in new_map:
        data_map[proto] = {
            'name': proto, 
            'value': new_map[proto], 
            'radius': new_map[proto] if new_map[proto] < 20 else 20,
            'color': 2
        }
    for proto in unknown_map:
        data_map[proto] = {
            'name': proto, 
            'value': unknown_map[proto], 
            'radius': unknown_map[proto] if unknown_map[proto] < 20 else 20,
            'color': 1
        }
    for proto in known_map:
        data_map[proto] = {
            'name': proto, 
            'value': known_map[proto], 
            'radius': known_map[proto] if known_map[proto] < 20 else 20,
            'color': 0
        }
    data = [x for x in data_map.values()]
    print(data)
    return data

@router.get("/radar", response_description="Radar chart")
async def radar(request: Request, timeframe: str = None):
    dataset1_label = 'Positive'
    dataset3_label = 'Total'
    now = datetime.datetime.utcnow()
    if timeframe == '1h':
        previous_minute = now - datetime.timedelta(minutes=60)
    elif timeframe == '8h':
        previous_minute = now - datetime.timedelta(minutes=480)
    else:
        previous_minute = now - datetime.timedelta(minutes=1440)
    query = {'time': {'$gte': previous_minute}}
    data = await db["incidents"].find(query).to_list(length=1000)
    positive_events = {
        'Discovery': 0.1,
        'Exploit': 0,
        'Escalate': 0,
        'Command': 0,
        'Impact': 0
    }
    total_events = positive_events.copy()
    for d in data:
        if d['tactic'] not in total_events:
            total_events[d['tactic']] = 1
            if d['positive']:
                positive_events[d['tactic']] = 1
            else:
                positive_events[d['tactic']] = 0
        else:
            total_events[d['tactic']] += 1
            if d['positive']:
                positive_events[d['tactic']] += 1
    total_events = {key: value
                    for key, value
                    in sorted(total_events.items(), key=lambda item: item[1])[::-1]}
    labels = [x for x in total_events]
    dataset3_data = [x for x in total_events.values()]
    dataset1_data = []
    for label in labels:
        dataset1_data.append(positive_events[label])
    response_data = {
        'labels': labels,
        'datasets':
        [
            {
                'label': dataset1_label,
                'data': dataset1_data,
                'backgroundColor': [
                    'rgb(255, 69, 58)',
                ],
                'borderWidth': 0
            },
            {
                'label': dataset3_label,
                'data': dataset3_data,
                'backgroundColor': [
                    'rgb(152, 152, 157)',
                ],
                'borderWidth': 0
            },
        ]
    }
    return response_data


@router.get("/sum_chart", response_description="Summary chart")
async def sum_chart(request: Request):
    now = datetime.datetime.now()
    label = 0
    labels = []
    data = []
    for i in range(59, 0, -1):
        start_date = now - datetime.timedelta(minutes=i*24)
        end_date = now - datetime.timedelta(minutes=i*24 - 24)
        query = {"$and": [{'time': {'$gte': start_date}}, {
            'time': {'$lt': end_date}}]}
        events = await db["events"].count_documents(query)
        data.append(events)
        label += events
        minute = (now - datetime.timedelta(minutes=i*24)).minute
        hour = (now - datetime.timedelta(minutes=i*24)).hour
        dt = f"{hour:02d}:{minute:02d}"
        labels.append(dt)
    response_data = {
        'labels':labels,
        'label': label,
        'data': data,
    }
    return response_data


@router.get("/timeline", response_description="Timeline chart full")
async def timeline_chart(request: Request, timeframe: str = None):
    now = datetime.datetime.utcnow()
    labels = []
    dataset1_data = []
    dataset2_data = []
    dataset3_data = []
    if timeframe == '0h':
        start_date = now - datetime.timedelta(minutes=1)
        end_date = now
        query = {"$and": [{'time': {'$gte': start_date}},
                          {'time': {'$lt': end_date}}]}
        messages = await db["messages"].count_documents(query)
        events = await db["events"].count_documents(query)
        query = {"$and": [{'time': {'$gte': start_date}}, {
            'time': {'$lt': end_date}}, {'positive': True}]}
        incidents = await db["incidents"].count_documents(query)
        dataset1_data = messages
        dataset2_data = events
        dataset3_data = incidents
        labels = now.strftime("%H:%M")
    elif timeframe == '8h':
        for i in range(59, 0, -1):
            start_date = now - datetime.timedelta(minutes=i*8)
            end_date = now - datetime.timedelta(minutes=i*8 - 8)
            query = {"$and": [{'time': {'$gte': start_date}},
                              {'time': {'$lt': end_date}}]}
            messages = await db["messages"].count_documents(query)
            events = await db["events"].count_documents(query)
            query = {"$and": [{'time': {'$gte': start_date}}, {
                'time': {'$lt': end_date}}, {'positive': True}]}
            incidents = await db["incidents"].count_documents(query)
            dataset1_data.append(messages)
            dataset2_data.append(events)
            dataset3_data.append(incidents)
            minute = (now - datetime.timedelta(minutes=i*8)).minute
            hour = (now - datetime.timedelta(minutes=i*8)).hour
            dt = f"{hour:02d}:{minute:02d}"
            labels.append(dt)
    elif timeframe == '24h':
        for i in range(59, 0, -1):
            start_date = now - datetime.timedelta(minutes=i*24)
            end_date = now - datetime.timedelta(minutes=i*24 - 24)
            query = {"$and": [{'time': {'$gte': start_date}},
                              {'time': {'$lt': end_date}}]}
            messages = await db["messages"].count_documents(query)
            events = await db["events"].count_documents(query)
            query = {"$and": [{'time': {'$gte': start_date}}, {
                'time': {'$lt': end_date}}, {'positive': True}]}
            incidents = await db["incidents"].count_documents(query)
            dataset1_data.append(messages)
            dataset2_data.append(events)
            dataset3_data.append(incidents)
            minute = (now - datetime.timedelta(minutes=i*24)).minute
            hour = (now - datetime.timedelta(minutes=i*24)).hour
            dt = f"{hour:02d}:{minute:02d}"
            labels.append(dt)
    else:
        for i in range(59, 0, -1):
            start_date = now - datetime.timedelta(minutes=i)
            end_date = now - datetime.timedelta(minutes=i - 1)
            query = {"$and": [{'time': {'$gte': start_date}},
                              {'time': {'$lt': end_date}}]}
            packets = await db["packets"].count_documents(query)
            messages = await db["messages"].count_documents(query)
            query = {"$and": [{'time': {'$gte': start_date}}, {
                'time': {'$lt': end_date}}]}
            events = await db["events"].count_documents(query)
            dataset1_data.append(packets)
            dataset2_data.append(messages)
            dataset3_data.append(events)
            minute = (now - datetime.timedelta(minutes=i)).minute
            hour = (now - datetime.timedelta(minutes=i)).hour
            dt = f"{hour:02d}:{minute:02d}"
            labels.append(dt)
    response_data = {
        'labels': labels,
        'datasets': [
          {
              'label': 'Events',
              'data': dataset3_data,
              'color': 'rgb(255, 159, 10)',
              'fill': True,
          },
          {
              'label': 'Messages',
              'data': dataset2_data,
              'color': 'rgb(255, 214, 10)',
              'fill': False,
          },
          {
              'label': 'Packets',
              'data': dataset1_data,
              'color': 'rgb(152, 152, 157)',
              'fill': False,
          },
        ]
    }
    return response_data


@router.get("/total_events", response_description="Total Events")
async def total_events(request: Request):
    now = datetime.datetime.utcnow()
    previous_two = now - datetime.timedelta(minutes=120)
    previous_one = now - datetime.timedelta(minutes=60)
    query = {"$and": [
        {'time': {'$gte': previous_two}}, 
        {'time': {'$lt': previous_one}}]}
    previous_count = await db["events"].count_documents(query)
    query = {"$and": [
        {'time': {'$gte': previous_one}}, 
        {'time': {'$lt': now}}]}
    count = await db["events"].count_documents(query)
    if previous_count == 0:
        change = 100 if count == 0 else 200
    else:
        change = int(count / previous_count * 100)
    change_text = '+' if change > 100 else ''
    change_text += str(change - 100)
    data = {
        'total': count,
        'change': change_text,
    }
    return data


@router.get("/total_messages", response_description="Total Meassages")
async def total_messages(request: Request):
    now = datetime.datetime.utcnow()
    previous_two_minutes = now - datetime.timedelta(minutes=120)
    previous_one_minute = now - datetime.timedelta(minutes=60)
    query = {"$and": [{'time': {'$gte': previous_two_minutes}}, {
        'time': {'$lt': previous_one_minute}}]}
    previous_count = await db["messages"].count_documents(query)
    query = {'time': {'$gte': previous_one_minute}}
    count = await db["messages"].count_documents(query)
    if previous_count == 0:
        change = 100 if count == 0 else 200
    else:
        change = int(count / previous_count * 100)
    change_text = '+' if change > 100 else ''
    change_text += str(change - 100)
    data = {
        'total': count,
        'change': change_text,
    }
    return data


@router.get("/total_packets", response_description="Total Packets")
async def total_packets(request: Request):
    now = datetime.datetime.utcnow()
    previous_two_minutes = now - datetime.timedelta(minutes=120)
    previous_one_minute = now - datetime.timedelta(minutes=60)
    query = {"$and": [{'time': {'$gte': previous_two_minutes}}, {
        'time': {'$lt': previous_one_minute}}]}
    previous_count = await db["packets"].count_documents(query)
    query = {
        "$and": [{'time': {'$gte': previous_one_minute}}]}
    count = await db["packets"].count_documents(query)
    if previous_count == 0:
        change = 100 if count == 0 else 200
    else:
        change = int(count / previous_count * 100)
    change_text = '+' if change > 100 else ''
    change_text += str(change - 100)
    data = {
        'total': count,
        'change': change_text,
    }
    return data


@router.get("/top_categories", response_description="Total categories")
async def top_categories(request: Request):
    now = datetime.datetime.utcnow()
    start_date = now - datetime.timedelta(days=1)
    end_date = now
    query = {"$and": [{'time': {'$gte': start_date}}, {
        'time': {'$lt': end_date}}, {'positive': True}]}
    data_raw = await db["incidents"].find(query).to_list(length=1000)
    data_length = len(data_raw)
    data_length = 30
    data_map = {
        'Discovery': 10,
        'Execution': 20,
        'Escalate': 0,
        'Command': 0,
        'Impact': 0,
    }
    for d in data_raw:
        if d['tactic'] in data_map:
            data_map[d['tactic']] += 1
    data = [
        {
            'id': 1,
            'title': 'Discovery',
            'count': data_map['Discovery'],
            'subtitle': 'locating information to assess',
            'percent': data_map['Discovery'] / data_length * 100 if data_map['Discovery'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0102/',
        },
        {
            'id': 2,
            'title': 'Execution',
            'count': data_map['Execution'],
            'subtitle': '',
            'percent': data_map['Execution'] / data_length * 100 if data_map['Execution'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0102/',
        },
        {
            'id': 3,
            'title': 'Escalate',
            'count': data_map['Escalate'],
            'percent': data_map['Escalate'] / data_length * 100 if data_map['Escalate'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0102/',
        },
        {
            'id': 4,
            'title': 'Command',
            'count': data_map['Command'],
            'percent': data_map['Command'] / data_length * 100 if data_map['Command'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0102/',
        },
        {
            'id': 5,
            'title': 'Impact',
            'count': data_map['Impact'],
            'percent': datadata_map_day['Impact'] / data_length * 100 if data_map['Impact'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0102/',
        },
    ]
    return data
