import json

with open('app/config/jwt_info.json', 'r') as f:
    jwt_config = json.load(f)

jwt_config_info = jwt_config['JWT']['JWT_SECRET_KEY']