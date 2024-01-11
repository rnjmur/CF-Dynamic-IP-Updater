#!/usr/bin/env python
#imports
import requests
import config_info as ConfigInfo
import cf_logger as CFLogger

class CFQuery:
    """
    Module to query CF and get zone IDs
    """
    def GetZones(configfile):
        """
        Get zone ids
        
        Parameter:
        configfile (string): the config_info object
        """
        # Set initial bearer token
        bearer_token = configfile.zone_1.bearer_token
        # Create Auth header
        headers = {
        'Authorization': 'Bearer ' + configfile.zone_1.bearer_token,
        'Content-Type': 'application/json',
        }
        
        try:
            print()
            # Query for zone IDs
            a_record_url = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers)
            config_build = ""
            for record in a_record_url.json()['result']:
                print(record['id'] + ' ' + record['name'])
                config_build += '\n\nzone_id=' + record['id'] + '\nbearer_token=' + bearer_token + '\nrecord_id='
                dns_records = requests.get('https://api.cloudflare.com/client/v4/zones/' + record['id'] + '/dns_records', headers=headers)
                for dns in dns_records.json()['result']:
                    print('ID: ' + dns['id'] +'   Type: ' + dns['type'] + '   Name: ' + dns['name'] + '   Content: ' + dns['content'])
                    if dns['type'] == 'A':
                        config_build += dns['id'] + ","
                config_build = config_build[:-1]
                print()
            for zone in configfile.GetZoneList():
                if not zone.bearer_token == bearer_token:
                    headers = {
                        'Authorization': 'Bearer ' + zone.bearer_token,
                        'Content-Type': 'application/json',
                        }
                    # Query for zone IDs
                    a_record_url = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers)
                    for record in a_record_url.json()['result']:
                        print(record['id'] + ' ' + record['name'])
                        config_build += '\n\nzone_id=' + record['id'] + '\nbearer_token=' + zone.bearer_token + '\nrecord_id='
                        dns_records = requests.get('https://api.cloudflare.com/client/v4/zones/' + record['id'] + '/dns_records', headers=headers)
                        for dns in dns_records.json()['result']:
                            print('ID: ' + dns['id'] +'   Type: ' + dns['type'] + '   Name: ' + dns['name'] + '   Content: ' + dns['content'])
                            if dns['type'] == 'A':
                                config_build += dns['id'] + ","
                        config_build = config_build[:-1]
                        print()
            print()
            print('For cfauth.ini file: \n' + config_build)
            
        except Exception as e:
            CFLogger.CFLogger.WriteError("CFQuery failed! Check that config file is correct! Details: " + str(e))
            print (e)
