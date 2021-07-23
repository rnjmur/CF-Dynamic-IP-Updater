#!/usr/bin/env python
#imports
import requests
import config_info as ConfigInfo

class CFQuery:
    def GetZones(configfile):
        headers = {
        'Authorization': 'Bearer ' + configfile.zone_2.bearer_token,
        'Content-Type': 'application/json',
        }
        
        # Query for zone IDs
        a_record_url = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers)
        for record in a_record_url.json()['result']:
            print(record['id'] + ' ' + record['name'])
            dns_records = requests.get('https://api.cloudflare.com/client/v4/zones/' + record['id'] + '/dns_records', headers=headers)
            for dns in dns_records.json()['result']:
                print('Type: ' + dns['type'] + '   Name: ' + dns['name'] + '   Content: ' + dns['content'])
            print()
            