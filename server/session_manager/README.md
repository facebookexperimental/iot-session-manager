# Session Manager App
The Session Manager app is an asynchronous python based application that provides simple creation of IoT 'sessions' that other devices can join. It is intended to be deployed with a MQTT Broker to provide the IoT communication.

The API utilizes Tornado to create two http endpoint (exposes two separate ports defined in settings) that can be authenticated separately: admin and iot.

The admin port is intended to be used by trusted clients to manage sessions.

The iot port is used for authenticating other clients to join these session. When JWT authentication is enabled for the iot-session-manager MQTT Broker, the session manager provides a JWT token to the iot client.


## The Session Model
The Session Manager creates and maintains a list of 'sessions'. The 'Session' class is the primary data model in the application. Each session has the following fields:
- id
- pin
- type

When a session is created, a random id and pin (the length of these are set in settings) are assigned to the session and returned to the session admin. The session admin can now distribute the id and pin to related devices that would like to connect to the session.


### Session Conductor
A session is also instantiated with a 'conductor' instance.  Different types of conductors can be instantiated by assignging a different 'type' in the create session function.  The configuration of the conductor classes is done in settings.py.

This conductor can contain functions that handle requests via the Session Manager's 'conductorRequest' API route.

The conductor can also run its own asyncronous event loop, which can connect to the IoT session to monitor the messages sent by clients or even send messages to coordinate a network of clients.

The conductor_interface class is intended to be extended to make powerful conductors for the network.

In some cases, the conductor_interface may just be an interface to another microservice running the conductor logic elsewhere.

## The SessionManager Class
The Session Manager is the controlling class for the Session model, and it also provides functions to the API handlers. This is where the main logic of the class takes place.

### Admin Functions
Each of the functions below also exists as an API route in the admin server:
#### Create Session (session_type)
Creates a session class for a given type, which instantiates a conductor of that type.

Returns session_id and session _pin.

#### Close Session (session_id)
Closes a session so it is no longer active.

#### Conductor Request (session_id, method: str, params: str)
Calls the conductor_request function for the matching session with a set of JSON parameters.
The conductor calls the callback associated with the method string and uses the params as arguments for that function.
The request returns the result of the conductor handler.

### IoT Functions
#### Join Session (session_id, session_pin)
This is intended to be accessible to any device. If the session_id and session_pin are validated, the session_manager returns a token. If JWT auth is configured, this is a signed JWT token used for authenticating with the MQTT broker.

### Session Storage
Initially this minimal application stores the sessions in a list in memory and can save the active session data locally to the disk via a JSON file. Upon start, it loads the session data from the disk.

#### Storage extension
This storage could be extended simply to store with a backend or a NoSQL database, that could provide other applications to information on the active sessions.

## HTTP Server
The HTTP server is provided by an asynchonous Tornado application.

### Authentication
There are two main consumers of the HTTP server
- Admins who will create, close, and call conductor requests for sessions.
- IoT clients who do not need to manage sessions, but only need an authenticated token to join the MQTT broker.

One of the simplest and most secure methods of authenticating the two different consumers would be to restrict the Admins to specific IP addresses (such as VPN network), and then only open the IoT port to the public.

Additionally custom authentication could be added to the Admin server.

### Admin Server Authentication
In the current version, there is no additional authentication to the Admin HTTP request handlers, but a very simple framework is in place that could be extended to either add in a simple user/credential setup, JWT authentication, or other method.

#### OAuth Integration
Tornado provides integration with the OAuth2 framework.  If additional authentication is needed beyone port restriction, it is reccomended to utilize some for of OAuth or authentication service rather than build your own.


### IoT Server Authentication
This app is initially intended to enable the IoT port to any public device.  The only route to this API is the joinSession route which requires ID and Pin.  Any device should be able to join a session if they have the correct ID and Pin for the session (similar to a VC meeting)

### MQTT Broker JWT Authentication
The MQTT Broker utilizes a JWT auth plugin (more info in the main README) to authenticate the MQTT broker.

One of the primary purposes of the Session Manager app is that it generates and signs the JWT tokens.

#### MQTT JWT ACL
Each JWT is created with an ACL payload for the client which restricts the client.

The ACL restricts the topics that the clients can subscribe or publish to topics on, and it also has a set expiration time for the token (default 24hrs).  This can be configured in the utils/jwt_helpers.py file.

By default, MQTT clients are restricted to topics that begin with the session_id.

For example, for a session with an ID of 123456.
- Allowed: /123456/test
- Allowed: /123456/#
- Allowed: /123456/test/customtopic
- Denied: /test/customtopic
- Denied: /#

MQTT clients are also required to use the session_id as their username when connecting to the broker.

## Main Asyncio Event Loop
Since the app is fully Asyncio based, it is easy to create a primary async event loop that works across the app but is separate from the Tornado app. This could be used for tasks that need to happen at regular intervals, regular communications with other services, etc.. An example of this has been created and initialized in main.py. You can extend the details of the loop in async_loop.py.
