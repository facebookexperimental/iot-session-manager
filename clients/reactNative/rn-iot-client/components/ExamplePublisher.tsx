// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from 'react'
import { useState,} from "react";
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';
import { useIot } from './IotClient/IotProvider';

export const ExamplePublisher = () => {
    const {publish} = useIot();
    const [topic, setTopic] = useState('');
    const [message, setMessage] = useState('');
  return (
    <View style={styles.container}>
            <Text>Publisher component within IoT Context</Text>
            <TextInput style={styles.textInput} placeholder="topic" onChangeText={setTopic}/>
            <TextInput style={styles.textInput} placeholder="message" onChangeText={setMessage}/>
            <Button title="Publish" onPress={()=>publish(topic,message)}/>
    </View>
  )
}

const styles = StyleSheet.create({
    container: {
        flex: 0.5,
        backgroundColor: '#8e8e8e',
        alignItems: 'center',
        justifyContent: 'flex-start',
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
