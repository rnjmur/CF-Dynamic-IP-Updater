# CF-Dynamic-IP-Updater

Use cloudflare API to update IPs when Dynamic IP changes

Python3 is required.  The tool currently only works with API tokens but I am working to add the ability to use API keys as well.

This tool will update your cloudflare A records whenever a dynamic IP address change is detected.

Simply add your cloudflare info into the cfauth.ini file and then run the cf-dyn-ip-updater.py file.  Make sure your generated API token has DNS edit rights configured properly for your zones or the updates will not work.

If you run cf-dyn-ip-updater.py -q or cf-dyn-ip-updater.py --query it will use the cloudflare API token configured in zone1 and run a query returning a list of all zone and record ids available.  For the query to work properly you must use an API token that has at least read permission for ALL zones.  The query will print out the cfauth.ini zone_id and record_id configuration so that you can copy and paste it into the cfauth.ini file.

If this program helps you out then I appreciate any donations!

PayPal:  https://paypal.me/JMurley77?locale.x=en_US

