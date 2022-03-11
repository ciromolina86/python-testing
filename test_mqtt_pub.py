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
    mqttClient1 = Client()
    mqttClient1.on_connect = on_connect
    mqttClient1.on_publish = on_publish

    mqttClient1.connect("broker.hivemq.com", 1883, 60)

    for x in range(10):
        randNumber = uniform(20.0, 21.0)
        mqttClient1.publish(topic="itg/cirom/temp/", payload=randNumber)
        time.sleep(1)

    mqttClient1.disconnect()


if __name__ == '__main__':
    main()
