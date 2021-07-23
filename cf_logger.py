#!/usr/bin/env python
#imports
import logging, datetime

class CFLogger:
    
    __log_file__ = 'ipchanges.log'
    __log_format__ = '%(levelname)s :: %(message)s'
    
    # Setting up the logger (a file where it records all IP changes)
    logging.basicConfig(level=logging.INFO, filename=__log_file__, format=__log_format__)
    
    def WriteLog(old_ip, new_ip):
        # Get the time of the IP change
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"{now} - IP change from {old_ip} to {new_ip}")