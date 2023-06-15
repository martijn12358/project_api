import paho.mqtt.client as mqtt

broker = "eu1.cloud.thethings.network"
port = 1883
username = "application-test-bike-mileage"
password = "NNSXS.KGQ3626QBCSRLOFIZSWGV6VH5B3LOOYFFCESSDI.GB5XQX3T45IWOABT3ZOYMGAJ7TRJ554MH7TPE6Q6ALBKHSC6WNJA"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected with result code " + str(rc))
        client.subscribe("application-test-bike-mileage/devices/eui-70b3d57ed005e82c/up")
    else:
        print("\nFailed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))



def run():

    client = mqtt.Client()
    client.on_connect = on_connect
    print("test")
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect(broker, port, 60)
    print("running mqtt client")
    client.loop_forever()

