using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class triggerCourse : MonoBehaviour
{
    [SerializeField]
    private GameObject hologram;
    [SerializeField]
    private GameObject indicator;
    [SerializeField]
    private GameObject text1;
    [SerializeField]
    private GameObject text2;
    private bool isTriggered = false;
    void Start()
    {
        text2.SetActive(false);
    }
    void Update()
    {
        if (isTriggered){ // If the trigger is activated, change the parkour.
            isTriggered = false;
            Parkour_Manager.Instance.changeObstacle();
        }
        if (Parkour_Manager.Instance.currentObstacleState == Parkour_Manager.ObstacleState.Parkour_2 && !isTriggered){ // If the current obstacle is the second parkour, desactivate the hologram.
            hologram.GetComponent<MeshRenderer>().enabled = false;
            indicator.SetActive(false);
            text1.SetActive(false);
            
        }

    }
    // Function to check if the player is in the trigger.
    void OnTriggerEnter(Collider other) 
    {
        if (other.gameObject.tag == "Player") // If the player is in the trigger, change the parkour and desactivate the hologram.
        {
            if (Parkour_Manager.Instance != null && Parkour_Manager.Instance.currentObstacleState == Parkour_Manager.ObstacleState.Parkour_1){
                // desactivate mesh renderer of the hologram
                hologram.GetComponent<MeshRenderer>().enabled = false;
                indicator.SetActive(false);
                text1.SetActive(false);
                text2.SetActive(true);
                isTriggered = true;
            }
        }
    }
}
