using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class triggerHammer : MonoBehaviour
{
    public static triggerHammer Instance;
    public bool isTriggered = false;
    public bool started = false;

    void Awake()
    {
        Instance = this;
    }
    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "hammer"){
            isTriggered = true;
            started = true;
        }
        else if (other.gameObject.tag == "rubikscube" || other.gameObject.tag == "hotdog"){
            isTriggered = false;
            started = true;
        }
    }
    void OnTriggerExit(Collider other)
    {
        if (other.gameObject.tag == "hammer"){
            isTriggered = false;
        }
    }
}
