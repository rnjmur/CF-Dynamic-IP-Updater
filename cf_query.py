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
        # Create Auth header
        headers = {
        'Authorization': 'Bearer ' + configfile.zone_1.bearer_token,
        'Content-Type': 'application/json',
        }
        
        try:
            # Query for zone IDs
            a_record_url = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers)
            config_build = ""
            for record in a_record_url.json()['result']:
                print(record['id'] + ' ' + record['name'])
                config_build += '\n\nzone_id=' + record['id'] + '\nrecord_id='
                dns_records = requests.get('https://api.cloudflare.com/client/v4/zones/' + record['id'] + '/dns_records', headers=headers)
                for dns in dns_records.json()['result']:
                    print('ID: ' + dns['id'] +'   Type: ' + dns['type'] + '   Name: ' + dns['name'] + '   Content: ' + dns['content'])
                    if dns['type'] == "A":
                        config_build += dns['id']
                        config_build += ","
                print()
                config_build = config_build[:-1]
            print()
            print('For cfauth.ini file: \n' + config_build)
            
        except Exception as e:
            CFLogger.CFLogger.WriteError("CFQuery failed! Check that config file is correct! Details: " + str(e))
            print (e)
