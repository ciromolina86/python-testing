from paho.mqtt.client import Client
from random import randrange, uniform
import time


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print("Topic: " + msg.topic + " QoS: " + str(msg.qos) + " Payload: " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def main():
    mqttClient2 = Client()
    mqttClient2.on_message = on_message
    mqttClient2.on_connect = on_connect
    mqttClient2.on_subscribe = on_subscribe

    mqttClient2.connect("broker.hivemq.com", 1883, 60)

    mqttClient2.subscribe('itg/cirom/temp/')
    mqttClient2.loop_forever()


if __name__ == '__main__':
    main()
