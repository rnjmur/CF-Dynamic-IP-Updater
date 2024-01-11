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
__version__ = '0.90'
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
-c:<filename> or --config:<filename>:  Use this config file instead of default cfauth.ini
"""

#Set config file name
__configfile__ = "cfauth.ini"

#Main
if __name__ == '__main__':
    # Create config_info object
    cf_configfile = ConfigInfo.ConfigInfo(__configfile__)
    
    #Check arguments
    if len(sys.argv) == 2:
        #set config file
        if '-c:' in sys.argv[1]:
            del cf_configfile
            cf_configfile = ConfigInfo.ConfigInfo(sys.argv[1][3:])
            CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile)
        elif '--config:' in sys.argv[1]:
            del cf_configfile
            cf_configfile = ConfigInfo.ConfigInfo(sys.argv[1][9:])
            CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile)
        #run continuosly as service
        elif sys.argv[1] == '-s' or sys.argv[1] == '--service':
            CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile, True)
        #run query to get zone ids
        elif sys.argv[1] == '-q' or sys.argv[1] == '--query':
            CFQuery.CFQuery.GetZones(cf_configfile)
        #display help
        else:
            print(__prog_info__)
            print(__help__)
    elif len(sys.argv) == 3:
        for arg in sys.argv:
            if '-c:' in arg:
                del cf_configfile
                cf_configfile = ConfigInfo.ConfigInfo(arg[3:])
            elif '--config:' in arg:
                del cf_configfile
                cf_configfile = ConfigInfo.ConfigInfo(arg[9:])
        for arg2 in sys.argv:
            #run continuosly as service
            if arg2 == '-s' or arg2 == '--service':
                CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile, True)
            #run query to get zone ids
            elif arg2 == '-q' or arg2 == '--query':
                CFQuery.CFQuery.GetZones(cf_configfile)
            #display help
            elif arg2 == '-h' or arg2 == '--help':
                print(__prog_info__)
                print(__help__)
    elif len(sys.argv) > 3:
        print("Too Many Arguments given!  See help below for proper syntax:\n")
        print(__help__)
    else:
        CFUpdate.CFUpdate.CFUpdateCheck(cf_configfile)
    
