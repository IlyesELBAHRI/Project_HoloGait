using System.Collections;
using System.Collections.Generic;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine;

public class EyeTrackingManager : MonoBehaviour
{
    /* Eye Tracking Data Array
       - 0 : Gaze Direction --> Direction of the gaze ray
       - 1 : Gaze Origin --> Origin of the gaze ray
       - 2 : Head Movement Direction --> Direction of the head movement
       - 3 : Head Velocity --> Velocity of the head movement
       - 4 : Hit Normal --> Normal of the object that is being looked at
       - 5 : Hit Position --> Position of the object that is being looked at if it exists, otherwise the last position 
       - 6 : Cursor Position --> Position of the cursor, at any time even if it is not on an object  (the best position to place the cues)
    */
    [SerializeField]
    private GameObject FootPrintCuesPrefab;
    [SerializeField]
    private GameObject RightFootPrintCuesPrefab;
    [SerializeField]
    private GameObject LeftFootPrintCuesPrefab;
    [SerializeField]
    private GameObject GreenStripeCuesPrefab;
    [SerializeField]
    private GameObject YellowStripeCuesPrefab;    
    [SerializeField]
    private GameObject StripesCuesPrefab;
    [SerializeField]
    private GameObject FrontCuesPrefab;
    private Vector3[] eyeTrackingData = new Vector3[7];
    private GameObject Target = null;
    private string TargetTag = null;
    private int typeOfCues = 1; // 1: foot print cues, 2: stripes
    public static EyeTrackingManager Instance;
    public float maxHeight = 0.5f;
    public float defaultDistanceInMeters = 3.0f;
    public string command = ""; // UDP command received from the python script
    public bool isFloorFound = false;
    
    private void Awake()
    {
        Instance = this;
    }

    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("Eye Tracking Manager Started");
        var eyeTrackingProvider = CoreServices.InputSystem?.EyeGazeProvider; // Get the eye tracking provider
        eyeTrackingProvider.IsEyeTrackingEnabled = true; // Enable eye tracking
    }

    // Update is called once per frame
    void Update()
    {
        var eyeTrackingProvider = CoreServices.InputSystem?.EyeGazeProvider; // Get the eye tracking provider

        if (Input.GetKeyDown(KeyCode.Backspace) || command == "MESH"){ // If the backspace key is pressed or the command "MESH" is received, toggle the spatial map
            command = "";
            Debug.Log("Spatial Map Toggled");
            SpatialMapToggler.Instance.ToggleSpatialMap();
        }
        if (command == "RESET"){ // If the command "RESET" is received, reset the cues
            command = "";
            Debug.Log("Cues Reset");
            ResetCues();
        }
        if (command == "TYPE" || Input.GetKeyDown("b")){ // If the command "TYPE" is received or the key "b" is pressed, toggle the type of cues
            command = "";
            if (typeOfCues == 1){
                typeOfCues = 2;
            }else{
                typeOfCues = 1;
            }
        }
        // If the command "FOG" is received or the return key is pressed and the eye tracking data is valid, place the cues
        if (( eyeTrackingProvider.IsEyeTrackingDataValid && Input.GetKeyDown(KeyCode.Return)) || command == "FOG"){
            command = "";
            Debug.Log("Eye Tracking Data Valid");
            //CoreServices.InputSystem?.EyeGazeProvider?.GazeCursorPrefab.transform.gameObject.SetActive(true);    
            getTargetInfo();
            getEyeTrackingData();
            Debug.Log("Target Name: " + Target.name);
            placeCues();
        }

    }
    // Function to reset the cues //
    public void ResetCues(){ 
        GameObject[] cues = GameObject.FindGameObjectsWithTag("FootPrintCues"); // Find all the foot print cues in the scene
        Debug.Log("Number of cues: " + cues.Length);
        if (cues.Length == 0){ // If there are no cues,
            return; // Do nothing
        }else{
            foreach (GameObject cue in cues){ // Otherwise, destroy all the cues
                Destroy(cue);
            }
        }
    }
    // Function to place the cues //
    public void placeCues(){
        ResetCues();
        Vector3 startPosition; 
        Vector3 targetPosition;
        Vector3 cameraForward = Camera.main.transform.forward;
        cameraForward.y = 0f;
        Quaternion targetRotation = Quaternion.LookRotation(cameraForward, Vector3.up);

        var cuesIndicator = Instantiate(FrontCuesPrefab); // Instantiate the front cues
        Vector3 offset = Camera.main.transform.forward * 1.0f; // Distance between the camera and the cues
        Vector3 positionFront = Camera.main.transform.position + offset; 
        cuesIndicator.transform.position = positionFront;
        cuesIndicator.transform.rotation = targetRotation;

        if (typeOfCues == 1){ // If the type of cues is foot print cues,
            if (TargetTag == "Parkour" || isFloorFound){ // If the target is a parkour object or the floor is found,
                startPosition = new Vector3(eyeTrackingData[1].x, maxHeight + 0.01f, eyeTrackingData[1].z + 0.4f);
                targetPosition = new Vector3(eyeTrackingData[6].x, maxHeight + 0.01f, eyeTrackingData[6].z);
            }else{
                startPosition = new Vector3(eyeTrackingData[1].x, eyeTrackingData[6].y + 0.05f, eyeTrackingData[1].z + 0.4f);
                targetPosition = new Vector3(eyeTrackingData[6].x, eyeTrackingData[6].y + 0.05f, eyeTrackingData[6].z);
            }                
            float distance = Vector3.Distance(startPosition, targetPosition);

            // Calculate the number of steps based on the distance and step size
            int numSteps = Mathf.CeilToInt(distance / 0.2f);

            // Calculate the direction from start to target position
            Vector3 direction = (targetPosition - startPosition).normalized;

            // Instantiate the foot print cues
            for (int i = 0; i < numSteps; i++)
            {
                // Determine if it's a left or right foot print
                GameObject footPrint = (i % 2 == 0) ? LeftFootPrintCuesPrefab : RightFootPrintCuesPrefab;

                // Calculate the position along the path
                float t = (float)i / (numSteps - 1); // Normalized distance between 0 and 1
                Vector3 position = Vector3.Lerp(startPosition, targetPosition, t);

                // Calculate the side offset based on the step number
                float sideOffset = (i % 2 == 0) ? -0.1f : 0.1f;

                // Calculate the forward offset
                float forwardOffset = 0.1f * i;

                // Apply the offsets to the position
                position += targetRotation * new Vector3(sideOffset, 0f, forwardOffset);

                // Instantiate the foot print cue at the calculated position
                var footPrintCue = Instantiate(footPrint);
                footPrintCue.transform.localScale = new Vector3(2.0f, 2.0f, 2.0f);
                footPrintCue.transform.position = position;
                footPrintCue.transform.rotation = targetRotation;
            }
            // Calculate the position above the last footprint
            Vector3 aboveFootPrintPosition = positionFront + direction * 0.2f;

            // Set the position of cuesIndicator to above the last footprint
            cuesIndicator.transform.position = aboveFootPrintPosition;
            cuesIndicator.transform.rotation = targetRotation;
        }
        else if (typeOfCues == 2){ // If the type of cues is stripes,
            if (TargetTag == "Parkour" || isFloorFound){
                startPosition = new Vector3(eyeTrackingData[1].x, maxHeight + 0.01f, eyeTrackingData[1].z + 0.4f);
                targetPosition = new Vector3(eyeTrackingData[6].x, maxHeight + 0.01f, eyeTrackingData[6].z);
            }else{
                startPosition = new Vector3(eyeTrackingData[1].x, eyeTrackingData[6].y + 0.05f, eyeTrackingData[1].z + 0.4f);
                targetPosition = new Vector3(eyeTrackingData[6].x, eyeTrackingData[6].y + 0.05f, eyeTrackingData[6].z);
            } 
            float distance = Vector3.Distance(startPosition, targetPosition);

            // Calculate the number of stripes based on the distance and stripe size
            int numStripes = Mathf.CeilToInt(distance / 0.15f);

            // Calculate the direction from start to target position
            Vector3 direction = (targetPosition - startPosition).normalized;

            // Instantiate the stripe cues
            for (int i = 0; i < numStripes; i++)
            {
                GameObject stripe = (i % 2 == 0) ? GreenStripeCuesPrefab : YellowStripeCuesPrefab;

                // Calculate the position along the path
                float t = (float)i / (numStripes - 1); // Normalized distance between 0 and 1
                Vector3 position = Vector3.Lerp(startPosition, targetPosition, t);

                // Calculate the forward offset
                float forwardOffset = 0.1f * i;

                // Apply the offset to the position
                position += targetRotation * new Vector3(0f, 0f, forwardOffset);

                // Instantiate the stripe cue at the calculated position
                var stripeCue = Instantiate(stripe);
                stripeCue.transform.localScale = new Vector3(2.0f, 2.0f, 2.0f);
                stripeCue.transform.position = position;
                stripeCue.transform.rotation = targetRotation;
            }

            // Calculate the position above the last stripe
            Vector3 aboveStripePosition = positionFront + direction * 0.2f;

            // Set the position of cuesIndicator to above the last stripe
            cuesIndicator.transform.position = aboveStripePosition;
            cuesIndicator.transform.rotation = targetRotation;
        }

    }
    // Function to get the eye tracking data //
    public Vector3[] getEyeTrackingData(){
        var eyeTrackingProvider = CoreServices.InputSystem?.EyeGazeProvider;
    
        eyeTrackingData[0] = eyeTrackingProvider.GazeDirection;
        eyeTrackingData[1] = eyeTrackingProvider.GazeOrigin;
        eyeTrackingData[2] = eyeTrackingProvider.HeadMovementDirection;
        eyeTrackingData[3] = eyeTrackingProvider.HeadVelocity;
        eyeTrackingData[4] = eyeTrackingProvider.HitNormal;
        eyeTrackingData[5] = eyeTrackingProvider.HitPosition;
        eyeTrackingData[6] = eyeTrackingProvider.GazeCursor.Position;
        var writeData = eyeTrackingData; // Write the eye tracking data to a variable
        return writeData; // Return the eye tracking data
    }
    // Function to get the target info //
    public GameObject getTargetInfo(){ 
        var eyeTrackingProvider = CoreServices.InputSystem?.EyeGazeProvider;
        Target = eyeTrackingProvider.HitInfo.transform.gameObject;
        TargetTag = Target.tag;
        Debug.Log("Target Tag: " + TargetTag);
        var writeData = Target;
        return writeData;
    }
}
