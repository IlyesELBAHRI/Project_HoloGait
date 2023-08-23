using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FloorCuesBehavior : MonoBehaviour
{
    private Vector3 initialPosition;
    public float max_distance = 1.0f;

    void Start(){
        initialPosition = Camera.main.transform.position;  
    }

    void Update(){

        float distance = Vector3.Distance(Camera.main.transform.position, initialPosition);
        if (distance > max_distance){ // If the distance between the camera and the initial position is greater than the max distance, deactivate the object.
            this.gameObject.SetActive(false);
        }
    }

}
