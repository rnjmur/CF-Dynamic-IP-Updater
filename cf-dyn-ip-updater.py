#!/usr/bin/env python
#imports
import sys
import config_info as ConfigInfo
import cf_update as CFUpdate
import cf_query as CFQuery

__help__ = """
This will check your IP against the IP currently in CloudFlare's DNS.
If different then it will update the CloudFlare DNS and log the changes.

Possible arguments:
-h or --help:  Print this message
-q or --query:  Display zone ids
-s or --service:  Use this if you are running this as a daemon
"""

__configfile__ = "cfauth.ini"

#Main
if __name__ == '__main__':
    cf_configfile = ConfigInfo.ConfigInfo(__configfile__)
    
    #Debugging
    print(__help__)
    print('Time wait Variable')
    print(cf_configfile.time_wait)
    print('Check IP value')
    print(cf_configfile.check_ip.api_key)
    print('zone count')
    print(cf_configfile.zone_count)
    print('print Zone ID')
    print(cf_configfile.zone_1.zone_id)
    print('print Bearer Token')
    print(cf_configfile.zone_1.bearer_token)
    print('print Records')
    print(cf_configfile.zone_1.record_id)
    print('print each record individually')
    for record in cf_configfile.zone_1.record_id:
        print(record)
    print(cf_configfile.smtp_enable)
    for rec in cf_configfile.smtp_recipients:
        print(rec)
    print(cf_configfile.smtp_server)
    print(cf_configfile.smtp_port)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s' or sys.argv[1] == '--service':
            CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile, "true")
            #pass
        elif sys.argv[1] == '-q' or sys.argv[1] == '--query':
            CFQuery.CFQuery.GetZones(cf_configfile)
    else:
        CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile)
        #pass
    