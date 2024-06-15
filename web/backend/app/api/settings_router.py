from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from subprocess import run, PIPE

router = APIRouter()
@router.get("/install_config", response_description="Install config to Core")
async def install_config(request: Request):
   # drop collections
   request.app.mongodb["services"].drop()
   request.app.mongodb["sources"].drop()
   request.app.mongodb["destinations"].drop()
   request.app.mongodb["nodes"].drop()
   request.app.mongodb["rules"].drop()

   # add nodes
   raw_rules =  await request.app.mongodb["raw_rules"].find().to_list(length=1000)
   nodes = []
   for rule in raw_rules:
      for name in rule['src'].split(';'):
         node ={
               'name': name,
               'zone': 'internal'
         }
         if node not in nodes:
               nodes.append(node)
      for name in rule['dst'].split(';'):
         node ={
               'name': name,
               'zone': 'internal'
         }
         if node not in nodes:
               nodes.append(node)
   await request.app.mongodb["nodes"].insert_many(nodes)

   # add services
   services = []
   for rule in raw_rules:
      for name in rule['service'].split(';'):
         service ={
               'name': name,
               'severity': 'low'
         }
         if service not in services:
               services.append(service)
   await request.app.mongodb["services"].insert_many(services)

   # add simple rules with one source, dest, port
   rules = []
   for rule in raw_rules:
      for src in rule['src'].split(';'):
         for service in rule['service'].split(';'):
            for dst in rule['dst'].split(';'):
               rules.append({
                   'rule_id': rule['rule_id'],
                   'name': rule['name'],
                   'src': src,
                   'dst': dst,
                   'service': service,
                   'action': rule['action'],
               })
   await request.app.mongodb["rules"].insert_many(rules)

@router.get("/check_rules", response_description="Check Critical rules")
async def check_rules(request: Request):
   request.app.mongodb["crit_rules"].drop()

   rules = await request.app.mongodb["rules"].find().to_list(length=10000)
   raw_rules = await request.app.mongodb["raw_rules"].find().to_list(length=10000)
   services = await request.app.mongodb["services"].find().to_list(length=10000)
   services_map = { x['name']:x['severity'] for x in services}
   crit_rules = []
   zero_rules = []
   for raw_rule in raw_rules:
      # Zero-Hit Rules: 
      # Rules that have never matched any traffic according to firewall logs or traffic counters.
      zero_list = (0, 'Zero', "Low (number of hits = 95705)")
      if raw_rule['hits'] in zero_list :
         zero_rules.append(raw_rule['rule_id'])
   if zero_rules:
      crit_rules.append({
            'name': 'Zero Hit Rules',
            'description': f'Unused rules without hits: {len(zero_rules)}',
            'time': '1',
            'severity': 'med',
            'tactic': 'ZHR',
            'positive': '1',
            'rules': zero_rules
         })

   # Criticality Services:
   # Unsecure protocols in use
   crit_protocols = {}
   for rule in rules:
      if rule['service'] in services_map:
         service = rule['service']
         if services_map[service] == 'high':
            if service in crit_protocols:
               crit_protocols[service].append(f"{rule['rule_id']} : {rule['name']}")
            else:
               crit_protocols[service] = [f"{rule['rule_id']} : {rule['name']}"]
   for crit_protocol in crit_protocols:
      crit_rules.append({
         'name': 'Critical Protocols',
         'description': f'Unsecure protocol in use: {crit_protocol}',
         'time': '1',
         'severity': 'high',
         'tactic': 'CS',
         'positive': '1',
         'rules': crit_protocols[crit_protocol]
      })

   # Redundant Rules: 
   # Duplicate rules that perform the same action for the same traffic, leading to unnecessary processing overhead.
   uniq_rules_map = {}
   uniq_rules = []
   redundant_rules = []
   for uniq_rule in uniq_rules:
      uniq = f"{uniq_rule['src']}-{uniq_rule['dst']}-{uniq_rule['service']}" 
      if uniq in uniq_rules_map:
         redundant_rules.append({
            'name': 'Redundant Rules',
            'description': 'Duplicate rules that perform the same action for the same traffic, leading to unnecessary processing overhead.',
            'time': '1',
            'severity': 'high',
            'tactic': 'RR',
            'positive': '1',
            'rules': [f"{uniq_rules_map[uniq]['rule_id']} : {uniq_rules_map[uniq]['name']}", f"{uniq_rule['rule_id']} : {uniq_rule['name']}"]
         })
   # print('RR')
   # print(json.dumps(uniq_rules, indent=4))
   # print('CritRules')
   print(json.dumps(crit_rules, indent=4))
   if crit_rules:
       await request.app.mongodb["crit_rules"].insert_many(crit_rules)

   return {"message": "Config installed successfully and Core service restarted"}

