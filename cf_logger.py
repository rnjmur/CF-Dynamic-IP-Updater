#!/usr/bin/env python
#imports
import logging, datetime

class CFLogger:
    """
    Module for logging IP changes
    """
    
    # Name of ip change log
    __log_file__ = 'cf-updater.log'
    # format for log
    __log_format__ = '%(levelname)s :: %(message)s'
    
    # Setting up the logger (a file where it records all IP changes)
    logging.basicConfig(level=logging.INFO, filename=__log_file__, format=__log_format__)
    
    def WriteLog(old_ip, new_ip):
        """
        Write to log
        
        Parameter:
        old_ip (string): The old ip address
        new_ip (string): The new ip address
        
        """
        # Get the time of the IP change
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Write new log
        logging.info(now + " - IP change from " + old_ip + " to " + new_ip)
        
    def WriteError(message):
        """
        Write error to log
        
        Parameter:
        message (string): error mesage to write to log
        """
        # Current date and time
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Write error log
        logging.info(now + " ERROR: " + message)