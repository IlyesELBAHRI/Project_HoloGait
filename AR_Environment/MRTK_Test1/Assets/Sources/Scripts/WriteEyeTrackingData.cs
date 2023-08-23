using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using Microsoft.MixedReality.Toolkit;
using UnityEngine;

public class WriteEyeTrackingData : MonoBehaviour
{
    private StreamWriter trackerData;
    private double previousValue = -1.0f;

    private void Awake()
    {
        string timestamp = DateTime.Now.ToString("dd_MM_yyyy_HH_mm_ss"); // Get the current date and time to name the file.
        //string timestamp = CoreServices.InputSystem?.EyeGazeProvider.Timestamp.ToString().Split(' ')[0].Replace("/", "_");
        string filename =  timestamp + "_eyeTrackingData.csv"; // Name of the file
        var DataPath = Path.Combine(Application.persistentDataPath, filename); 
        trackerData = new StreamWriter(DataPath); // this is the path for the hololens
        //trackerData = new StreamWriter("Assets/Sources/Data/" + filename); // this is the path for the unity editor
        trackerData.AutoFlush = true; // Auto flush the data
        string columnTitles = "Time,Gaze_Direction.x,Gaze_Direction.y,Gaze_Direction.z,Gaze_Origin.x,Gaze_Origin.y,Gaze_Origin.z,Head_Movement_Direction.x,Head_Movement_Direction.y,Head_Movement_Direction.z,Head_Velocity.x,Head_Velocity.y,Head_Velocity.z,Hit_Normal.x,Hit_Normal.y,Hit_Normal.z,Hit_Position.x,Hit_Position.y,Hit_Position.z,Cursor_Position.x,Cursor_Position.y,Cursor_Position.z";
        trackerData.WriteLine(columnTitles);
    }
    private void OnDestroy()
    {
        trackerData.Close();
    }
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        // every 0.01 seconds, write the data in the file
        if (Math.Round(Time.time,2) != previousValue){
            previousValue = Math.Round(Time.time,2);
            WriteData();
        }
    }
    private void WriteData(){
        var eyeTrackingData = EyeTrackingManager.Instance.getEyeTrackingData(); // Get the eye tracking data from the EyeTrackingManager.
        //Debug.Log("Time :" + Math.Round(Time.time,2) );
        // Convert the data to string and write it in the file.
        string time = Time.time.ToString("0.##", CultureInfo.InvariantCulture); 
        string gazeDirection = FormatVector3(eyeTrackingData[0]);
        string gazeOrigin = FormatVector3(eyeTrackingData[1]);
        string headMovementDirection = FormatVector3(eyeTrackingData[2]);
        string headVelocity = FormatVector3(eyeTrackingData[3]);
        string hitNormal = FormatVector3(eyeTrackingData[4]);
        string hitPosition = FormatVector3(eyeTrackingData[5]);
        string cursorPosition = FormatVector3(eyeTrackingData[6]);

        string line = $"{time},{gazeDirection},{gazeOrigin},{headMovementDirection},{headVelocity},{hitNormal},{hitPosition},{cursorPosition}";
        trackerData.WriteLine(line);
    }
    private string FormatVector3(Vector3 vector){
        return FormattableString.Invariant($"{vector.x},{vector.y},{vector.z}");
    }
}
