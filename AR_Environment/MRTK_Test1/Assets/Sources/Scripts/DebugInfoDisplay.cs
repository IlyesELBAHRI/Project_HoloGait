using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;


public class DebugInfoDisplay : MonoBehaviour
{
    public GameObject contentBackPlate;
    private string previousLogMessage = "";
    private int previousLogMessageCount = 1;
    private TMP_Text textMeshPro;
    private int logMessageCount = 0;

    private void Start()
    {
        textMeshPro = contentBackPlate.GetComponentInChildren<TMP_Text>(); // Get the TextMeshPro component of the child object of ContentBackPlate.

        if (textMeshPro == null)
        {
            Debug.LogError("TextMeshPro component not found in ContentBackPlate.");
        }

        Application.logMessageReceived += HandleLogMessage; // Subscribe to the log message event.
    }

    private void OnDestroy()
    {
        Application.logMessageReceived -= HandleLogMessage; // Unsubscribe from the log message event.
    }

    private void HandleLogMessage(string logString, string stackTrace, LogType type)
    {
        if (textMeshPro != null)
        {
            string logMessage = logString;

            if (type == LogType.Error || type == LogType.Exception) // If the log type is an error or exception, color the message red.
            {
                logMessage = "<color=red>" + logMessage + "</color>";
            }
            else if (type == LogType.Warning) // If the log type is a warning, color the message yellow.
            {
                logMessage = "<color=yellow>" + logMessage + "</color>";
            }
            if (previousLogMessage == logMessage){ // If the log message is the same as the previous log message, increment the count.
                previousLogMessageCount++;
                textMeshPro.text +="[" + System.DateTime.Now.ToString("HH:mm:ss") + "] "+ logMessage + " (" +  previousLogMessageCount + ")" + "\n";
            }
            else{ // If the log message is different from the previous log message, reset the count.
                previousLogMessageCount = 1;
                textMeshPro.text +="[" + System.DateTime.Now.ToString("HH:mm:ss") + "] "+  logMessage + " (" +  previousLogMessageCount + ")" + "\n";
            }
            logMessageCount++;
            if (logMessageCount > 21)
            {
                textMeshPro.text = "[" + System.DateTime.Now.ToString("HH:mm:ss") + "] "+ logMessage + " (" +  previousLogMessageCount + ")" + "\n";
                logMessageCount = 1;
            }
            previousLogMessage = logMessage;
        }
    }
}

