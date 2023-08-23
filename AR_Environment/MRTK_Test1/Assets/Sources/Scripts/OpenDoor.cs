using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OpenDoor : MonoBehaviour
{
    [SerializeField]
    private Transform doorTransform;
    [SerializeField]
    private GameObject button;
    public float targetRotationY = 120.0f; 
    public float rotationSpeed = 5.0f; 
    public bool buttonPressed = false;

    private Quaternion initialRotation;

    void Start()
    {
        initialRotation = doorTransform.rotation; // Initial rotation of the door
    }

    void Update()
    {
        if ( EyeTrackingManager.Instance.command == "DOOR"){ // If the command is DOOR, set the buttonPressed to true.
            EyeTrackingManager.Instance.command = "";
            buttonPressed = true;
        }
        if (buttonPressed){ // If the button is pressed, open the door.
            buttonPressed = false;
            StartCoroutine(OpenTheDoorCoroutine()); // Coroutine to open the door.
        }
    }

    IEnumerator OpenTheDoorCoroutine() // Coroutine to open the door.
    {
        float elapsedTime = 0.0f;
        Quaternion targetRotation = Quaternion.Euler(0.0f, targetRotationY, 0.0f); // Rotation target

        while (elapsedTime < rotationSpeed) // While the elapsed time is less than the rotation speed, rotate the door.
        {
            // Rotate the door 
            doorTransform.rotation = Quaternion.Slerp(initialRotation, targetRotation, elapsedTime / rotationSpeed);

            elapsedTime += Time.deltaTime;
            yield return null;
        }

        // Desactivate the door
        // doorTransform.gameObject.SetActive(false);

        // Desactivate the button
        button.SetActive(false);
    }

    public void ButtonPressed()
    {
        buttonPressed = true;
    }
}
