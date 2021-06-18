import requests
from requests.auth import HTTPBasicAuth
from dnac_config2 import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
import json


def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD))  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use

def get_device_list():
    """
    Building out function to retrieve list of devices. 
    Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token() # Get Token
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    
    device_list = resp.json() #This will return the list of devices in dictionary format
    
    device_list = json.dumps(device_list, indent=4) #this will make the device list more readable
    print(device_list)



get_device_list()