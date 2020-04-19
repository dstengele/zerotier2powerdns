import requests

# Settings
ZONE = 'example.com'
POWERDNS_API_ENDPOPINT = 'http://localhost:8081/api/v1/servers/localhost'
POWERDNS_API_KEY = 'SECRET'

ZEROTIER_API_ENDPOINT = 'https://my.zerotier.com/api'
ZEROTIER_API_KEY = 'SECRET'
ZEROTIER_NETWORK_ID = 'xxxxxxxxxxxxxxxx'
# END Settings

headers = {
    'powerdns': {
        'X-API-Key': POWERDNS_API_KEY,
        'Content-Type': 'application/json'
    },
    'zerotier': {
        'Authorization': f'Bearer {ZEROTIER_API_KEY}'
    }
}

# Get all members in the Zerotier Network
network_members = requests.get(f'{ZEROTIER_API_ENDPOINT}/network/{ZEROTIER_NETWORK_ID}/member',
                               headers=headers['zerotier']).json()
for network_member in network_members:
    name = network_member['name']
    hostname = '.'.join(name.split('.')[::-1] + ['zt'] + [ZONE])
    ipv4 = network_member['config']['ipAssignments'][0]
    ipv6_raw = f'fd{network_member["networkId"]}9993{network_member["nodeId"]}'
    ipv6 = ':'.join(ipv6_raw[i:i + 4] for i in range(0, len(ipv6_raw), 4))

    zone_content_request = requests.get(f'{POWERDNS_API_ENDPOPINT}/zones/{ZONE}',
                                        headers=headers['powerdns'])
    zone_content_request.raise_for_status()
    zone_content = zone_content_request.json()

    rrsets = [{
        'name': hostname + '.',
        'type': 'A',
        'ttl': 86400,
        'changetype': 'REPLACE',
        'records': [{
            'content': ipv4,
            'disabled': False
        }]
    }, {
        'name': hostname + '.',
        'type': 'AAAA',
        'ttl': 86400,
        'changetype': 'REPLACE',
        'records': [{
            'content': ipv6,
            'disabled': False
        }]
    }]
    replace_operation_request = requests.patch(f'{POWERDNS_API_ENDPOPINT}/zones/{ZONE}',
                                               headers=headers['powerdns'],
                                               json={'rrsets': rrsets})
    replace_operation_request.raise_for_status()
