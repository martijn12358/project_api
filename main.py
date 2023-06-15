import api
import database_functions
import mqtt_broker
import threading


try:
    database_functions.connect_database()
    database_functions.database_checker()

    thread_api = threading.Thread(target=api.app.run)
    thread_mqtt = threading.Thread(target=mqtt_broker.run)
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

