using Microsoft.MixedReality.OpenXR;
using Microsoft.MixedReality.Toolkit.Input;
using Microsoft.MixedReality.Toolkit.Teleport;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.WSA.Input;

public class FloorDetector : MonoBehaviour
{
    private GestureRecognizer recognizer;
    public GameObject obj;
    public GameObject placeObj;
    public bool SetFloorEditor = false;
    // Start is called before the first frame update
    void Start()
    {
        recognizer = new GestureRecognizer(GestureSettings.Tap);
        //recognizer.SetRecognizableGestures(GestureSettings.Tap);
        //recognizer.Tapped += OnTap;
        //recognizer.StartCapturingGestures();
        obj.SetActive(false);
    }


    // private void OnTap(TappedEventArgs tap)
    // {
    //     var cursor = FindObjectOfType<AnimatedCursor>();
        
    //     if (cursor)
    //     {
    //         if (Vector3.Distance(Camera.main.transform.position, cursor.transform.position) > 3) return;

    //         var camPos = Camera.main.transform.position;
    //         obj.transform.position = new Vector3(camPos.x, cursor.transform.position.y, camPos.z);

    //         var camDir = Camera.main.transform.forward;
    //         camDir.y = 0;
    //         obj.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
    //         recognizer.StopCapturingGestures();
    //         obj.SetActive(true);
    //     }
    //     gameObject.SetActive(false);
    // }

    // Update is called once per frame
    void Update()
    {
        // Need to find every frame (I think), otherwise we might get an old object
        var cursor = FindObjectOfType<AnimatedCursor>();
        if(placeObj)
        {
            if (Vector3.Distance(Camera.main.transform.position, cursor.transform.position) <= 3)
            {
                placeObj.SetActive(true);
                placeObj.transform.position = cursor.transform.position;
                placeObj.transform.rotation = Quaternion.LookRotation(Vector3.forward, Vector3.up);
            }
            else
            {
                placeObj.SetActive(false);
            }
        }


        if (SetFloorEditor)
        {
            SetFloorEditor = false;
            if (!cursor) return;

            var camPos = Camera.main.transform.position;
            obj.transform.position = new Vector3(camPos.x, cursor.transform.position.y, camPos.z);

            var camDir = Camera.main.transform.forward;
            camDir.y = 0;
            obj.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
            //recognizer.StopCapturingGestures();
            obj.SetActive(true);
            gameObject.SetActive(false);
        }
    }
}

