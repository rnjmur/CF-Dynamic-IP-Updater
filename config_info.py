#!/usr/bin/env python
#imports
import configparser

class ConfigInfo:
    """
    Object to store configuration file items
    
    Configuration Data is stored using two data nodes.
    Data Node 1 (ZoneInfo) stores the Cloudflare Zone ID, bearer token, and a list of the DNS records to update
    Data Node 2 (IPCheck) stores the whatismyip api key
    
    """
    #Variable to track number of zones
    zone_count = 0
    #default time wait
    time_wait = 300

    class ZoneInfo:
        """
        object to store config info for each zone
        """
        def __init__(self, zone_id, bearer_token, record_id, custom_id):
            """
            Initialize object with values
            
            Parameters:
            zone_id (string): This zone's id
            bearer_token (string): CF API Key
            record_id (string): DNS records to update
            zone_list (list): List of Zone Nodes
            """
            self.zone_id = zone_id
            self.bearer_token = bearer_token
            # split records into list
            self.record_id = record_id.split(',')
            self.custom_id = custom_id.split(',')
    
    class IPCheck:
        """
        Object to store api key for whatsmyip.com
        """
        def __init__(self, api_key):
            """
            Initialize whatismyip object
            
            Parameters:
            spi_key (string): store api key
            """
            self.api_key = api_key
    
    def __init__(self, configfile):
        """
        Initialize object by reading in items from the config file
        
        Parameters:
        configfile (string): config file name
        
        """
        # Reading the keys from the configuration file
        config = configparser.ConfigParser()
        config.read(configfile)
        
        # Create Placeholder list for zones
        self.zone_list = []
        
        # Check and read in values for each config file section
        
        if 'global' in config:
            self.time_wait = int(config.get('global', 'time_wait'))
        
        if 'mail' in config:
            self.smtp_enable=config.get('mail', 'enable')
            self.smtp_sender=config.get('mail', 'sender')
            self.smtp_recipients=config.get('mail', 'recipients').split(',')
            self.smtp_server=config.get('mail', 'smtp')
            self.smtp_port=int(config.get('mail', 'smtp_port'))
            self.smtp_un=config.get('mail', 'smtp_un')
            self.smtp_pw=config.get('mail', 'smtp_pw')
        
        if 'whatismyip' in config:
            self.check_ip = self.IPCheck(config.get('whatismyip', 'api_key'))
        else:
            self.check_ip = self.IPCheck("0")
        
        if 'zone_1' in config:
            self.zone_1 = self.ZoneInfo(config.get('zone_1', 'zone_id'), config.get('zone_1', 'bearer_token'), config.get('zone_1', 'record_id'), 
                config.get('zone_1', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_1)
            self.zone_count += 1
        
        if 'zone_2' in config:
            self.zone_2 = self.ZoneInfo(config.get('zone_2', 'zone_id'), config.get('zone_2', 'bearer_token'), config.get('zone_2', 'record_id'), 
                config.get('zone_2', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_2)
            self.zone_count += 1
        
        if 'zone_3' in config:
            self.zone_3 = self.ZoneInfo(config.get('zone_3', 'zone_id'), config.get('zone_3', 'bearer_token'), config.get('zone_3', 'record_id'), 
                config.get('zone_3', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_3)
            self.zone_count += 1
        
        if 'zone_4' in config:
            self.zone_4 = self.ZoneInfo(config.get('zone_4', 'zone_id'), config.get('zone_4', 'bearer_token'), config.get('zone_4', 'record_id'), 
                config.get('zone_4', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_4)
            self.zone_count += 1
        
        if 'zone_5' in config:
            self.zone_5 = self.ZoneInfo(config.get('zone_5', 'zone_id'), config.get('zone_5', 'bearer_token'), config.get('zone_5', 'record_id'), 
                config.get('zone_5', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_5)
            self.zone_count += 1
        
        if 'zone_6' in config:
            self.zone_6 = self.ZoneInfo(config.get('zone_6', 'zone_id'), config.get('zone_6', 'bearer_token'), config.get('zone_6', 'record_id'), 
                config.get('zone_6', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_6)
            self.zone_count += 1
        
        if 'zone_7' in config:
            self.zone_7 = self.ZoneInfo(config.get('zone_7', 'zone_id'), config.get('zone_7', 'bearer_token'), config.get('zone_7', 'record_id'), 
                config.get('zone_7', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_7)
            self.zone_count += 1
        
        if 'zone_8' in config:
            self.zone_5 = self.ZoneInfo(config.get('zone_8', 'zone_id'), config.get('zone_8', 'bearer_token'), config.get('zone_8', 'record_id'), 
                config.get('zone_8', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_8)
            self.zone_count += 1
        
        if 'zone_9' in config:
            self.zone_9 = self.ZoneInfo(config.get('zone_9', 'zone_id'), config.get('zone_9', 'bearer_token'), config.get('zone_9', 'record_id'), 
                config.get('zone_9', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_9)
            self.zone_count += 1
        
        if 'zone_10' in config:
            self.zone_10 = self.ZoneInfo(config.get('zone_10', 'zone_id'), config.get('zone_10', 'bearer_token'), config.get('zone_10', 'record_id'), 
                config.get('zone_10', 'custom_id', fallback=''))
            self.zone_list.append(self.zone_10)
            self.zone_count += 1

    def GetZoneList(self):
        return self.zone_list