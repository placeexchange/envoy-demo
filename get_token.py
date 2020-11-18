"""This is a slightly modified version of the sample snippet provided by auth0 on our M2M application's Quick Start tab."""

import http.client
import json
from os import environ

conn = http.client.HTTPSConnection(environ["AUTH0_DOMAIN"])

payload = {
    "client_id": environ["CLIENT_ID"],
    "client_secret": environ["CLIENT_SECRET"],
    "audience": environ["API_AUDIENCE"],
    "grant_type": "client_credentials",
}

headers = {"content-type": "application/json"}
conn.request("POST", "/oauth/token", body=json.dumps(payload), headers=headers)
res = conn.getresponse()
data = json.loads(res.read())

print(data["access_token"], end='')
