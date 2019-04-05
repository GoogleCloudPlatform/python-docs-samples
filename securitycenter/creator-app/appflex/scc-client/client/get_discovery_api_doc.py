import json
import requests
import sys

developer_key = sys.argv[1]

response = requests.get("https://securitycenter.googleapis.com/$discovery/rest?key={}".format(developer_key))

if response.status_code != 200:
    print("Error. Code={}, Headers={}, Content={}".format(response.status_code, response.headers, response.content))
    sys.exit(1)
    
doc = json.dumps(json.loads(response.content.decode('utf-8')), sort_keys=True, indent=4)

with open('./v1beta1/The_public_Cloud_Security_Command_Center_API.json', 'w+') as f:
    f.write(doc)

print("Discovery API doc updated.")
