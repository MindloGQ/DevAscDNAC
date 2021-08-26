import requests
from requests.auth import HTTPBasicAuth

#DNAC Sandbox Credentials
DNAC_USER='devnetuser'
DNAC_PASSWORD='Cisco123!'

def get_auth_token():
    """
    this function retrives a token from DNAC Center
    """
    url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD))  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use

def get_device_list():
    """
    This function retrives a list of devices managed by DNAC
    """
    global token #Make the token variable available to all functions
    token = get_auth_token() # Get Token
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr)  # Make the Get Request
    device_list = resp.json()
    get_device_id(device_list)

def get_device_id(device_json):
    for device in device_json['response']: # Loop through Device List and Retreive DeviceId
        print("Fetching Interfaces for Device ----> {}".format(device['hostname']))
        print('\n')
        get_device_int(device['id'])
        print('\n')

def get_device_int(device_id):
    """
    Building out function to retrieve device interface. Using requests.get to make a call to the network device Endpoint
    """
    url = "https://sandboxdnac.cisco.com/api/v1/interface"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    querystring = {"macAddress": device_id} # Dynamically build the querey params to get device spefict Interface info
    resp = requests.get(url, headers=hdr, params=querystring)  # Make the Get Request
    interface_info_json = resp.json()
    print_interface_info(interface_info_json)

def print_interface_info(interface_info):
    print("{0:25}{1:7}{2:20}{3:25}{4:15}{5:15}{6:25}". format("portName", "vlanId", "portMode", "portType", "duplex", "status", "description"))
    for intf in interface_info['response']:
        if intf['status'] == 'up' and intf['vlanId'] == "1" and intf['portMode'] == "access":
            print("{0:25}{1:7}{2:20}{3:25}{4:15}{5:15}{6:25}".
                format(str(intf['portName']),
                        str(intf['vlanId']),
                        str(intf['portMode']),
                        str(intf['portType']),
                        str(intf['duplex']),
                        str(intf['status']),
                        str(intf['description'])))

"""
Here we start the chain reaction.
1. we call the get_device_list() function
2. the get_device_list() function will use the get_auth_token() function to retrieve the token
3. the get_device_list() function will retrieve the list of devices managed by DNAC
4. the get_device_list() function will call the get_device_id() function 
5. the get_device_id() function will retrieve the device id's of all the devices
5. the get_device_id() function will call the get_device_int() function
6. the get_device_int() function will retrieve all the interfaces from each device
7. the get_device_int() function will call the print_interface_inf() function
8. the print_interface_info() function will print a table with interface information
######LET'S GOOOOO!!!!!!######
"""
get_device_list()