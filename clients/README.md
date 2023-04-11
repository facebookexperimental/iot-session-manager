# IoT Client Design

## Configuration
ClientId -
SessionId -
SessionPin -

JoinSession URL
Broker IP
Broker Port

## External Methods

### Connect (sessionId, sessionPin, ClientId)
Sends JoinSessionRequest HTTP Post to Session Manager API, recieves token
Uses token to connect to MQTT broker with the clientId as username and token as password.

### Subscribe(topic, callback)
Subscribes to a topic with provided callback function that will be triggered when a message with
that topic is recieved.

### Publish (topic, payload)
Publishes payload to a given topic.

## Internal Methods

### JoinSessionRequest

### MQTT Open

### On Message

## Events

### OnConnecting
### OnConnected
### OnFail
### OnDisconnected
