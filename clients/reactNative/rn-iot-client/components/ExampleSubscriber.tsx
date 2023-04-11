import React, { useCallback, useEffect } from 'react'
import { useState,} from "react";
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';
import { IotMessage } from './IotClient/IotClient';
import { useIot } from './IotClient/IotProvider';

export const ExampleSubscriber = () => {
    const {newMessage} = useIot();
    const [messages, setMessages] = useState<Array<IotMessage>>([]);
    const [filteredMessages, setFilteredMessages] = useState<Array<IotMessage>>([]);

    useEffect(()=>{
      const newMessages = [...messages]
      newMessages.push(newMessage)
      setMessages(newMessages)

    },[newMessage])

    useEffect(()=>{
      if(newMessage.topic == 'topic1'){
        const newMessages = [...filteredMessages]
        newMessages.push(newMessage)
        setFilteredMessages(newMessages)
      }
    },[newMessage])
  return (
    <View style={styles.container}>
      <>
            <Text>Subscriber component within IoT Context</Text>
            <Text>Listing All Messages</Text>
            {
              messages.map((item, index)=><Text key={index}>Topic: {item.topic} Payload:{item.message}</Text>)
            }
            <Text>Listing Messages sent to 'topic1'</Text>
            {
              filteredMessages.map((item, index)=><Text key={index}>Topic: {item.topic} Payload:{item.message}</Text>)
            }
    </>
    </View>
  )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#8e8e8e',
        alignItems: 'center',
        justifyContent: "flex-start",
        gap: 5,
        width: "100%"
      },
    textInput: {
      backgroundColor: '#fff',
      width: 200,
      textAlign: "center",
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
