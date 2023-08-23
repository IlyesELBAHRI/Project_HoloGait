using Microsoft.MixedReality.OpenXR;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Input;
using Microsoft.MixedReality.Toolkit.SpatialAwareness;
using Microsoft.MixedReality.Toolkit.Teleport;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.WSA.Input;

public class sceneSetup : MonoBehaviour
{
    public GameObject obstacle1;
    public GameObject obstacle2;
    public GameObject obstacle3;
    public GameObject stuff;
    public GameObject floorObject; 
    //[SerializeField]
    //private GameObject Camera;
    [SerializeField]
    private float launchTime = 5.0f;
    private bool isFloorSet = false;
    private bool isSceneSet = false;
    private bool setupFinished = false;
    
    // Start is called before the first frame update
    void Start()
    {   
        floorObject.SetActive(false);
        DeactivateAllChildren(obstacle1);
        DeactivateAllChildren(obstacle2);
        DeactivateAllChildren(obstacle3);
        DeactivateAllChildren(stuff);
        //StartCoroutine(LaunchFloorSetup());
    }

    // Update is called once per frame
    void Update()
    {
        //// for debugging purposes /////
        if (Input.GetKeyUp("r")){
            Debug.Log("Reset");
        }
        if (Input.GetKeyUp("f") && !setupFinished){
            GetFloorPosition();
        }
        ////////////////////////////////
        if (isFloorSet && !isSceneSet){
            // Vector3 parkourPosition = parkour.transform.position;
            // Debug.Log("Parkour position before adjustment : " + parkourPosition);
            //parkourPosition.y = floorObject.transform.position.y;
            // parkour.transform.position = new Vector3(floorObject.transform.position.x, parkour.transform.position.y, floorObject.transform.position.z);
            // parkour.transform.rotation = floorObject.transform.rotation;
            isSceneSet = true;
            isFloorSet = false;
            // parkour.transform.position = new Vector3(floorObject.transform.position.x,floorObject.transform.position.y,floorObject.transform.position.z);
            // Debug.Log("Parkour position after adjustment : " + parkour.transform.position);

        }
        if (isSceneSet){
            isSceneSet = false;
            setupFinished = true;

            // Get the first Mesh Observer available, generally we have only one registered
            var observer = CoreServices.GetSpatialAwarenessSystemDataProvider<IMixedRealitySpatialAwarenessMeshObserver>();
            // Set to not visible
            observer.DisplayOption = SpatialAwarenessMeshDisplayOptions.None;
            Debug.Log("Mesh Observer Display Option : " + observer.DisplayOption);

            Parkour_Manager.Instance.changeObstacle();
        }
            
    }
    private void DeactivateAllChildren(GameObject parent){
        for (int i = 0; i < parent.transform.childCount; i++){
            parent.transform.GetChild(i).gameObject.SetActive(false);
        }
        parent.SetActive(false);
    }
    private void ActivateAllChildren(GameObject parent){
        parent.SetActive(true);
        for (int i = 0; i < parent.transform.childCount; i++){
            parent.transform.GetChild(i).gameObject.SetActive(true);
        }
    }
    public void SetUpCoroutine(){
        StartCoroutine(LaunchFloorSetup());
    }   
    private IEnumerator LaunchFloorSetup(){
        yield return new WaitForSeconds(launchTime);
        GetFloorPosition();
    }
    public void GetFloorPosition(){

        var cursor = FindObjectOfType<AnimatedCursor>();

        // if (cursor){
        //     // create a cube to show where the cursor is (<--- this is for debugging purposes)
        //     var cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
        //     cube.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        //     cube.transform.position = cursor.transform.position;
        //     cube.transform.rotation = cursor.transform.rotation;
        //     cube.GetComponent<MeshRenderer>().material.color = Color.red;
        //     Debug.Log("Cube position: " + cube.transform.position);
        //     Debug.Log("Cursor position: " + cursor.transform.position);
        // }

        if (cursor){
            Debug.Log("Cursor found");
            if (Vector3.Distance(Camera.main.transform.position, cursor.transform.position) <= 3)
            {
                var camPos = Camera.main.transform.position;
                // Position the floor object on the same plane as the cursor
                var floorPosition = new Vector3(camPos.x, cursor.transform.position.y, camPos.z);
                // Position the floor object at the same position as the cursor
                //var floorPosition = new Vector3(cursor.transform.position.x, cursor.transform.position.y, cursor.transform.position.z);
                floorObject.transform.position = floorPosition;
                Debug.Log("Floor position: " + floorObject.transform.position);
                obstacle1.transform.position = floorPosition;
                Debug.Log("Obstacle 1 position: " +obstacle1.transform.position);
                obstacle2.transform.position = floorPosition;
                Debug.Log("Obstacle 2 position: " +obstacle2.transform.position);
                obstacle3.transform.position = floorPosition;
                Debug.Log("Obstacle 3 position: " +obstacle3.transform.position);

                var stuffOffset = new Vector3(0, 0, 0.7f);
                stuff.transform.position = floorPosition - stuffOffset;
                Debug.Log("Stuff position: " +stuff.transform.position);


                var camDir = Camera.main.transform.forward;
                camDir.y = 0;
                floorObject.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
                obstacle1.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
                obstacle2.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
                obstacle3.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
                stuff.transform.rotation = Quaternion.LookRotation(camDir, Vector3.up);
                floorObject.SetActive(true);
                ActivateAllChildren(obstacle1);
                ActivateAllChildren(obstacle2);
                ActivateAllChildren(obstacle3);
                ActivateAllChildren(stuff);
                isFloorSet = true;
            }
        }
        //gameObject.SetActive(false);

        // RaycastHit hit;
        // // show raycast
        // Debug.DrawRay(Camera.main.transform.position, Vector3.down * 100, Color.red, 10);
        // if (Physics.Raycast(Camera.main.transform.position, Vector3.down, out hit, LayerMask.GetMask("Spatial Awareness"))){
        //     floorObject.transform.position = hit.point;
        //     floorObject.transform.rotation = Quaternion.FromToRotation(Vector3.up, hit.normal);

        //     Debug.Log("Floor position : " + hit.point);
        //     Debug.Log("Floor rotation : " + Quaternion.FromToRotation(Vector3.up, hit.normal));
            
        //     Renderer renderer = hit.collider.GetComponent<Renderer>();
        //     MeshFilter meshFilter = hit.collider.GetComponent<MeshFilter>();
        //     MeshCollider meshCollider = hit.collider.GetComponent<MeshCollider>();

        //     // Debug
        //     if (renderer != null)
        //     {
        //         Debug.Log("Object name: " + renderer.gameObject.name);
        //         Debug.Log("Object material: " + renderer.sharedMaterial.name);
        //     }

        //     if (meshFilter != null)
        //     {
        //         Debug.Log("Object mesh vertices count: " + meshFilter.sharedMesh.vertexCount);
        //         Debug.Log("Object mesh triangles count: " + meshFilter.sharedMesh.triangles.Length / 3);
        //     }

        //     if (meshCollider != null)
        //     {
        //         Debug.Log("Object mesh collider enabled: " + meshCollider.enabled);
        //     }
        //     isFloorSet = true;
        // }
        
    }
}
