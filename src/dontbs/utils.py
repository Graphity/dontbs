import os
import json
import requests

MODULE_DIR = os.path.dirname(__file__)
CACHE = os.path.join(MODULE_DIR, 'goals.json')


def set_gh_goal(contributions: int) -> None:
    with open(CACHE) as f:
        data = json.load(f)
        data['gh_contributions'] = contributions
        
    with open(CACHE, 'w') as f:
        json.dump(data, f, indent=2)


def get_gh_goal() -> int:
    with open(CACHE) as f:
        data = json.load(f)
        return data['gh_contributions']


def generate_insult() -> str:
    endpoint = "https://insult.mattbas.org/api/insult"
    r = requests.get(endpoint)
    return r.text.strip()
