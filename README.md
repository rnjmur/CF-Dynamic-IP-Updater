# CF-Dynamic-IP-Updater

Use cloudflare API to update DNS when Dynamic IP changes occur.

Python3 is required.  The tool only works with Global API tokens.

This tool will update your Cloudflare DNS A records whenever a dynamic IP address change is detected.  It can also bre used to update DNS records other than A records.

Simply add your cloudflare info into the cfauth.ini file and then run the cf-dyn-ip-updater.py file.  Make sure your generated API token has DNS edit rights configured properly for your zones or the updates will not work.

If you run cf-dyn-ip-updater.py -q or cf-dyn-ip-updater.py --query it will use the cloudflare API tokens configured for each zone and run a query returning a list of all zone and record ids available.  For the query to work properly you must use an API token that has at least read permission for ALL zones.  The query will print out the cfauth.ini zone_id, bearer token, and record_id configuration so that you can copy and paste it into the cfauth.ini file.

Prerequisites:
Python 3.8 or higher
pip install requests
Cloudflare Global API Key

Additional info can be found in the Wiki.

If this program helps you out then I appreciate any donations!

PayPal:  https://paypal.me/JMurley77?locale.x=en_US

