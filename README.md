# IoT Session Manager
This is a deployment ready application that creates a simple way for wireless device to device messaging over the internet or on local networks. This can be especially useful for rapid prototyping of systems that involve communication and coordination between multiple devices. The messaging is handled by the 'language of the Internet of Things' - MQTT.  One challenge with setting up an traditional MQTT broker is managing the connection and ACL of the different devices connected to the network.  The IoT Session Manager provides a simple API that manages clients, along with a Mosquitto broker, and web proxy that can all be deployed with a single docker compose command, and it can be used to create private 'sesssions' that clients can join.  MQTT traffic is restricted to those clients that have the ID and Pin for a given session, and they can only communicate to other devices in that session.

## Features:
- Simple deployment of MQTT Broker, Web Proxy with HTML serving, Session manager
- JWT token authentication for session management and IoT login
- Logging for all services

# Deployment
## Two Deployment Modes:
1. Development
    - No authentication to control service API
        - simple setup for local connectivity
    - Local JWT MQTT broker authentication 
        - custom RSA keys used locally
        - Keys need to be setup using the script in the deployment/certs/local_mqtt_keys

2. Production (WIP)
    - Reference RSA keys from AWS and BOTO3
        
## Docker Deployment
In both cases the server is deployed via docker compose. This creates three containers:
1. Mosquitto Broker (with or without JWT authentication plugin)
2. NGINX revers proxy and web server
3. Session Manager python Tornado API

Each of these services has an associated Dockerfile. 

### Deployment Steps:
1. Navigate to server/deployment
2. Configure the keys, certs, and dependent mqtt plugin (see below) depending on production or development deployment.
3. Configure the docker-compose.yaml file with your desired ports
4. Configure the .env file with the variables that will determine the type of deployment (more below)

Run `docker compose build`
Run `docker compose up`


## Dev Configuration - .env file configuration
Configuration for deployment happens in the .env file.
In this file you set the mode of authentication for the mqtt-broker and session manager app.

There are two 'modes' for authentication to the MQTT broker and both the broker and session manager builds depend on the mode.
- dev_no_auth : No broker authentication
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

# Authentication and Authorization

## Session Manager Authentication
Currently the session manager creates two separate ports for authentication (see session_manager README for more info). In production deployment, the  Admin port could be restricted to specific IP addresses to only allow those services to manage the sessions.  Alternatively the Session Manager API could be routed through the reverse proxy and custom authentication could be added to the Session Manager application via a user database or Tornado SSO. 

## Mosquitto (MQTT) broker JWT Authentication Dependencies
The MQTT broker can be authenticated with custom JWT tokens that are created by the Session Manager.  This is useful to restrict the connection and ACL for the network, but requires a dependency on https://github.com/wiomoc/mosquitto-jwt-auth.  More setup details are found in the README in the server/deployment/mqtt_broker/ folders.


# Example Clients
This repository also contains several example client classes that can be used to connect directly to the Session Manager server. 
Currently there are working clients for Python and Unity, but javascript (React Web/Native), c++ (Arduino/ESP), and uPy (Arduino/ESP) are on the roadmap. 

## License
iot-session-manager is MIT licensed, as found in the LICENSE file.
