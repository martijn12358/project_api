from api import Api
import threading
from database_functions import Database
from mqtt_broker import mqtt_broker
import json

with open('settings.json', 'r') as file:
    settings = json.load(file)

broker = settings['broker']
port = settings['port']
username = settings['username']
password = settings['password']
db_host = settings['db_host']
db_user = settings['db_user']
db_password = settings['db_password']
db = settings['db']
rs_db = settings['rs_db']
fl_db = settings['fl_db']

try:
    database = Database(host=db_host, user=db_user, password=db_password, database=db)

    database.connect_database()
    database.database_checker()
    if rs_db:
        database.reset_database()
    if fl_db:
        database.fill_database()

    mqtt_client = mqtt_broker(broker=broker, port=port, username=username, password=password, database=database)
    api = Api(database=database)

    thread_api = threading.Thread(target=api.run)
    thread_mqtt = threading.Thread(target=mqtt_client.run)
    try:
        thread_api.start()
    except Exception as e:
        print(e)
    try:
        thread_mqtt.start()
    except Exception as e:
        print(e)

except Exception as e:
    print(e)

