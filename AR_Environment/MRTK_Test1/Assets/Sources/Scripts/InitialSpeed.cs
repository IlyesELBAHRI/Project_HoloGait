using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InitialSpeed : MonoBehaviour
{

    [SerializeField]
    private Vector3 initialSpeed;
    // Start is called before the first frame update
    void Start()
    {
        var rigidbody = GetComponent<Rigidbody>();
        rigidbody.velocity = initialSpeed;
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
