// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.


using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TestPingSubscriber : MonoBehaviour
{
    public GameObject IotClientObject;
    public GameObject TextObject;
    private IotClient IotClient;

    private Text text;

    void Awake()
    {

    }
    // Start is called before the first frame update
    void Start()
    {
        this.IotClient =  IotClientObject.GetComponent<IotClient>();
        this.IotClient.TopicSubscribe(gameObject,"testPing","TestPingRcv");
    }

    // Update is called once per frame
    void Update()
    {

    }
    public void TestPublish()
    {
        double testTimeSent = Time.realtimeSinceStartupAsDouble;
        Debug.Log("Test Publish Called");
        Debug.Log(testTimeSent.ToString());
        this.IotClient.Publish("testPing", testTimeSent.ToString());
    }
    public void TestPingRcv(string message)
    {
        Debug.Log("Subscriber Message Recieved for topic: " + message);
        double timeSent = System.Double.Parse(message);
        double timeRcv = Time.realtimeSinceStartupAsDouble;
        double timeDelta = timeRcv - timeSent;
        int roundedMs = System.Convert.ToInt32(timeDelta*1000.0);
        Debug.Log("Received Test Ping Response: "+ roundedMs.ToString());
        text = TextObject.GetComponent<Text>();
        text.text = roundedMs.ToString() + "ms";
    }
}
