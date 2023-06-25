from api import Api
import threading
from database_functions import Database
from mqtt_broker import mqtt_broker

broker = "eu1.cloud.thethings.network"
port = 1883
username = "application-test-bike-mileage@ttn"
password = "NNSXS.KGQ3626QBCSRLOFIZSWGV6VH5B3LOOYFFCESSDI.GB5XQX3T45IWOABT3ZOYMGAJ7TRJ554MH7TPE6Q6ALBKHSC6WNJA"
db_host = "localhost"
db_user = "project_dev"
db_password = "project_password"
db = "data"


try:
    database = Database(host=db_host, user=db_user, password=db_password, database=db)

    database.connect_database()
    database.database_checker()
    database.reset_database()
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

