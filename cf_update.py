#!/usr/bin/env python
#imports
import requests, time, json, smtplib, threading
import config_info as ConfigInfo
import cf_logger as CFLogger

class CFUpdate:
    # Class overriding Threading.Thread
    # Used to start a thread which sends DNS updates
    class runCFUpdate (threading.Thread):
        def __init__(self, name, zone_id, record_id, headers, payload_data):
            threading.Thread.__init__(self)
            self.ThreadID = name
            self.zone_id = zone_id
            self.record_id = record_id
            self.payload_data = payload_data
            self.headers = headers
            
        def run(self):
            requests.patch('https://api.cloudflare.com/client/v4/zones/' + zone_id + '/dns_records?name=' + record_id, headers=headers, data=json.dumps(payload_data))

    def CFUpdater(configfile):
        # The headers we want to use
        headers = {
            'Authorization': 'Bearer ' + configfile.bearer_token, 
            'content-type': 'application/json'
            }
        
        # Getting the initial data of your A Record
        a_record_url = requests.get('https://api.cloudflare.com/client/v4/zones/' + configfile.zone_id + '/dns_records?name=' + configfile.record_id[0], headers=headers)
        arecordjson = a_record_url.json()
        
        # This is the current IP that your chosen A record has been set to on Cloudflare
        current_set_ip = arecordjson['result'][0]['content']
        
        # This gets your current live external IP (whether that is the same as the A record or not)
        currentip = requests.get('https://api.ipify.org?format=json')
        
        # Status code should be 200, otherwise the API is probably down (this can happen quite a bit)
        ipcheck_status = currentip.status_code
        
        # Handling any API errors (otherwise we'd be trying to change the IP to some random HTML)
        while ipcheck_status != 200:
            time.sleep(60)
            currentip = requests.get("https://api64.ipify.org?format=json")
            ipcheck_status = currentip.status_code
        
        currentactualip = currentip.json()['ip']
        
        if currentactualip == current_set_ip:
            print(currentactualip + " Matches " + current_set_ip)
            # If IPs match then no need to continue
            return "true"
        else: # If your live IP is NOT the same as the A Record's IP
            print(currentactualip + " Doesn't Match " + current_set_ip)
            pass
        
        # The "Payload" is what we want to change in the DNS record JSON (in this case, it's our IP)
        payload = {'content': currentactualip}
        
        # Change the IP using a PATCH request
        for record in configfile.record_id:
            CFUpdate.runCFUpdate(configfile.zone_id + record, configfile.zone_id, record, payload).start()
            #requests.patch(f"https://api.cloudflare.com/client/v4/zones/{configfile.zone_id}/dns_records/{record}", headers=headers, data=json.dumps(payload))
        
        #Log the IP change
        CFLogger.WriteLog(current_set_ip, currentactualip)
        
        return false

    def SendMail(configfile):
        # Sends an email to you to let you know everything has been updated.
        if configfile.smtp_enable == "Y":
            sender = configfile.smtp_sender
            receivers = configfile.smtp_recipients
            
            message = f"""From: Server <{configfile.smtp_sender}>
            To: <{configfile.smtp_recipients}>
            Subject: DNS IP Updated
            The server's IP has changed from {current_set_ip} to {currentactualip}.
            The DNS records have been updated.
            """
            
            smtpObj = smtplib.SMTP(configfile.smtp_server, port=configfile.smtp_port)
            smtpObj.connect(configfile.smtp_server, port=configfile.smtp_port)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(configfile.smtp_un, configfile.smtp_pw)
            smtpObj.sendmail(sender, receivers, message)

    def CFUpdateCheck(cf_configfile, is_service="false"):
        if is_service == "false":
            temp_zone_counter = cf_configfile.zone_count
            if temp_zone_counter == 5:
                if CFUpdate.CFUpdater(cf_configfile.zone_5) == "true":
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 4:
                if CFUpdate.CFUpdater(cf_configfile.zone_4) == "true":
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 3:
                if CFUpdate.CFUpdater(cf_configfile.zone_3) == "true":
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 2:
                if CFUpdate.CFUpdater(cf_configfile.zone_2) == "true":
                    return
                else:
                    temp_zone_counter -= 1
            if temp_zone_counter == 1:
                if CFUpdate.CFUpdater(cf_configfile.zone_1) == "true":
                    return
                else:
                    temp_zone_counter -= 1
                    while threading.activeCount() > 1:
                        time.sleep(5)
                    CFUpdate.SendMail(cf_configfile)
        else:
            while true:
                time.sleep(cf_configfile.time_wait)
                temp_zone_counter = cf_configfile.zone_count
                if temp_zone_counter == 5:
                    if CFUpdate.CFUpdater(cf_configfile.zone_5) == "true":
                        continue
                    else:
                        temp_zone_counter -= 1
                if temp_zone_counter == 4:
                    if CFUpdate.CFUpdater(cf_configfile.zone_4) == "true":
                        continue
                    else:
                        temp_zone_counter -= 1
                if temp_zone_counter == 3:
                    if CFUpdate.CFUpdater(cf_configfile.zone_3) == "true":
                        continue
                    else:
                        temp_zone_counter -= 1
                if temp_zone_counter == 2:
                    if CFUpdate.CFUpdater(cf_configfile.zone_2) == "true":
                        continue
                    else:
                        temp_zone_counter -= 1
                if temp_zone_counter == 1:
                    if CFUpdate.CFUpdater(cf_configfile.zone_1) == "true":
                        continue
                    else:
                        temp_zone_counter -= 1
                        while threading.activeCount() > 1:
                            time.sleep(5)
                        CFUpdate.SendMail(cf_configfile)