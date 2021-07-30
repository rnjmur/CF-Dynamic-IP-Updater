#!/usr/bin/env python
#imports
import sys
import config_info as ConfigInfo
import cf_update as CFUpdate
import cf_query as CFQuery

# program info Variables
__author__ = 'RNJMUR'
__credits__ = ['RNJMUR']
__license__ = 'GPL 3.0'
__version__ = '0.80'
__maintainer__ = 'RNJMUR'
__email__ = 'rnjmur@hotmail.com'
__status__ = 'Beta'

__prog_info__ = "\nAuthor: " + __author__ + \
        "\nCredits: " + "".join(__credits__) + \
        "\nLicense: " + __license__ + \
        "\nVersion: " + __version__ + \
        "\nMaintainer: " + __maintainer__ + \
        "\nContact: " + __email__ + \
        "\nStatus: " + __status__ + "\n"

__help__ = """
This will check your IP against the IP currently in CloudFlare's DNS.
If different then it will update the CloudFlare DNS and log the changes.

Possible arguments:
-h or --help:  Print this message
-q or --query:  Display Cloudflare zone ids for use in config file
-s or --service:  Use this if you are running this as a service
"""

#Set config file name
__configfile__ = "cfauth.ini"

#Main
if __name__ == '__main__':
    # Create config_info object
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
    #End Debugging
    #Check arguments
    if len(sys.argv) > 1:
        #run continuosly as service
        if sys.argv[1] == '-s' or sys.argv[1] == '--service':
            CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile, True)
            #pass
        #run query to get zone ids
        elif sys.argv[1] == '-q' or sys.argv[1] == '--query':
            CFQuery.CFQuery.GetZones(cf_configfile)
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(__prog_info__)
            print(__help__)
    else:
        CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile)
        #pass
    