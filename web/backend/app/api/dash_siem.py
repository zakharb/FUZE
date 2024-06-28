from fastapi import APIRouter, Request
from app.db import db
import datetime

router = APIRouter()


@router.get("/severity", response_description="Severity chart")
async def severity(request: Request, timeframe: str = None):
    """Formula Summary Severity Percentage = 
    (Percentage of Low Severity * W_low 
    + Percentage of Medium Severity * W_medium + Percentage of High Severity * W_high)
    / (W_low + W_medium + W_high)"""
    now = datetime.datetime.utcnow()
    if timeframe == '1d':
        previous_minute = now - datetime.timedelta(minutes=1440)
    elif timeframe == '8h':
        previous_minute = now - datetime.timedelta(minutes=480)
    else:
        previous_minute = now - datetime.timedelta(minutes=60)
    query = {'time': {'$gte': previous_minute},
             'severity': 'low', 'positive': True}
    low = await db["incidents"].count_documents(query)
    query = {'time': {'$gte': previous_minute},
             'severity': 'med', 'positive': True}
    med = await db["incidents"].count_documents(query)
    query = {'time': {'$gte': previous_minute},
             'severity': 'high', 'positive': True}
    high = await db["incidents"].count_documents(query)
    total = high + med + low
    severity = (high / total * 3 + med / total * 2 + low / total) / 6 * 100 if total != 0 else 0
    color = severity // 34
    data = {
        'bar': {
            'value': severity,
            'color': color,
        },
        'values': [
            {
                'title': 'High',
                'data': high,
                'color': 'text-danger',
            },
            {
                'title': 'Medium',
                'data': med,
                'color': 'text-warning',
            },
            {
                'title': 'Low',
                'data': low,
                'color': 'text-secondary',
            },
        ]
    }
    return data


@router.get("/bubble", response_description="Sources chart")
async def bubble(request: Request, timeframe: str = None):
    data_map = {}
    data = []
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(minutes=1440)
    query = {"$and": [{'time': {'$gte': start_date}}, {
        'time': {'$lt': end_date}}, {'positive': True}]}
    color = {
        'low': 0,
        'med': 1,
        'high': 2
    }
    incidents = await db["incidents"].find(query).sort("_id", -1).to_list(length=1000)
    for inc in incidents:
        severity = color[inc['severity']]
        for event in inc['events'].values():
            source = event['source']
            if source not in data_map:
                data_map[source] = {
                    'name': source, 
                    'value': 1, 
                    'radius': 15,
                    'color': severity, 
                }
            else:
                if data_map[source]['value'] < 30:
                    data_map[source]['value'] += 1
                    data_map[source]['radius'] += 1
                if severity > data_map[source]['color']:
                    data_map[source]['color'] = severity
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
        'Discovery': 0,
        'Execution': 0,
        'Collection': 0,
        'Control': 0,
        'Impact': 0,
    }
    # positive_events = {
    #     'Discovery': 0,
    #     'Exploit': 0,
    #     'Escalate': 0,
    #     'Command': 0,
    #     'Impact': 0
    # }
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
    labels = [x for x in total_events]
    dataset3_data = [x for x in total_events.values()]
    dataset1_data = []
    for label in labels:
        dataset1_data.append(positive_events[label])
    response_data = {
        'labels': labels,
        'datasets': [
            {
                'label': dataset1_label,
                'data': dataset1_data,
                'backgroundColor': ['rgb(10, 132, 255)'],
                'borderColor': 'rgb(10, 132, 255)',
                'borderWidth': 1,
            },
            {
                'label': dataset3_label,
                'data': dataset3_data,
                'backgroundColor': ['rgb(152, 152, 157)'],
                'borderColor': 'rgb(100, 100, 105)',
                'borderWidth': 1,
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
            'time': {'$lt': end_date}}, {'positive': True}]}
        events = await db["incidents"].count_documents(query)
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
            messages = await db["messages"].count_documents(query)
            events = await db["events"].count_documents(query)
            query = {"$and": [{'time': {'$gte': start_date}}, {
                'time': {'$lt': end_date}}, {'positive': True}]}
            incidents = await db["incidents"].count_documents(query)
            dataset1_data.append(messages)
            dataset2_data.append(events)
            dataset3_data.append(incidents)
            minute = (now - datetime.timedelta(minutes=i)).minute
            hour = (now - datetime.timedelta(minutes=i)).hour
            dt = f"{hour:02d}:{minute:02d}"
            labels.append(dt)
    response_data = {
        'labels': labels,
        'datasets': [
          {
              'label': 'Incidents',
              'data': dataset3_data,
              'color': 'rgb(10, 132, 255)',
              'fill': True,
          },
          {
              'label': 'Events',
              'data': dataset2_data,
              'color': 'rgb(106, 196, 220)',
              'fill': False,
          },
          {
              'label': 'Messages',
              'data': dataset1_data,
              'color': 'rgb(152, 152, 157)',
              'fill': False,
          },
        ]
    }
    return response_data


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


@router.get("/total_events", response_description="Total Events")
async def total_events(request: Request):
    now = datetime.datetime.utcnow()
    previous_two_minutes = now - datetime.timedelta(minutes=120)
    previous_one_minute = now - datetime.timedelta(minutes=60)
    query = {"$and": [{'time': {'$gte': previous_two_minutes}}, {
        'time': {'$lt': previous_one_minute}}]}
    previous_count = await db["events"].count_documents(query)
    query = {'time': {'$gte': previous_one_minute}}
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


@router.get("/total_incidents", response_description="Total Incidents")
async def total_incidents(request: Request):
    now = datetime.datetime.utcnow()
    previous_two_minutes = now - datetime.timedelta(minutes=120)
    previous_one_minute = now - datetime.timedelta(minutes=60)
    query = {"$and": [
        {'time': {'$gte': previous_two_minutes}}, 
        {'time': {'$lt': previous_one_minute}}, 
        {'positive': True}
    ]}
    previous_count = await db["incidents"].count_documents(query)
    print(previous_count)
    query = {
        "$and": [
            {'time': {'$gte': previous_one_minute}}, 
            {'positive': True}
        ]}
    count = await db["incidents"].count_documents(query)
    print(count)
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
    data_map = {
        'Discovery': 0,
        'Execution': 0,
        'Collection': 0,
        'Lateral Movement': 0,
        'Command and Control': 0,
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
            'title': 'Collection',
            'count': data_map['Collection'],
            'percent': data_map['Collection'] / data_length * 100 if data_map['Collection'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0100/',
        },
        {
            'id': 4,
            'title': 'Lateral Movement',
            'count': data_map['Lateral Movement'],
            'percent': data_map['Lateral Movement'] / data_length * 100 if data_map['Lateral Movement'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0109/',
        },
        {
            'id': 5,
            'title': 'Command and Control',
            'count': data_map['Command and Control'],
            'percent': data_map['Command and Control'] / data_length * 100 if data_map['Command and Control'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0101/',
        },
        {
            'id': 6,
            'title': 'Impact',
            'count': data_map['Impact'],
            'percent': data_map['Impact'] / data_length * 100 if data_map['Impact'] else 0,
            'href': 'https://attack.mitre.org/tactics/TA0105/',
        },
    ]
    return data
