import json

with open('app/config/session_info.json', 'r') as f:
    session_config = json.load(f)

session_info = session_config['SESSION']
