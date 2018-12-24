import paho.mqtt.client as paho
import serial

mqtt_server ="192.168.0.22"
mqtt_port = 1883
mqtt_topic_state ="netmedias/fan/status"
mqtt_topic_command ="netmedias/fan/switch"
mqtt_user_name ="homeassistant"
mqtt_password = "welcome"
s = serial.Serial("/dev/ttyS0", 57600)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    client.publish(mqtt_topic_state, msg.payload.decode("UTF-8"), qos=0)
    
    s.write(msg.payload.decode("UTF-8"))

client = paho.Client()
client.username_pw_set(mqtt_user_name, mqtt_password)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(mqtt_server, mqtt_port)
client.subscribe(mqtt_topic_command, qos=0)
client.loop_forever()