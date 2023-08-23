using UnityEngine;

public class ObjectPlacer : MonoBehaviour
{
    [SerializeField]
    private GameObject objectToPlace;

    public void PlaceObject(Vector3 location)
    {
        Debug.Log("Placing object");
        Debug.Log("Location : " + location);
        EyeTrackingManager.Instance.maxHeight = location.y;
        Vector3 cameraForward = Camera.main.transform.forward;
        var obj = Instantiate(objectToPlace, gameObject.transform);
        Collider colliderComponent = obj.GetComponent<Collider>(); 
        if (colliderComponent != null)
        {
            Debug.Log("Collider found");
            Vector3 objectHeight = colliderComponent.bounds.size;
            Debug.Log("Object height : " + objectHeight);
            // location += Vector3.up * (objectHeight.y / 2f);
            // Verify the direction of the camera in the Z axis
            float cameraDirection = Vector3.Dot(cameraForward, Vector3.forward);
            // if (cameraDirection < 0f){
            //     location -= Vector3.forward * (objectHeight.z / 2f);
            // }
            // else{
            //     location += Vector3.forward * (objectHeight.z / 2f);
            // }

            // Debug.Log("Location adjusted : " + location);
            obj.transform.position = location;
        }
        else{
            Debug.Log("No collider found");
            obj.transform.position = location;
        }
        
        cameraForward.y = 0f;
        Quaternion targetRotation = Quaternion.LookRotation(cameraForward, Vector3.up);
        obj.transform.rotation = targetRotation;
    }
}
