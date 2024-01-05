import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# UniFi Controller details
controller_url = 'https://unifiportal.domain.com:8443'  # Replace with your controller URL
username = 'username'  # Replace with your username
password = 'password'  # Replace with your password
site = 'default'  # Replace with your site name, if different

# Endpoint URLs
login_url = f"{controller_url}/api/login"
sites_url = f"{controller_url}/api/self/sites"
settings_url = f"{controller_url}/api/s/{site}/get/setting"

# Start a session
session = requests.Session()

# Login to the UniFi Controller
login_data = json.dumps({'username': username, 'password': password})
headers = {'Content-Type': 'application/json'}

response = session.post(login_url, data=login_data, headers=headers, verify=False)
if response.status_code != 200:
    print("Failed to log in to the UniFi Controller")
    exit()

# Get list of sites
sites_response = session.get(sites_url, verify=False)
sites_data = sites_response.json()['data']

# Check each site for guest network and captive portal settings
for site in sites_data:
    site_name = site['desc']
    settings_response = session.get(f"{controller_url}/api/s/{site['name']}/get/setting", verify=False)
    settings_data = settings_response.json()['data']
    
    for setting in settings_data:
        if setting.get('key') == 'guest_access':
            if setting.get('portal_enabled', False):
                print(f"Site '{site_name}' is using a guest network with a captive portal.")

# Logout from the controller
session.get(f"{controller_url}/logout", verify=False)
