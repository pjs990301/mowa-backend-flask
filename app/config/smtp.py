import json

with open('app/config/smtp_info.json', 'r') as f:
    smtp_config = json.load(f)

smtp_info = smtp_config['SMTP']
