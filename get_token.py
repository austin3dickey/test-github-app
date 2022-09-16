import argparse
from datetime import datetime, timedelta
from pprint import pprint

import jwt
import requests

parser = argparse.ArgumentParser(description="Get a GitHub App installation token")
parser.add_argument("-k", help="Private key file contents", required=True)
parser.add_argument("-a", help="App ID", required=True)
args = parser.parse_args()

private_key = args.k
app_id = args.a
assert private_key
assert app_id

# get JWT
payload = {
    "iss": app_id,
    "iat": datetime.utcnow() - timedelta(minutes=1),
    "exp": datetime.utcnow() + timedelta(minutes=10),
}
jw_token = jwt.encode(payload=payload, key=private_key, algorithm="RS256")

# get installations of this app
res = requests.get(
    "https://api.github.com/app/installations",
    headers={"Authorization": f"Bearer {jw_token}"},
)
res.raise_for_status()

# we assume there is 1 installation (with multiple repos)
install_id = res.json()[0]["id"]

# get the API token
res = requests.post(
    f"https://api.github.com/app/installations/{install_id}/access_tokens",
    headers={"Authorization": f"Bearer {jw_token}"},
)
res.raise_for_status()

print(res.json()["token"])
