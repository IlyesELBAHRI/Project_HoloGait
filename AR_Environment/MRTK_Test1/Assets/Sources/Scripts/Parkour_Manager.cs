using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Parkour_Manager : MonoBehaviour
{
    [SerializeField]
    private GameObject parkour1;
    [SerializeField]
    private GameObject parkour2;
    [SerializeField]
    private GameObject stopParkour;
    [SerializeField]
    private GameObject trigger;
    [SerializeField]
    private GameObject path1;
    [SerializeField]
    private GameObject path2;

    public enum ObstacleState { Parkour_1,Parkour_2,Stop,} // Enum to define the state of the obstacle.
    public static Parkour_Manager Instance; // Singleton instance of the class.
    public ObstacleState currentObstacleState; // Current state of the obstacle.

    void Awake()
    {
        Instance = this;
    }

    // Start is called before the first frame update
    void Start()
    {
        currentObstacleState = ObstacleState.Parkour_1;
        EyeTrackingManager.Instance.ResetCues();
        parkour2.SetActive(false);
        stopParkour.SetActive(false);
        path1.SetActive(false);
        path2.SetActive(false);

    }

    // Update is called once per frame
    void Update()
    {
        // Input keyboard are for debug
        if (Input.GetKeyDown(KeyCode.RightShift) || EyeTrackingManager.Instance.command == "RESTART") // If the command is RESTART, restart the scene.
        {
            EyeTrackingManager.Instance.command = "";
            Debug.Log("Restart");
            UDPClientServer.Instance.udpClose();
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }
        if (EyeTrackingManager.Instance.command == "CUES" || Input.GetKeyDown("o")){ // If the command is CUES, show the path.
            EyeTrackingManager.Instance.command = "";
            showPath();
        }//currentObstacleState != ObstacleState.Stop  &&
        if ( EyeTrackingManager.Instance.command == "PARKOUR"){ // If the command is PARKOUR, change the obstacle.
            EyeTrackingManager.Instance.command = "";
            changeObstacle();
        }
        if (EyeTrackingManager.Instance.command == "STOP"){ // If the command is STOP, stop everything.
            EyeTrackingManager.Instance.command = "";
            EyeTrackingManager.Instance.ResetCues();
            currentObstacleState = ObstacleState.Stop;
            parkour1.SetActive(false);
            parkour2.SetActive(false);
            stopParkour.SetActive(true);
            trigger.SetActive(false);
        }

    }
    // Function to change the obstacle depending on the current state.
    public void changeObstacle(){ 
        if (currentObstacleState == ObstacleState.Parkour_1){
            EyeTrackingManager.Instance.ResetCues();
            currentObstacleState = ObstacleState.Parkour_2;
            parkour1.SetActive(false);
            parkour2.SetActive(true);
        }
        else if (currentObstacleState == ObstacleState.Parkour_2){
            EyeTrackingManager.Instance.ResetCues();
            currentObstacleState = ObstacleState.Stop;
            parkour2.SetActive(false);
            parkour1.SetActive(false);
            stopParkour.SetActive(true);
            trigger.SetActive(false);
        }
        else if (currentObstacleState == ObstacleState.Stop){
            EyeTrackingManager.Instance.ResetCues();
            currentObstacleState = ObstacleState.Parkour_1;
            parkour1.SetActive(true);
            parkour2.SetActive(false);
            stopParkour.SetActive(false);
            trigger.SetActive(true);
        }

    }
    // Function to show the path depending on the current state of the course.
    private void showPath(){
        if (currentObstacleState == ObstacleState.Parkour_1){

            if (path1.activeInHierarchy){
                path1.SetActive(false);
            }
            else{
                path1.SetActive(true);
            }
            path2.SetActive(false);
        }
        else if (currentObstacleState == ObstacleState.Parkour_2){
            if (path2.activeInHierarchy){
                path2.SetActive(false);
            }
            else{
                path2.SetActive(true);
            }
            path1.SetActive(false);
        }
    }
    // Unused function to fade in the obstacle
    private IEnumerator FadeInObstacle(GameObject obstacle) 
    {
        foreach (MeshRenderer renderer in obstacle.GetComponentsInChildren<MeshRenderer>())
        {
            FadeInElement fadeInElement = renderer.gameObject.AddComponent<FadeInElement>();
            yield return new WaitForSeconds(0.5f); 
        }
        obstacle.SetActive(true);
    }



}
