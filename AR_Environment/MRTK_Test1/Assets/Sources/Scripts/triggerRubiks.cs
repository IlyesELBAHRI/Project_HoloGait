using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class triggerRubiks : MonoBehaviour
{
    public static triggerRubiks Instance;
    public bool isTriggered = false;
    public bool started = false;

    void Awake()
    {
        Instance = this;
    }
    void OnTriggerEnter(Collider other)
    { 
        if (other.gameObject.tag == "rubikscube"){
            isTriggered = true;
            started = true;
        }
        else if (other.gameObject.tag == "hammer" || other.gameObject.tag == "hotdog"){
            isTriggered = false;
            started = true;
        }
        
    }
    void OnTriggerExit(Collider other)
    {
        Debug.Log("exit");
        Debug.Log(other.gameObject.tag);
        if (other.gameObject.tag == "rubikscube"){
            isTriggered = false;
        }
    }
}
