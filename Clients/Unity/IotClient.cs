using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;
using UnityEngine.Networking;
using M2MqttUnity;
using uPLibrary.Networking.M2Mqtt.Messages;


// Data class used to submit the JoinSession request
[System.Serializable]
public class SessionData
{
    public string client;
    public string id;
    public string pin;
}

// Data class returned from the JoinSession request
[System.Serializable]
public class TokenResponse
{
    public string token;
}

// Subscription object for registration of topic subscriptions from game objects
class Subscription
{
    public GameObject go;
    public string topic;
    public string methodName;
}


/*
*   The IoT Client is an extension of the M2MqttUnity Client which must be included in the package
*   This client handles the connection to a session provided by the iot-session-manager.
*
*   Any game object with a reference to this script can
*       - Subscribe to topics via the TopicSubscription method.
*       - Publish messages to topics of their choice
*/

public class IotClient : M2MqttUnityClient
{
    private IDictionary<string, List<Subscription>> topicSubscriptions;

    [Header("IoT Client Configuration")]
    public string joinSessionUrl = "http://localhost:88/api/joinSession";
    public string clientId = "UnityExampleClient";
    public string sessionId = "none";
    public string sessionPin = "none";

    private void Awake()
    {
         topicSubscriptions = new Dictionary<string, List<Subscription>>();
    }


    /*
    * Functions to configure the Session ID and Session Pin via UI elements
    */
    public void SetSessionId(string sessionId)
    {
        this.sessionId = sessionId;
    }

    public void SetSessionPin(string sessionPin)
    {
        this.sessionPin = sessionPin;
    }


    /*
    * Primary IoT Client Interface Methods for joining session, subscribing, and publishing
    */

    // Triggers the connection to iot-session-manager. Typically called from button click, but could be called on startup.
    public void JoinSession()
    {
        StartCoroutine(JoinSessionRequest(sessionId , sessionPin));
    }

    // Publishes topic over MQTT and includes the sessionId base topic as required by the server
    public void Publish(string topic, string text = "")
    {
        byte[] message = System.Text.Encoding.UTF8.GetBytes(text);
        client.Publish("/"+this.sessionId+"/"+topic, message, MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
        Debug.Log("Message published to topic: "+topic+" with message "+"text");
    }

    // Stores the subscribing gameObject and methodName in a dictionary for the given topic, so messages are broadcast to that method name.
    public void TopicSubscribe(GameObject go, string topic, string methodName)
    {
        List<Subscription> handlerList = new List<Subscription>();
        Subscription newSub = new Subscription();
        newSub.go = go;
        newSub.topic = topic;
        newSub.methodName = methodName;
        // If existing subscriptions for topic are in dictionary, set handlerList to that list
        if(topicSubscriptions.ContainsKey(topic)){
            handlerList = topicSubscriptions[topic];
        }
        handlerList.Add(newSub);
        topicSubscriptions[topic] = handlerList;
        Debug.Log(go + " Subscribing to "+ topic + "with callback "+methodName);
    }


    /*
    *  Event Callback Methods - overriding MQTT client methods
    */

    // DecodeMessage or sometimes 'OnMessage' is called anytime a topic that is subscribed to is recieved
    protected override void DecodeMessage(string fulltopic, byte[] message)
    {
        string msg = System.Text.Encoding.UTF8.GetString(message);
        Debug.Log("Received: topic " + fulltopic + " message " + msg);
        var topicArray = fulltopic.Split('/');
        string topic = topicArray[2];
        Debug.Log("Shortened topic " + topic);

        List<Subscription> handlerList = new List<Subscription>();
        if(topicSubscriptions.ContainsKey(topic)){
            handlerList = topicSubscriptions[topic];
            foreach(Subscription sub in handlerList){
                    Debug.Log("Sending message to subscriber " + sub.go + " with callback "+ sub.methodName);
                    sub.go.SendMessage(sub.methodName, msg);
            }
        } else {
            Debug.Log("No subscriptions found for topic: " + topic);
        }
    }

    protected override void OnConnecting()
    {
        base.OnConnecting();
        Debug.Log("Connecting to broker on" + brokerAddress);
    }

    protected override void OnConnected()
    {
        base.OnConnected();
        Debug.Log("Connected to broker on " + brokerAddress + "\n");
        SubscribeAllTopics();
    }

    protected override void OnDisconnected()
    {
        Debug.Log("Disconnected from broker");
    }

    /*
    * Subscribes to all the topics for the session, if there is a concern of the app recieving too many unneeded messages, this could be removed
    * and you could subscribe to only topics as they are called in TopicSubscribe.  For ease of prototyping, subscribing to all topics is used.
    */
    protected void SubscribeAllTopics()
    {
        client.Subscribe(new string[] { "/" + this.sessionId + "/#" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        Debug.Log("Subscribing to all topics for session");
    }


    /*
    *   Join Session HTTP Request Methods
    *
    *   Posts session credentials to JoinSession method of server
    *   Gathers token from the server response
    *   Authenticates to MQTT and opens connection with token
    */
    IEnumerator JoinSessionRequest(string sessionId, string sessionPin)
    {

        SessionData data = new SessionData();
        data.client = this.clientId;
        data.id = sessionId;
        data.pin = sessionPin;

        string bodyJson = JsonUtility.ToJson(data);

        using (UnityWebRequest webRequest = new UnityWebRequest(this.joinSessionUrl, "POST"))
        {
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(bodyJson);
            webRequest.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
            webRequest.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            webRequest.SetRequestHeader("Content-Type", "application/json");
            yield return webRequest.SendWebRequest();

            switch (webRequest.result)
            {
                case UnityWebRequest.Result.ConnectionError:
                case UnityWebRequest.Result.DataProcessingError:
                    Debug.LogError(": Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.ProtocolError:
                    Debug.LogError( ": HTTP Error: " + webRequest.error);
                    break;
                case UnityWebRequest.Result.Success:
                    Debug.Log(":\nReceived: " + webRequest.downloadHandler.text);
                    string token = GetResponseToken(webRequest.downloadHandler.text);
                    MqttOpen(token);
                    break;
            }
            webRequest.Dispose();
        }
    }

    private string GetResponseToken(string responseText)
    {
        TokenResponse response = new TokenResponse();
        response = JsonUtility.FromJson<TokenResponse>(responseText);
        Debug.Log("Retrieved Token: "+response.token);
        return response.token;
    }

    private void MqttOpen(string token)
    {
        this.mqttUserName = this.clientId;
        this.mqttPassword = token;
        this.Connect();
    }
}
