using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class obstacle6manager : MonoBehaviour
{
    public TMP_Text textMeshPro;
    private int count = 0;
    
    // Update is called once per frame
    void Update(){
        if (isStarted()){
            checkColliders();
        }
    }
    // Check if the colliders are triggered and how many are triggered. If all are triggered, change the obstacle.
    private void checkColliders(){
        count = 0;
        if (triggerHammer.Instance.isTriggered){
            count++;
        }
        if (triggerHotDog.Instance.isTriggered){
            count++;
        }
        if (triggerRubiks.Instance.isTriggered){
            count++;
        }
        textMeshPro.text = "Result: " + count + "/3";
        if (count == 3){
            Parkour_Manager.Instance.changeObstacle();
            textMeshPro.text = "Please put items in the right place";
            count = 0;
        }
    }
    private bool isStarted(){
        if (triggerHammer.Instance.started || triggerHotDog.Instance.started || triggerRubiks.Instance.started){
            return true;
        }
        else{
            return false;
        }

    }

}
