import base64
from datetime import datetime

import paho.mqtt.client as mqtt
import json



class mqtt_broker:
    def __init__(self, broker, port, username, password, database):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("\nConnected with result code " + str(rc))
            client.subscribe("v3/application-test-bike-mileage@ttn/devices/eui-70b3d57ed005e82c/up")
        else:
            print("\nFailed to connect, return code %d\n", rc)

    def _on_message(self, client, userdata, msg):
        print(msg.payload)
        self._data_extractor(json.loads(msg.payload))

    def _data_extractor(self, message):
        payload = message["uplink_message"]["frm_payload"]
        date = message["received_at"]
        date_parts = date.split('.')
        date = date_parts[0]
        datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M")

        gateway_name = message["uplink_message"]["rx_metadata"][0]["gateway_ids"]["gateway_id"]

        try:
            longitude = message["uplink_message"]["rx_metadata"][0]["location"]["longitude"]
            latitude = message["uplink_message"]["rx_metadata"][0]["location"]["latitude"]
        except Exception as e:
            latitude = 52.219373
            longitude = 6.895129
            print("location data not available, inserting standard location")

        bytes_mesg = base64.b64decode(payload).hex()
        bytes_array = [bytes_mesg[i:i + 2] for i in range(0, len(bytes_mesg), 2)]
        distance_bytes = bytes_array[1] + bytes_array[2]
        timer_bytes = bytes_array[3] + bytes_array[4]
        bytes_array_n = [int(bytes_array[0], 16), int(distance_bytes, 16), int(timer_bytes, 16)]
        wheelrotation_second = (64 / 1000000) * bytes_array_n[2]

        self.database.enter_message(wheelrotation_second, bytes_array_n[1], date_parts[0], longitude, latitude, "markers",
                                         gateway_name, 0)
        self.database.enter_bike_battery(bytes_array_n[0])

    def run(self):
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.username_pw_set(self.username, self.password)
        client.connect(self.broker, self.port, 60)
        print("running mqtt client")
        client.loop_forever()
