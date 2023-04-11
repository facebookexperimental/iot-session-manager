// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';

import { IotProvider } from './components/IotClient/IotProvider';
import { ExamplePublisher } from './components/ExamplePublisher';
import { ExampleSubscriber } from './components/ExampleSubscriber';

export default function App() {

  return (
    <View style={styles.container}>
       <IotProvider>
       <Text>Welcome to the App</Text>
       <ExamplePublisher/>
       <ExampleSubscriber/>
       </IotProvider>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: "flex-start",
    gap: 5
  },
});
