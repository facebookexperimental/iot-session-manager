# IoT Session Manager

## Features:
- Simple deployment of MQTT Broker, Web Proxy with HTML serving, Session manager
- RSA Encrypted token authentication for session management and IoT login
- Logging for all services

# Deployment
## Two Deployment Modes:
1. Development
    - no authentication to control service API,
    - no MQTT broker authentication

2. Production
    - Auth service authentication for control service - validate with public key
        - Auth service Options
        - OKTA
        - multiple app public keys for multi-app authentication


## Dev Configuration - .env file configuration
Configuration for deployment happens in the .env file.
In this file you set the mode of authentication for the mqtt-broker and session manager app.

There are two 'modes' for authentication to the MQTT broker and both the broker and session manager builds depend on the mode.
- dev : No broker authentication
- dev_jwt_auth : Broker authentication with locally created RSA kay
    - session_manager needs private local key
    - mqtt_broker needs public local key


## Production Considerations and Setup
web_proxy
    - needs SSL Certs

mqtt_broker
    - needs SSL Certs
    - public key of KMS

session_manager
    - needs ARN of KMS key

# Authentication and Athorization

## Mosquitto (MQTT) broker JWT Authentication
The MQTT broker can be authenticated with custom JWT tokens that are created by the Session Manager.

The Mosquitto broker utilizes a JWT authentication plugin, and requires a third party binary to be installed in the repo:
https://github.com/wiomoc/mosquitto-jwt-auth

You can clone and build from source or download the prebuild release for linux and add it to this folder:
https://github.com/wiomoc/mosquitto-jwt-auth/releases/tag/0.4.0

You will need to adjust the location of the binary in the mosquitto.conf accordingly


## License
iot-session-manager is MIT licensed, as found in the LICENSE file.
