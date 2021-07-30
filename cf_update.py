#!/usr/bin/env python
#imports
import requests, time, json, smtplib, threading
import config_info as ConfigInfo
import cf_logger as CFLogger

class CFUpdate:
    """ Static Module with code to do CloudFlare API IP change """
    class runCFUpdate (threading.Thread):
        """
        Class overriding Threading.Thread used to start a thread
        which sends DNS updates
        """
        def __init__(self, name, zone_id, record_id, headers, payload_data):
            """
            Initialize thread object
            
            
            Parameters:
            name (string): a Name for the thread
            zone_id (string): The zone_id to make changes to
            record_id (string): The DNS record to change
            headers (string): The authentication header
            payload_data (string): The payload containing the ip address change
            """
            threading.Thread.__init__(self)
            self.ThreadID = name
            self.zone_id = zone_id
            self.record_id = record_id
            self.payload_data = payload_data
            self.headers = headers
            
        def run(self):
            """ Thread code to run """
            try:
                print(json.dumps(self.payload_data))
                thread_url = requests.patch('https://api.cloudflare.com/client/v4/zones/' + self.zone_id + '/dns_records/' + self.record_id, headers=self.headers, data=json.dumps(self.payload_data))
                print(thread_url)
            except Exception as e:
                CFLogger.CFLogger.WriteError("Update to CF failed!  Details: " + str(e))
                print(e)

    def CFUpdater(configfile, ip_check="0"):
        """
        Method to check for IP changes then use CF API to update if necessary
        
        Parameters:
        configfile (config_info): config_info zone object
        ip_check (string): API key for whatismyip or 0
        """
        # The headers we want to use
        headers = {
            'Authorization': 'Bearer ' + configfile.bearer_token, 
            'content-type': 'application/json'
            }
        
        # Getting the initial data of the A Record
        a_record_url = requests.get('https://api.cloudflare.com/client/v4/zones/' + configfile.zone_id + '/dns_records/' + configfile.record_id[0], headers=headers)
        arecordjson = a_record_url.json()
        
        # Use try to catch errors reading from CloudFlare or IP check
        try:
            # This is the current IP that the A record has been set to on Cloudflare
            current_set_ip = arecordjson['result']['content']
            
            # This gets your current live external IP (whether that is the same as the A record or not)
            if ip_check == "0":
                currentip = requests.get('https://api.ipify.org?format=json')
                
                # Status code should be 200, otherwise the API is probably down (this can happen quite a bit)
                ipcheck_status = currentip.status_code
                
                # Handling any API errors (otherwise we'd be trying to change the IP to some random HTML)
                while ipcheck_status != 200:
                    time.sleep(60)
                    currentip = requests.get("https://api64.ipify.org?format=json")
                    ipcheck_status = currentip.status_code
                currentactualip = currentip.json()['ip']
            else:
                currentip = requests.get('http://api.whatismyip.com/ip.php?key=' + ip_check + '&output=json')
                
                # Status code should be 200, otherwise the API is probably down (this can happen quite a bit)
                ipcheck_status = currentip.status_code
                
                # Handling any API errors (otherwise we'd be trying to change the IP to some random HTML)
                while ipcheck_status != 200:
                    time.sleep(60)
                    currentip = requests.get('http://api.whatismyip.com/ip.php?key=' + ip_check + '&output=json')
                    ipcheck_status = currentip.status_code
                currentactualip = check_ip.json()['ip_address'][0]['result']
        except Exception as e:
            CFLogger.CFLogger.WriteError("CFUpdater failed checking IP! Check that config file is correct! Details: " + str(e))
            print(e)
            return False

        
        if currentactualip == current_set_ip:
            # If IPs match then no need to continue
            print('Current IP ' + currentactualip + ' matches ' + current_set_ip)
            return True
        else: # If your live IP is NOT the same as the A Record's IP
            print('Current IP ' + currentactualip + ' does not match ' + current_set_ip)
            pass
        
        # The "Payload" is what we want to change in the DNS record JSON (in this case, it's our IP)
        payload = {'content': currentactualip}
        
        # Change the IP using a PATCH request
        for record in configfile.record_id:
            CFUpdate.runCFUpdate(configfile.zone_id + record, configfile.zone_id, record, headers, payload).start()
            #requests.patch(f"https://api.cloudflare.com/client/v4/zones/{configfile.zone_id}/dns_records/{record}", headers=headers, data=json.dumps(payload))
        
        #Log the IP change
        CFLogger.CFLogger.WriteLog(current_set_ip, currentactualip)
        
        return False

    def SendMail(configfile):
        """ Sends an email to you to let you know everything has been updated. """
        if configfile.smtp_enable == "Y" or configfile.smtp_enable == "y":
            sender = configfile.smtp_sender
            receivers = configfile.smtp_recipients
            
            message = "From: Server <" + configfile.smtp_sender + """>
            To: <""" + configfile.smtp_recipients + """>
            Subject: DNS IP Updated
            The server's IP has changed from """ + current_set_ip + " to " + currentactualip + """.
            The DNS records have been updated.
            """
            
            smtpObj = smtplib.SMTP(configfile.smtp_server, port=configfile.smtp_port)
            smtpObj.connect(configfile.smtp_server, port=configfile.smtp_port)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(configfile.smtp_un, configfile.smtp_pw)
            smtpObj.sendmail(sender, receivers, message)

    def CFUpdateCheck(cf_configfile, is_service=False):
        if not is_service:
            temp_zone_counter = cf_configfile.zone_count
            if temp_zone_counter == 5:
                if CFUpdate.CFUpdater(cf_configfile.zone_5):
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 4:
                if CFUpdate.CFUpdater(cf_configfile.zone_4):
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 3:
                if CFUpdate.CFUpdater(cf_configfile.zone_3):
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 2:
                if CFUpdate.CFUpdater(cf_configfile.zone_2):
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 1:
                if CFUpdate.CFUpdater(cf_configfile.zone_1):
                    return
                else:
                    temp_zone_counter -= 1
                    while threading.activeCount() > 1:
                        time.sleep(5)
                    CFUpdate.SendMail(cf_configfile)
        else:
            CFUpdate.daemonStart(cf_configfile)
    
    def daemonStart(cf_configfile):
        while True:
            time.sleep(cf_configfile.time_wait)
            temp_zone_counter = cf_configfile.zone_count
            if temp_zone_counter == 5:
                if CFUpdate.CFUpdater(cf_configfile.zone_5):
                    continue
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 4:
                if CFUpdate.CFUpdater(cf_configfile.zone_4):
                    continue
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 3:
                if CFUpdate.CFUpdater(cf_configfile.zone_3):
                    continue
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 2:
                if CFUpdate.CFUpdater(cf_configfile.zone_2):
                    continue
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 1:
                if CFUpdate.CFUpdater(cf_configfile.zone_1):
                    continue
                else:
                    temp_zone_counter -= 1
                    while threading.activeCount() > 1:
                        time.sleep(5)
                    CFUpdate.SendMail(cf_configfile)
