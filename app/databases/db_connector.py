import json
import mysql.connector

with open('app/databases/db_info.json', 'r') as f:
    db_config = json.load(f)

db = mysql.connector.connect(
    host=db_config['Database']['host'],
    user=db_config['Database']['user'],
    password=db_config['Database']['password'],
    database=db_config['Database']['database'],
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()
