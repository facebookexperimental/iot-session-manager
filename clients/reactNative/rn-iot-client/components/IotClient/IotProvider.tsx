// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { createContext, useState, useContext, useRef, useCallback, useEffect } from "react";
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';
import { IotClient } from './IotClient';
import type { IotSubscription, IotState, IotMessage} from './IotClient';
import * as SecureStore from 'expo-secure-store';

import React from 'react'

/*
// IoT Provider provides a Context to the rest of the app to use the IoT
// Control class.  Also manages the state and connection of logon.

Providers are a helpful way to creat an interface to a pure JS/TS class running in the app.
The core application logic can live outside of the React framework and then Context brings that into the app
in a way that all the components can use the same instance of the class.

*/

type IotClientContext = {
    connected: boolean
    newMessage: IotMessage
    publish: (topic:string, message:string)=>void;
}

interface IotProperties {
    children?: React.ReactNode,
}


const IotContext = createContext<IotClientContext>({}as IotClientContext)

const IotProvider = ({children}:IotProperties)=>{
    const [sessionId, setSessionId] = useState('');
    const [sessionPin, setSessionPin] = useState('');
    const [connected, setConnected] = useState(false);
    const [newMessage, setNewMessage] = useState<IotMessage>({topic:'',message:''})

    useEffect(()=>{
        console.log("Iot Provider Starting Up, looking for session creds");
        loadSessionCreds().catch(console.error);
    },[])

    const onStateChange = useCallback((state:IotState)=>{
        console.log(`Connection State Changed from Client: ${state.connected ? 'connected':'disconnected'}`)
        setConnected(state.connected);
    },[setConnected])


    const onIotMessage = useCallback((message:IotMessage)=>{
        setNewMessage(message)
    },[])

    const iotClient = useRef(new IotClient(onStateChange, onIotMessage));

    const publish = (topic:string, message:string)=>{
        iotClient.current.publish(topic, message)
    }

    const logout = async ()=>{
        iotClient.current.disconnect()
        await clearSessionCreds();
    }

    const connect = async (id:string, pin:string)=>{
        iotClient.current.joinSession(id,pin)
        await saveSessionCreds();
    }

    // Storage functions only available for Native
    const saveSessionCreds = async ()=>{
        await SecureStore.setItemAsync("sessionId",sessionId);
        await SecureStore.setItemAsync("sessionPin",sessionPin);
    }

    const loadSessionCreds = async ()=>{
        let id = await SecureStore.getItemAsync("sessionId");
        setSessionId(id ?? '');
        let pin = await SecureStore.getItemAsync("sessionPin");
        setSessionPin(pin ?? '')
        console.log(`Loaded Session Creds ${id}, ${pin}`)
        if(id !== '' && id && pin){
            iotClient.current.joinSession(id,pin)
        }
    }

    const clearSessionCreds = async ()=>{
        await SecureStore.deleteItemAsync("sessionId");
        await SecureStore.deleteItemAsync("sessionPin");
    }

    return(
        <IotContext.Provider value={{
            connected,
            publish,
            newMessage
        }}>
        {connected ?
        <View style={styles.header}>
            <Text style={styles.text}>Connected to Session: {sessionId}</Text>
            <Button title="Leave Session" onPress={logout}/>
        </ View>
        :
        <View style={styles.header}>
            <TextInput style={styles.textInput} placeholder="Session Id" onChangeText={setSessionId}/>
            <TextInput style={styles.textInput} placeholder="Session Pin" onChangeText={setSessionPin}/>
            <Button title="Join Session" onPress={()=>connect(sessionId,sessionPin)}/>
        </View>
    }


        {children}
        </IotContext.Provider>
    )
}


const useIot = ()=>{
    const context=useContext(IotContext);
    if(!context){
        throw new Error('useIot must be used within Iot Context Provider')
    }
    return context;
}

const styles = StyleSheet.create({
    textInput: {
      backgroundColor: '#fff',
      width: "30%",
      textAlign: "center",
    },
    header: {
        flexDirection: "row",
        backgroundColor: '#8e8e8e',
        gap: 20,
        paddingTop: 50,
        paddingBottom: 10,
        paddingHorizontal: 25,
        width: "100%",
        height: 100,

    },
    button: {
        color: '#2196F3',
    },
    text: {
        textAlignVertical: "center",
        fontSize:15,
        width: "50%",

    }
  });


export {IotContext, IotProvider, useIot}
