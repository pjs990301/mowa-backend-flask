import json

with open('app/config/jwt_info.json', 'r') as f:
    jwt_config = json.load(f)

jwt_config_info = jwt_config['JWT']['JWT_SECRET_KEY']
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box: **'Bearer &lt;your_JWT_token&gt;'**"
    }
}