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

# Check each site for devices and clients
for site in sites_data:
    site_name = site['desc']
    site_key = site['name']

    # Checking for devices
    devices_url = f"{controller_url}/api/s/{site_key}/stat/device"
    devices_response = session.get(devices_url, verify=False)
    devices_data = devices_response.json()['data']

    # Checking for clients
    clients_url = f"{controller_url}/api/s/{site_key}/stat/sta"
    clients_response = session.get(clients_url, verify=False)
    clients_data = clients_response.json()['data']

    if not devices_data and not clients_data:
        print(f"Site '{site_name}' is empty (no devices and no clients).")

# Logout from the controller
session.get(f"{controller_url}/logout", verify=False)
