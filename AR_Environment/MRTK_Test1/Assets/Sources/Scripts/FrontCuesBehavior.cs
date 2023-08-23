using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FrontCuesBehavior : MonoBehaviour
{
    [SerializeField]
    private List<GameObject> frontCues;
    private Vector3 initialPosition;
    public float max_distance = 0.6f;

    void Start(){
        initialPosition = Camera.main.transform.position;
        StartCoroutine(ShowFrontCues());   
    }

    void Update(){
        // If the distance between the camera and the initial position is greater than the max distance, deactivate the object.
        float distance = Vector3.Distance(Camera.main.transform.position, initialPosition);
        if (distance > max_distance){
            foreach(GameObject cue in frontCues){
                cue.SetActive(false);
            }
            this.gameObject.SetActive(false);
            StopCoroutine(ShowFrontCues());
        }
    }
    IEnumerator ShowFrontCues(){ // Coroutine to show the front cues.

        foreach(GameObject cue in frontCues){
            cue.SetActive(true);
            yield return new WaitForSeconds(0.5f);
        }
        foreach(GameObject cue in frontCues){
            cue.SetActive(false);
        }
        StartCoroutine(ShowFrontCues());
    }


}
