using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowMovement_1 : MonoBehaviour
{
    public float speed = 1f;
    public float distance = 0.05f; 

    private float initialX;
    private float initialZ;

    void Start(){
        // initialX = transform.localPosition.x;
        initialZ = transform.localPosition.z;
    }

    void Update()
    {
        float displacement = distance * Mathf.Sin(Time.time * speed);
        // transform.localPosition = new Vector3(initialX + displacement, transform.localPosition.y, transform.localPosition.z);
        transform.localPosition = new Vector3(transform.localPosition.x, transform.localPosition.y, initialZ + displacement);
    }
}
