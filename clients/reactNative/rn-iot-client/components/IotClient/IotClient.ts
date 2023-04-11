// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Paho from 'paho-mqtt';
import config from './config.json'

export type SessionData = {
    client: string,
    id: string,
    pin: string,
}

export type IotSubscription = {
    callback: (params:string)=>any,
    topic: string,
}

export type IotConfig = {
    authUrl: string,
    brokerIp: string,
    brokerPort: string,
    clientId: string
}

export type IotState = {
    connected: boolean
}

export type IotMessage = {topic:string, message:string}

export class IotClient {
    token: string
    sessionId: string
    clientId: string
    config: IotConfig
    client: Paho.Client
    onStateChange: (state:IotState)=>void
    onIotMessage: (message: IotMessage)=>any

    constructor(onStateChange:(state:IotState)=>void, onIotMessage: (message: IotMessage)=>any ){
        this.token = '';
        this.config = config;
        this.clientId = config.clientId;
        this.client = new Paho.Client(
            this.config.brokerIp,
            parseInt(this.config.brokerPort),
            this.clientId=this.clientId
            )
        this.client.onMessageArrived = this.onMessage.bind(this);
        this.client.onConnectionLost = this.onDisconnect.bind(this);
        this.sessionId = '';
        this.onStateChange = onStateChange;
        this.onIotMessage = onIotMessage;


    }

    joinSession(sessionId:string, sessionPin:string){
        console.log(`Joining Session: ${sessionId} ${sessionPin}`)
        this.sessionId = sessionId;
        const bodyData = {
            id:sessionId,
            pin:sessionPin,
            client: this.clientId,
        };
        fetch(this.config.authUrl, {
            method: 'POST',
            headers: {
                Accept: 'application.json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
        })
        .then(response =>{
            return response.json()
        } )
        .then(data=>{

            this.token=data.token
            this.client.connect({
                onSuccess: ()=>this.onConnected(this.sessionId),
                userName: this.clientId,
                password: data.token,
                useSSL: true
            })
            console.log(`Connected to: ${this.sessionId}`)
        }
        ).catch(error=>console.error(error))
    }

    onConnected(sessionId:string){
        console.log("MQTT Connected")
        console.log(`Subscribing to: /${sessionId}/#`)
        this.sessionId = sessionId;
        this.client.subscribe(`/${sessionId}/#`)
        this.onStateChange({connected: true})
    }
    onDisconnect(){
        console.log("MQTT Disconnected")
        this.onStateChange({connected:false})
    }

    onMessage(message:Paho.Message){
        console.log("Message recieved")
        console.log(message.destinationName)
        console.log(message.payloadString)
        const topic = message.destinationName.split('/')[2]
        this.onIotMessage({topic, message:  message.payloadString})
    }

    publish(topic:string, payload:string){
        const fullTopic = `/${this.sessionId}/${topic}`
        console.log(`Publishing to: ${fullTopic} with Payload: ${payload}`)
        this.client.send(fullTopic,payload)
    }

    disconnect(){
        this.client.disconnect();
    }
}
