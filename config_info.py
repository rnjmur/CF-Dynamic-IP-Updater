#!/usr/bin/env python
#imports
import configparser

class ConfigInfo:
    """
    Object to store configuration file items
    
    Extended description of function.
    
    Parameters:
    arg1 (int): Description of arg1
    
    Returns:
    int: Description of return value
    
    """
    #Variable to track number of zones
    zone_count = 0
    #default time wait
    time_wait = 300

    class ZoneInfo:
        """
        object to store config info for each zone
        """
        def __init__(self, zone_id, bearer_token, record_id):
            """
            Initialize object with values
            
            Parameters:
            zone_id (string): This zone's id
            bearer_token (string): CF API Key
            record_id (string): DNS records to update
            """
            self.zone_id = zone_id
            self.bearer_token = bearer_token
            # split records into list
            self.record_id = record_id.split(',')
    
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
            self.zone_1 = self.ZoneInfo(config.get('zone_1', 'zone_id'), config.get('zone_1', 'bearer_token'), config.get('zone_1', 'record_id'))
            self.zone_count += 1
        
        if 'zone_2' in config:
            self.zone_2 = self.ZoneInfo(config.get('zone_2', 'zone_id'), config.get('zone_2', 'bearer_token'), config.get('zone_2', 'record_id'))
            self.zone_count += 1
        
        if 'zone_3' in config:
            self.zone_3 = self.ZoneInfo(config.get('zone_3', 'zone_id'), config.get('zone_3', 'bearer_token'), config.get('zone_3', 'record_id'))
            self.zone_count += 1
        
        if 'zone_4' in config:
            self.zone_4 = self.ZoneInfo(config.get('zone_4', 'zone_id'), config.get('zone_4', 'bearer_token'), config.get('zone_4', 'record_id'))
            self.zone_count += 1
        
        if 'zone_5' in config:
            self.zone_5 = self.ZoneInfo(config.get('zone_5', 'zone_id'), config.get('zone_5', 'bearer_token'), config.get('zone_5', 'record_id'))
            self.zone_count += 1
        

    