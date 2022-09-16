import os
from pprint import pprint

import requests

token = os.environ["API_TOKEN"]

res = requests.get(
    "https://api.github.com/repos/austin3dickey/test-github-app/commits/4d186e29b16ee78bdb55466df87292bf6e3c51fb/check-suites",
    headers={"Authorization": f"Bearer {token}"},
)
pprint(res.__dict__)
res.raise_for_status()
