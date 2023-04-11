# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging
import requests
import paho.mqtt.client as mqtt
import json

logger = logging.getLogger()

'''
IoT Client Script

This IoT client can be used by other python applications to authenticate to the session manager
and connect to the MQTT broker. It can then be used to subscribe and publish to topics.
This class can be extended and improved to support handling of messages via the on-message class.
'''

class IotClient():
    def __init__(self, config) -> None:
        self.token = ''
        self.config = config
        self.connected = False
        self.subscriptions = {}
        self._client_id = config.get('client_id')
        self._client = mqtt.Client(client_id="", transport="TCP")
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_publish = self._on_publish
        self._client.on_disconnect = self._on_disconnect


    def _on_message(self, client, userdata, msg):
        logger.info(f"Message Recieved: Topic: {msg.topic}, payload: {msg.payload}")
        short_topic = msg.topic.split('/')[2]
        handlerList = self.subscriptions.get(short_topic)
        if handlerList:
            for handler in handlerList:
                handler(msg.payload)
        else:
            logger.info(f"No handlers found for {msg.topic}")

    def _on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT")
        self.connected = True

    def _on_disconnect(self, client, userdata, rc):
        logger.info("Disconnected from MQTT")
        self.connected= False

    def _on_publish(self, client, userdata, rc):
        logger.info({"publishing": None, "published_rc": rc})
        pass

    def join_session(self,session_id, session_pin):
        logger.info(f'Attempting to connect with {session_id} and {session_pin}')
        self.session_id = session_id
        body_data = {
            "id":session_id,
            "pin":session_pin,
            "client": self._client_id
        }
        response = requests.post(f'{self.config["auth_url"]}',json=body_data)
        try:
            data = response.json()
            logger.info(f"Recieved token {data['token']}")
            self._client.username_pw_set(username=self._client_id, password=data["token"])
            self._client.connect(self.config["broker_ip"], self.config["broker_port"])
            self._client.loop_start()
        except:
            logger.info(f"ERROR IOT CONNECTION: {response.content}")


    def topic_subscribe(self, topic: str, callback, qos=0):
        self._client.subscribe(f'/{self.session_id}/{topic}', qos)
        handlerList = self.subscriptions.get(topic)
        if handlerList:
            handlerList.append(callback)
        else:
            handlerList = [callback]
        self.subscriptions[topic] = handlerList

    def publish(self, topic: str, payload:str):
        self._client.publish(f'/{self.session_id}/{topic}',payload)
