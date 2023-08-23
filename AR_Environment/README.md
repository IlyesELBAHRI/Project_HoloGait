# HoloGait-Project

Welcome to the HoloGait-Project! This project aims to improve the quality of life for individuals with Parkinson's disease by utilizing augmented reality (AR) and innovative technologies. By addressing the freezing of gait (FoG) phenomenon, HoloGait offers a personalized and adaptive solution to help patients overcome mobility challenges.

# Table of contents

1. [Introduction](#introduction)
2. [How to Use the HoloGait Unity Project](#how-to-use-the-hologait-unity-project)
3. [Hololens' App](#hololens-app)
4. [UDP Communication with HoloLens - Interface](#udp-communication-with-hololens---interface)
5. [Application Overview](#application-overview)
    1. [Getting Started](#getting-started)
    2. [Setting Up the Course](#setting-up-the-course)
    3. [Disabling Spatial Mesh](#disabling-spatial-mesh)
    4. [Course Obstacles](#course-obstacles)
    5. [Supervisor Commands](#supervisor-commands)
    6. [Course Behavior Control](#course-behavior-control)
    7. [UDP Communication](#udp-communication)
    8. [Eye-Tracking Data Logging](#eye-tracking-data-logging)
6. [Replay HoloGait App](#replay-hologait-app)
    1. [Implementation Details](#implementation-details)
    2. [Future Improvements](#future-improvements)
7. [Limitations and Improvements](#limitations-and-improvements)
8. [Conclusion](#conclusion)
9. [Acknowledgments](#acknowledgments)
10. [Contact Information](#contact-information)
11. [Important Links - Documentation, Tutorials, and References](#important-links---documentation-tutorials-and-references)
    1. [Unity Documentation (for specific issues and questions)](#unity-documentation)
    2. [Joost Van Schaik's website](#joost-van-schaiks-website)
    3. [Microsoft Documentation](#microsoft-documentation)
    4. [Other Documentation](#other-documentation)
    5. [Some videos that helped me](#some-videos-that-helped-me)



## Introduction
The HoloGait project incorporates several key features to enhance the management of FoG:

- **Augmented Reality (AR) Environment:** Using the HoloLens AR headset and the Mixed Reality Toolkit 2 (MRTK2), HoloGait creates immersive and simulated environments to guide patients during their movements. Real-time visual cues are displayed to provide assistance and overcome FoG episodes.

- **Eye Tracking:** HoloGait leverages eye tracking technology to track the patient's gaze. By analyzing the eye movement, visual cues are triggered to provide real-time guidance and support.

- **UDP Command Controls:** The HoloLens application can be controlled via UDP commands, offering dynamic interactions and customization options. This allows for activating visual cues when FoG is detected, adjusting the position of the virtual ground during setup, changing the type of visual cues, disabling the environment mesh, stopping the progression, displaying pre-implemented arrow paths, and resetting visual cues in the scene.

- **Haptic Feedback System:** The HoloGait project includes a haptic feedback system that provides additional sensory cues to aid patients in overcoming FoG episodes.

Please note that this specific project focuses on the development of the AR environment using the Mixed Reality Toolkit 2 (MRTK2), including the trigger of FoG, visual cues, eye tracking integration, and related functionalities. The haptic feedback system and FoG detection aspects are part of a separate project within the HoloGait initiative.

***All the codes provided are commented so you can refer to them for further details.***

***Every links you can refer to are in the "Important Links - Documentation, Tutorials, and References" section at the end of this README.***

## How to Use the HoloGait Unity Project
**Note**: Some assets used to create the course in the HoloGait project are not available in this repository. These assets, such as PolygonSciFi, PolygonTown, and PolygonOffice, are paid assets from the Unity Store. Therefore, if you want to use the same course, you may need to adapt the scene or import the assets from the Unity Store.

To get started with the HoloGait Unity project, follow these steps:

1. **Clone the Repository:** Clone the HoloGait project repository to your local machine. Be careful to initialize the github repository as git lfs to retrieve the files, as the project is too large and has been pushed via git lfs.
```bash
git lfs install
git pull origin main
```

2. **Open the Project in Unity:** Open Unity (version 2020.3.48) and either create a new UWP project based on the existing project or open the Unity project directly from the Unity Hub by selecting the correct folder where the repository was cloned. Cloning is recommended as the project is already set up. Ensure that you have the same version of Unity to avoid compatibility issues.

3. **Address Potential Issues:**

| Step | Description | Screenshot |
| --- | --- | --- |
| 1 | In the Build Settings, ensure you choose the correct scene to build, select the UWP platform, set the target device to HoloLens (architecture x64), and build in release mode. | ![Step 1](https://i.imgur.com/HSd2qZI.png) |
| 2 | In Project Settings, navigate to Mixed Reality Toolkit and ensure the necessary options are checked. | ![Step 2](https://i.imgur.com/SXZhaJN.png) |
| 3 | In Player Settings, customize the application and package names accordingly. The package name should match the application name. | ![Step 3](https://i.imgur.com/IBVjWXa.png) |
| 4 | In the Capabilities tab (also in Player Settings), ensure that all capabilities are checked. | ![Step 4](https://i.imgur.com/s04pqIF.png) |
| 5 | In XR Plugin Management, enable the settings. | ![Step 5](https://i.imgur.com/dTdAvkC.png) |
| 6 | In OpenXR, adjust the settings. | ![Step 6](https://i.imgur.com/qVS9A6J.png) |

You can also simply refer to the tutorials provided by Microsoft [Unity development for HoloLens](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/unity-development-overview?tabs=arr%2CD365%2Chl2).

4. **MRTK Configuration:** Follow the tutorial [MRTK](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/?view=mrtkunity-2022-05) for setting up the Mixed Reality Toolkit (MRTK). Specifically, run the "MixedRealityFeatureTool for Unity," click "Start", select the project path, and import any missing packages as indicated in the tutorial.

|   |   |
| --- | --- | 
| ![Step 1](https://i.imgur.com/8IszNde.png) | ![Step 2](https://i.imgur.com/EV0BRJH.png) |


5. **Spatial Awareness Configuration:** In the scene's GameObject that contains the MRTK configurations, go to the "Spatial Awareness" section and ensure that "SpatialObjectMeshObserver" is set up for Unity Editor debugging with the same configuration as shown in the image bellow. Make sure the desired room's mesh (scanned with HoloLens) by simply foolowing this tutorial [Using a Spatial Mesh inside the Unity Editor](https://localjoost.github.io/migrating-to-mrtk2-using-spatial-mesh/) or a pre-scanned mesh from the project's assets (located in "Sources/Mesh") is set as "Spatial Mesh Object." For "OpenXR Spatial Mesh Observer," have the same configuration as shown in the image bellow. For Unity Editor debugging, adapt the "Input" -> "Input Simulation Service" as needed to simulate Hololens inputs in the editor.

|   |   | |
| --- | --- | --- |
| ![Step 1](https://i.imgur.com/p5y2Ct7.png) | ![Step 2](https://i.imgur.com/7enW9JN.png) | ![Step 3](https://i.imgur.com/G1ZdH6K.png) |

6. **Customize the Course:** If you don't have access to the paid assets, create your own course using different assets or modify the existing course to fit your needs. 

| Obstacle | Description | Screenshot |
| --- | --- | --- |
| 1 | Obstacle by opening the door with a button | ![Obstacle 1](https://i.imgur.com/9LkRhg2.png) |
| 2 | A column to go around with a direction. | ![Obstacle 2](https://i.imgur.com/zWYjX12.png) |
| 3 | Obstacles in the form of bushes to step over | ![Obstacle 3](https://i.imgur.com/V4gkshy.png) |
| 4 | A narrow path that looks like a passageway over the water | ![Step 4](https://i.imgur.com/HVGrtdg.png) |
| 5 | A surface with a hole in the middle to go around | ![Obstacle 5](https://i.imgur.com/giurdkw.png) |
| 6 | A table with 3 objects to position in the right place | ![Obstacle 6](https://i.imgur.com/0yHuAEh.png) |


| Part of the course | Description | Screenshot |
|:---:|:---:|:---:|
| 1 | The first part of the course involves passing through the gate, then around the column, then over the obstacles, and finally to the trigger box for the 2nd course. | ![Obstacle 1](https://i.imgur.com/1h0B11w.png) |
| 2 | The second part of the course involves passing between the barriers to get to a path over the water, then a space with a false hole in the middle to go around, and finally the table with a rubiks cube, a hammer and a hot dog to be placed in the right spot in the form of a mini-game. Once you've passed the obstacle, the course is over. | ![Obstacle 2](https://i.imgur.com/VZt5Ofg.png) |
| 3 | Two platforms with a green hologram and an arrow inside are placed at either end of the course to show the patient where to go, in addition to the visual cues. *(It's important to note that these ends are adapted for the gait room in Cereneo's at G level).* | ![Obstacle 3](https://i.imgur.com/O4HiiFG.png) |
| 4 | An arrow path showing the patient where to go. This arrow path is fixed and not dynamic, unlike visual cues, and is mainly used to help the patient before he or she even has a FoG. This path can be displayed by sending the UDP command "CUES". | ![Obstacle 4](https://i.imgur.com/ISaTHCq.png) |

| Visual Cues | Description | Screenshot |
|:---:|:---:|:---:|
| 1 | Footprints visual cue, dynamically displayed with eye-tracking data to show the patient where to walk in FoG phases. | ![Cue 1](https://i.imgur.com/wFun9GO.png) |
| 2 | Stripes visual cue, in the same way as footprints, but provides another method of unlocking the patient during a FoG. | ![Cue 2](https://i.imgur.com/NDNRT1Y.png) |
| 3 | Front visual cue, displaying a downward-facing arrow which will be placed directly in front of the patient's gaze to show him where he should look at the visual cues on the ground in the event of a FoG looking straight ahead.| ![Cue 3](https://i.imgur.com/kizyjxu.png) |

Once the course is ready, place the prefab in the corresponding variable in the "HoloGramCollection" GameObject as shown in the image bellow.
<p align="center">
  <img src="https://i.imgur.com/KJ8RWkg.png" alt="HologramCollection">
</p>

7. **Build and Deploy the Application:** Once everything is in place, go to the Build Settings, click "Build," select the target folder, open the created solution, choose "Release" and "ARM64" configurations, enter the correct IP address of the target HoloLens device (ensure both the computer and HoloLens are on the same network), and then launch without debugging.

|   |   | |
| --- | --- | --- |
| ![Step 1](https://i.imgur.com/jlc60M7.png) | ![Step 2](https://i.imgur.com/qN4xiGi.png) | ![Step 3](https://i.imgur.com/ysrTftF.png) |

8. **First Launch and Permissions:** When you deploy and launch the application on the HoloLens, you may encounter permission dialogues. Please accept all permissions. After the first launch, close and relaunch the application to ensure proper calibration of eye tracking.

9. **Testing and Patient Interaction:** Now, you can test the application. For a real patient interaction, provide proper guidance during the setup phase, as it can be complex. Additionally, you can monitor the live view of what the patient sees on the "Microsoft Hololens" application while connected to the same network. Note that the live view may have occasional bugs, and you may need to restart the computer and HoloLens to resolve any issues. The live view allows monitoring and sending UDP commands effectively (refer to the corresponding section).

**Important**: This version of HoloGait is the initial release and has room for improvement (as seen in the "Limitations and Improvements" section). When testing with a patient, ensure you guide them through the setup phase. For more information and guidance on developing HoloLens applications, refer to the official Unity or Microsoft documentation or the website of Joost Van Schaik (https://localjoost.github.io/), which contains helpful articles for HoloLens application development.

Once you have successfully built and deployed the application, you are ready to use the HoloGait system with a patient. You can go to the "Application Overview" section for more details on the application itself. Enjoy the innovative and immersive experience it provides!


## Hololens App
The "Hololens_App" folder contains the application specifically designed to be deployed on the HoloLens device. To use the app, follow these steps:

1. **Download the Application ZIP:** Download the ZIP file containing the application from "AR_Environment/Hololens_App".

2. **Extract the Files:** Extract the contents of the ZIP file to a local directory of your choice.

3. **Connect HoloLens to Your Computer:** Ensure that your HoloLens device is connected to your computer and on the same Wi-Fi network.

4. **Access the Device Portal:** Open a web browser and navigate to the corresponding IP address of your HoloLens device (e.g., `http://192.168.1.100`) to access the HoloLens Device Portal.

5. **Deploy the Application:** In the Device Portal, navigate to the "Apps" section and select "Local Storage". Choose the file containing the application, and if necessary, any dependencies. Allow the application to be pushed to the HoloLens.

6. **First Launch and Eye Tracking Calibration:** Upon the first launch of the application on the HoloLens, you may need to authorize the necessary permissions/dialogues. After that, close the application and relaunch it, ensuring that eye tracking is properly calibrated.

7. **Test the Application:** Once the application is launched, you can test its functionality. Refer to the "Application Overview" section for detailed information on its features and usage.

Please ensure that your HoloLens device is properly configured and connected before proceeding with the application deployment.

For more detailed instructions on how to deploy an application on HoloLens, you can refer to the documentation [Using the Windows Device Portal](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/using-the-windows-device-portal).

![TutoDeployApp1](https://i.imgur.com/R7mZ4up.png)
![TutoDeployApp2](https://i.imgur.com/MOAaPha.png)


## UDP Communication with HoloLens - Interface
The HoloGait application communicates with the HoloLens device using UDP commands. To use the UDP communication feature, follow these steps:

1. **Retrieve the UDP Files:** Navigate to the "AR_Environment/UDP" folder and obtain the required files, including the Python script named "UDPclient.py".

2. **Modify UDP Parameters:** In the "UDPclient.py" script, you can adjust the UDP port by modifying the variable `hololens_port` (initialized to "8080") to match your preferred port number. Additionally, ensure that the IP addresses are correctly set for communication between the HoloLens device and your computer. You may need to modify the IP addresses for Unity Editor debugging or use a fixed IP address when deploying to the HoloLens with a router providing a static IP address.

3. **Run the Python Script:** Execute the "UDPclient.py" Python script to open the graphical user interface (GUI) created with TKinter. This GUI contains various buttons representing different features.

4. **UDP Command Controls:** The buttons in the GUI allow you to send UDP commands to the HoloLens application, enabling dynamic interactions and customizations. Here are the currently implemented commands:
   - "FOG": Toggle the display of visual cues based on eye tracking data, useful when the Fog detection by machine learning hasn't triggered the command.
   - "YES": Used during the setup phase to position the ground correctly at the patient's feet level.
   - "NO": Provide more time to find the correct ground placement.
   - "CUES": Display a path of arrows to guide the patient and prevent FoG.
   - "MESH": Disable the environment mesh in the HoloLens after the ground is placed correctly.
   - "STOP": Halt the progression and show an environment indicating the two ends of the room where the patient should stand.
   - "RESET": Remove visual cues from the scene if necessary (although this is rarely required since cues are reset in the code as needed).
   - "RESTART": Restart the application to the setup phase in case of any issues.
   - "TYPE": Switch between displaying footprint cues and stripe cues.
   - "DOOR": Used for the first obstacle if the patient has difficulty opening the door; the operator can assist by triggering the command.

5. **Customize Features:** You can customize the commands by adding or modifying items in the `commands` list within the Python script. To associate an image with each command, place the corresponding PNG image in the "AR_Environment/UDP" folder, following the same method used for the existing buttons.

Here is an overview of the variables to modify in the "UDPclient.py" script:

![TutoUDP1](https://i.imgur.com/P4xzQn6.jpg)
![TutoUDP2](https://i.imgur.com/caaGdJN.jpg)

Here is a screenshot of the graphical user interface (GUI) created with TKinter, showing the buttons associated with various features and commands:

![TutoUDP3](https://i.imgur.com/Y2UWEoj.jpg)

Please make sure that your HoloLens device is correctly connected to your computer on the same network before running the Python script and interacting with the HoloGait application.

***It's important to note that during the development phase for debugging on the Unity editor, you'll need to authorize the firewall to let incoming data through to Unity in order to receive UDP commands. In addition, you'll need to modify the IP address in the code to match that of your computer.***

If you encounter any issues or have specific requirements, you can easily add or modify features by extending the commands list in the "UDPclient.py" script and associating corresponding images for the buttons.

## Application Overview

This section provides an overview of the functionality and flow of the "_Hologait" application for Microsoft HoloLens. All the codes are thoroughly commented, but detailed explanations will not be provided here. You can refer directly to their respective folders in "Sources/Scripts" or "Sources/Imported/Scripts" for a deeper understanding.

### Getting Started

To begin, the patient must be positioned at one of the two ends of the room, suitable for the course, while standing upright. The supervisor can then launch the "_Hologait" application from the "App Manager" in the Microsoft HoloLens. The patient's initial position represents the Unity scene's origin, and the direction they face defines the Z-axis's direction in the scene.

### Setting Up the Course

The first step of the application, besides potential eye calibration, is setting up the course. This is achieved by utilizing the spatial mesh generated by the HoloLens when scanning the room. The spatial mesh allows us to find the floor's position accurately, enabling correct placement of the course at the appropriate height. While the floor is being sought, the message "Please look at the floor" is displayed in front of the patient. The supervisor should guide the patient to look at the floor in front of the opposite end of the room, ensuring that the course is not misaligned. The supervisor controls and notifies the application using UDP commands "YES" and "NO" to indicate whether the floor has been found or not. Once a potential floor position is detected within a certain distance (e.g., 3 meters, adjustable), a rotating arrow appears at the found position, asking, "Is this the floor?" just above it. The supervisor must send "YES" if the position is correct; otherwise, they send "NO," and the application reenters the floor search mode for 2 seconds. Once the floor is found and accepted with the "YES" command, the course appears, ideally positioned if everything went well. This process is managed by the "GetPositionOnSpatialMap()" function in the "LookingDirectionHelpers.cs" script located in "Assets/MRTKExtensions/Utilities." This function traces a raycast on the spatial map directly in front of the camera's direction and returns the position if found, as seen in the following code snippet:
```csharp
// Code snippet from "LookingDirectionHelpers.cs"
public static Vector3? GetPositionOnSpatialMap(float maxDistance = 2, BaseRayStabilizer stabilizer = null)
{
    var transform = CameraCache.Main.transform;
    var headRay = stabilizer?.StableRay ?? new Ray(transform.position, transform.forward);
    if (Physics.Raycast(headRay, out var hitInfo, maxDistance, GetSpatialMeshMask()))
    {
        return hitInfo.point;
    }
    return null;
}
```
The "GetPositionOnSpatialMap()" function is utilized by the "CheckLocationOnSpatialMap()" function in "Sources/Imported/Scripts/FloorFinder.cs", which checks if a potential floor position is found and displays the rotating arrow accordingly following this code : 
```csharp
// Code snippet from "FloorFinder.cs"
        private void CheckLocationOnSpatialMap()
        {
            if (foundPosition == null && Time.time > _delayMoment)
            {
                foundPosition = LookingDirectionHelpers.GetPositionOnSpatialMap(maxDistance);
                if (foundPosition != null)
                {
                    if (CameraCache.Main.transform.position.y - foundPosition.Value.y > 1f)
                    { 
                        lookPrompt.SetActive(false);
                        confirmPrompt.transform.position = foundPosition.Value;
                        confirmPrompt.SetActive(true);
                        buttonYesNo.SetActive(true);
                        locationFoundSound.Play();
                    }
                    else
                    {
                        foundPosition = null;
                    }
                }
            }
        }
```
The supervisor can manually control this process with the "Reset()" and "Accept()" functions called with "YES" or "NO." You can refer directly to the thoroughly commented code for more details.

This is the arrow that appears when the floor is found and asks the supervisor if it is the correct position:

<p align="center">
  <img src="https://i.imgur.com/bLMiy7I.png" alt="FloorArrow">
</p>

### Disabling Spatial Mesh

Once the course setup is complete, the supervisor should send the "MESH" command to disable the spatial mesh of the HoloLens, which can obstruct the patient's visibility of the course. The command triggers the "ToggleSpatialMap()" function in the "SpatialMapToggler.cs" script, which disables all observers if they are active or enables them if the command is sent again.

### Course Obstacles
The course contains several obstacles that the patient needs to navigate through. These obstacles include:

1. Door: The door must be opened by pressing a button. When the button is pressed, the "OpenDoor.cs" script's coroutine is triggered, which rotates the door until it reaches a rotation of 120 degrees (modifiable) and then hides the button.

2. Column: The patient must navigate around a column with directional arrows indicating the correct direction.

3. Bushes: Bushes are represented as objects to be stepped over.

4. TriggerBox: The patient needs to reach the center of the trigger box, indicated by a middle arrow and a message. Upon entering the box, the message "Please turn around" appears, and the second part of the course becomes visible. This functionality is implemented by the "TriggerCourse.cs" script, which checks the tag of the object entering its collider. If it has the "Player" tag, it proceeds to the second part of the course.

5. Water Passage: An obstacle requiring the patient to cross over a moving water passage, implemented using a shader in "Sources/Colors/water."

6. Fake Hole: This part has a fake hole in the middle, attempting to confuse the patient. If the supervisor sends the "CUES" command, arrow paths are displayed on the floor, one in red and one in green, indicating two possible paths to navigate around the fake hole, allowing the supervisor to observe the patient's preference.

7. Table and Objects: The final obstacle involves a table with three objects (hammer, hot-dog, rubik's cube) and three slots to place them. This serves as a mini-game, and once all three objects are correctly placed, the course is completed. The slots have trigger colliders that check the tag of the deposited object. If the tag matches the correct object, the "obstacle6manager.cs" script increments the number of correctly placed objects. Various scripts such as "triggerHammer.cs," "triggerHotDog.cs," and "TriggerRubiks.cs" control this process, verifying if the object entered in the collider is correct. Once all objects are correctly placed, the scene transitions to the end of the course, showing platforms representing the two ends of the room.

### Supervisor Commands

During the course, the supervisor can interact with the application and send various commands:

- CUES: The supervisor can choose to display predefined arrow paths on the floor to assist the patient in navigation. Sending this command displays the correct arrow path based on the current phase of the course.

- STOP: The supervisor can use the "STOP" command to halt the application in case of any issues or to show the end scene immediately with the platforms representing the room's ends.

- RESTART: Sending the "RESTART" command restarts the application from the beginning, prompting the supervisor to find the floor again.

- FOG: In case the detection of Freezing of Gait (FoG) is not successful, the supervisor can manually trigger the display of visual cues using the "FOG" command. The "EyeTrackingManager.cs" script handles the eye-tracking system. The function "getEyeTrackingData()" retrieves the eye-tracking data at the moment of FoG detection, and "placeCues()" then instantiates front cues to show them 1 meter in front of the patient. The cues may include footprints or stripes, which can be changed at any time by sending the "TYPE" command. The cues are displayed between the origin of the patient's gaze (adjusted to the floor's height) and the position they are looking at, calculating the distance and number of steps required to reach that position. These cues guide the patient until they have traversed a certain distance, at which point the cues disappear, indicating the patient has moved beyond the FoG phase.

- EyeTrackingManager.cs: This script manages the eye-tracking system. It holds variables for different cue types and checks for incoming commands such as "MESH," "RESET," "TYPE," or "FOG." The script allows anyone to access eye-tracking data through a public function that returns an array of eye-tracking information, including gaze direction, gaze origin, head movement direction, head velocity, hit normal, hit position, and cursor position. These different data are explained directly in the code comments.

### Course Behavior Control

The behavior of the course is managed by the "Parcours_Manager.cs" script, which utilizes the "currentObstacleState" variable. This variable, of type Enum with three states ("Parkour_1," "Parkour_2," "Stop"), controls whether the first or second part of the course should be displayed or if the course should be stopped. The public function "changeObstacle()" allows for switching between different parts of the course based on the current state of the application. Additionally, the script monitors incoming UDP commands such as "RESTART," "CUES," "PARKOUR," and "STOP." When "CUES" is received, it calls the "showPath()" function to display the appropriate arrow path on the floor based on the current course state.

### UDP Communication

The "UDPClientServer.cs" script establishes a UDP server listening on port 8080 (modifiable) and waits for messages received at the correct IP address. The received message is copied into the "command" variable of "EyeTrackingManager.cs" to control the application.

### Eye-Tracking Data Logging

Lastly, the "WriteEyeTrackingData.cs" script enables the creation of a CSV file that writes eye-tracking data every 10ms. The data is retrieved using the corresponding function from "EyeTrackingManager.cs" and formatted to be saved as a CSV file. Depending on the commented or uncommented line (as specified in the code comments), the CSV file is either saved in the "Data" folder if the application is launched in the Unity editor or stored and accessible through the Device Portal at the HoloLens' IP address, in the "_Hologait" application's "/LocalState" directory.
The CSV file is represented as follows:

![Imgur](https://i.imgur.com/w6n3P2L.png)

This overview provides a glimpse of the "_Hologait" application's functioning. Some code details have not been explained here, but they are thoroughly commented and relatively easy to comprehend. This overview should give you a comprehensive understanding of how the application works and serves as a reference for any future modifications or improvements.

## Replay HoloGait App

In addition to the main "_Hologait" application running on the Microsoft HoloLens, there is a separate application called "Replay HoloGait App" located in the "Replay_HoloGait_App" directory. This application is designed to run directly on a computer and utilizes the eye-tracking data stored in the CSV file generated at the end of using the "_Hologait" application.

The purpose of the "Replay HoloGait App" is to recreate and visualize the patient's movements within the course. The eye-tracking data from the CSV file is used to trace the patient's path, including their gaze direction and other relevant information. This feature serves as a valuable tool for doctors or supervisors to better understand the patient's experience during the course and identify any potential issues or areas of improvement.

### Implementation Details

The "Replay HoloGait App" is built using Python, and it relies on the eye-tracking data stored in the CSV file. The script processes the data to recreate the patient's movements in the course along the X-axis (sideways movements) and Z-axis (forward and backward movements). Unfortunately, the Y-axis data is not precise and is therefore not utilized in the visualization.

The current version of the Python script provides a basic representation of the patient's movement in the space. However, it is important to note that the data from MRTK2 eye tracking in Unity might not be very accurate or stable. As a result, the visualization may not perfectly reflect the patient's actual movements within the course.

### Future Improvements

As suggested by my supervisor Mathias, further improvements can be made to enhance the accuracy and usability of the "Replay HoloGait App." Implementing this application directly in Unity, combining C# scripts with Python in a Python environment in Unity, can help refine the visualization process and potentially yield more precise results.

The objective is to achieve a more accurate and reliable representation of the patient's movement within the course. This improved visualization will provide valuable insights for medical professionals and supervisors, aiding them in understanding the patient's experience and making informed assessments.

Once implemented and refined in Unity, the "Replay HoloGait App" will become an essential component of the entire "_Hologait" system, complementing the main HoloLens application and further facilitating patient evaluation and treatment.

Please find below a screenshot of the current Python-based visualization, representing the patient's movement within the course:

<p align="center">
  <img src="https://i.imgur.com/45RWEA8.png" alt="Replay HoloGait App Screenshot">
</p>

(As this is a work in progress, further improvements will be made to achieve the desired results.)


## Limitations and Improvements

1. **Limitations**:
    - **Limited Adaptability**: The current version of the Hologait application is designed specifically for the Gait room at the Cereneo clinic at Park Hotel. This restricts its usability to spaces with similar dimensions, although any room or corridor of comparable size could suffice. To enhance the application's versatility, future versions should incorporate features to adapt the course layout based on the room's dimensions, either by sending UDP messages with the room dimensions to the Hololens application or by leveraging the Hololens' spatial mapping capabilities to dynamically adjust the course layout.

    - **Single Course Design**: As the first version, the application offers only one course design, which may not be suitable for all patients. To address this limitation, multiple course options should be considered for patients to choose from at the beginning of the application. These courses can be designed based on patient feedback and therapist recommendations.

    - **Eye Tracking Calibration Complexity**: The setup process for the Hololens, particularly the eye tracking calibration, can be challenging for patients with Parkinson's disease. Automating the eye tracking calibration without requiring patient input remains a challenge. Incorrect calibration leads to misplacement of visual cues, affecting the effectiveness of the application. Finding alternative approaches to calibrate the eye tracking or simplifying the calibration process would be beneficial.

    - **Hololens Immersion**: The Hololens may not provide an immersive experience everytime, especially for elderly patients unaccustomed to new technologies. Adjusting the headset and visor properly can be difficult, given the limited field of view of the Hololens. Additionally, issues with color perception and translucency within the application need to be addressed. Exploring other advanced headsets like Magic Leap or Apple Vision Pro, if available in 2024, might offer better solutions to these problems.

    - **Streaming Issues**: The streaming function from the Hololens can sometimes encounter bugs, leading to interruptions in monitoring the patient's view. Exploring alternative methods for real-time monitoring could mitigate this limitation.

2. **Improvements**:

    - **Adaptive Course Design**: Develop a system that allows the course layout to adapt to the dimensions of the room or environment automatically. This can enhance the application's versatility and accessibility in different settings.

    - **Multiple Course Options**: Create a selection of course designs with varying levels of complexity. This will provide patients with choices that suit their individual needs and challenges, allowing for a more personalized and effective training experience.

    - **Continuous Visual Cues**: Prioritize creating a simple scene without complex courses first, where patients can receive continuous visual cues through eye tracking. These cues can act as a preventive measure for Freezing of Gait (FoG) and aid patients in navigating freely.

    - **Simplified Eye Tracking Calibration**: Investigate ways to streamline the eye tracking calibration process to make it more user-friendly and less demanding for patients. This could involve automated calibration techniques or intuitive interfaces.

    - **Alternative Headsets**: Explore the use of other headsets with improved immersive features and color perception to enhance the patient's experience and overall engagement.

    - **Remote Control and Mobile Application**: Develop a mobile application that allows therapists or patients to remotely control the application and trigger visual cues or FoG alerts. Perhaps also a small remote control for the patient with a button to send a command to the Hololens to prevent a FoG, because a Parkinson's patient knows when a FoG is about to occur (good suggestion by **Dr. Leopold**). This would eliminate the need for a computer running Python scripts.

    - **Enhanced Monitoring**: Look into alternative approaches for real-time patient monitoring that offer a more reliable and uninterrupted stream of the patient's view during the session.

Despite the limitations and challenges presented by the Hololens and the current version of the Hologait application, valuable feedback from the patient with Parkinson's disease and the supervising therapist indicates that the application shows promise as a training tool. Addressing these limitations and implementing suggested improvements can significantly enhance the application's usability and effectiveness in assisting patients with Parkinson's disease and Freezing of Gait.


## Conclusion
The HoloGait-Project offers an innovative and personalized solution to address the freezing of gait phenomenon in Parkinson's disease. By leveraging augmented reality, eye tracking, UDP command controls, and a haptic feedback system, HoloGait aims to empower patients and improve their mobility and independence.

For more detailed information, technical specifications, and code implementation details, please refer to the documentation and code provided in this repository.

## Acknowledgments
The HoloGait project was made possible thanks to the collaboration and support of various individuals and organizations. I would like to extend my gratitude to:

- The supervisors of the HoloGait project, **Chris**, **Mathias**, and **Mathilde**, for their guidance and support throughout the development process.

- Special thanks to **Mathias Bannwart**, the AR Environment supervisor, for being my direct supervisor during the development of the HoloLens application. Mathias provided essential guidance, information, and assistance throughout the project, ensuring its successful implementation. He was always available to help with any issues that arose.

- The patients and therapists at the **Cereneo Clinic in Hertenstein** for allowing us to test the HoloLens and the application and providing invaluable feedback. Their participation made the testing process enriching and insightful.

- The **Cereneo Center for Neurology and Rehabilitation** for providing the necessary resources and facilities for testing and refining the HoloGait application.

- The **Mixed Reality Toolkit (MRTK) Community** for their open-source framework, which significantly contributed to the development of HoloGait. Especially, I would like to thank **Joost Van Schaik** for his helpful articles and tutorials on HoloLens application development.

- **Microsoft** for providing valuable documentation, tools, and support for HoloLens application development.

All this has enabled the Hologait project to run smoothly and be completed in good conditions..

## Contact Information
For inquiries or further information about the HoloGait project, please contact:

- Supervisors HoloGait: Chris Awai, Mathias Bannwart, Mathilde Lestoille
- AR Environment supervisor: Mathias Bannwart
- App created by: Ilyes EL BAHRI
- Haptic Feedback System: Louis Dubarle
- FoG Detection: Adam Khazrane
- Emails: elbahri.ilyes94@gmail.com, chris.awai@cereneo.foundation, mathias.bannwart@cereneo.foundation, mathilde.lestoille@cereneo.foundation, louisdubarle@icloud.com, adam.kha@free.fr

Feel free to reach out to us with any questions, feedback, or collaboration opportunities.

## Important Links - Documentation, Tutorials, and References
Here are some useful links and documentation that have been instrumental in the development of this project:

### Unity Documentation
- [Unity Documentation](https://docs.unity3d.com/Manual/XR.html)
- [Unity Discussions](https://forum.unity.com/forums/ar-vr-xr-discussion.80/)

### Joost Van Schaik's website
- [Website](https://localjoost.github.io/)
- [Building a floating HoloLens ‘info screen’ - 2: adding the C# behaviours](https://localjoost.github.io/building-floating-hololens-info-screen-2/)
- [Using a HoloLens scanned room inside your HoloLens app](https://localjoost.github.io/using-hololens-scanned-room-inside-your/)
- [Using Scene Understanding in the Unity Editor](https://localjoost.github.io/Using-Scene-Understanding-in-the-Unity-Editor/)
- [Accessing and recording eye tracking data with MRTK3](https://localjoost.github.io/Accessing-and-recording-eye-tracking-data-with-MRTK3/)
- [HoloLens CubeBouncer application part 2-create the gaze aligned cube grid](https://localjoost.github.io/hololens-cubebouncer-application-part-2/)
- [Finding the floor - and displaying holograms at floor level in HoloLens apps](https://localjoost.github.io/finding-floor-and-displaying-holograms/)
- [Migrating to MRTK2–interacting with the Spatial Map](https://localjoost.github.io/migrating-to-mrtk2interacting-with/)
- [Finding the Floor with HoloLens 2 and MRTK 2.7.3](https://localjoost.github.io/Finding-the-Floor-with-HoloLens-2-and-MRTK-273/)
- [Migrating to MRTK2: using a Spatial Mesh inside the Unity Editor](https://localjoost.github.io/migrating-to-mrtk2-using-spatial-mesh/)
- [Migrating to MRTK2 - setting up and understanding Eye Tracking](https://localjoost.github.io/migrating-to-mrtk2-setting-up-and/)

### Microsoft Documentation
- [Install the tools](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/install-the-tools)
- [Unity development for HoloLens](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/unity-development-overview?tabs=arr%2CD365%2Chl2)
- [Unity Tutorials](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/tutorials)
- [Choosing a Unity version and XR plugin](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/choosing-unity-version)
- [Set up a new OpenXR project with MRTK](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/new-openxr-project-with-mrtk)
- [Using Visual Studio to deploy and debug](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/using-visual-studio?tabs=hl2)
- [Connect HoloLens to a network](https://learn.microsoft.com/en-us/hololens/hololens-network)
- [Exercise - Configure Unity for Windows Mixed Reality](https://learn.microsoft.com/en-us/training/modules/learn-mrtk-tutorials/1-3-exercise-configure-unity-for-windows-mixed-reality)
- [Using the HoloLens Emulator](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/using-the-hololens-emulator)
- [Holographic remoting — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/tools/holographic-remoting?view=mrtkunity-2022-05)
- [Getting started with MRTK2 and XR SDK](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/configuration/getting-started-with-mrtk-and-xrsdk?view=mrtkunity-2022-05#windows-mixed-reality)
- [HoloLens 2 fundamentals: develop mixed reality applications](https://learn.microsoft.com/en-us/training/paths/beginner-hololens-2-tutorials/)
- [What is Mixed Reality Toolkit 2?](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/?view=mrtkunity-2022-05#documentation)
- [Introduction to mixed reality development](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/development)
- [Introduction to the Mixed Reality Toolkit--Set Up Your Project and Use Hand Interaction](https://learn.microsoft.com/en-us/training/modules/learn-mrtk-tutorials/1-1-introduction)
- [MRTK2 profile configuration guide](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/configuration/mixed-reality-configuration-guide?view=mrtkunity-2022-05)
- [Interaction models](https://learn.microsoft.com/en-us/training/modules/learn-mrtk-tutorials/1-6-interaction-models)
- [Experience settings — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/experience-settings/experience-settings?view=mrtkunity-2022-05)
- [Mixed Reality scene content — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/experience-settings/scene-content?view=mrtkunity-2022-05)
- [Spatial mapping in Unity](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/spatial-mapping-in-unity?tabs=mrtk)
- [Scene understanding](https://learn.microsoft.com/en-us/windows/mixed-reality/design/scene-understanding)
- [Scene understanding observer — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/spatial-awareness/scene-understanding?view=mrtkunity-2022-05)
- [IMixedRealitySpatialAwarenessObserver Interface](https://learn.microsoft.com/fr-fr/dotnet/api/microsoft.mixedreality.toolkit.spatialawareness.imixedrealityspatialawarenessobserver?view=mixed-reality-toolkit-unity-2020-dotnet-2.8.0)
- [Configuring mesh observers via code — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/spatial-awareness/usage-guide?view=mrtkunity-2021-01)
- [Speech — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/input/speech?view=mrtkunity-2022-05)
- [Getting started with eye tracking in MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/input/eye-tracking/eye-tracking-basic-setup?view=mrtkunity-2022-05)
- [Eye tracking in Mixed Reality Toolkit — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/input/eye-tracking/eye-tracking-main?view=mrtkunity-2022-05)
- [Eye tracking on HoloLens 2](https://learn.microsoft.com/en-us/windows/mixed-reality/design/eye-tracking)
- [Accessing eye tracking data in your Unity script — MRTK2](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/features/input/eye-tracking/eye-tracking-eye-gaze-provider?view=mrtkunity-2022-05)

- [Try out the MRTK2 Examples Hub](https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/mrtk2/running-examples-hub?view=mrtkunity-2022-05)
- [Improve visual quality and comfort](https://learn.microsoft.com/en-us/hololens/hololens-calibration)

### Other Documentation

- [How-To: Use Spatial Understanding to Query your Room with HoloLens](https://medium.com/southworks/how-to-use-spatial-understanding-to-query-your-room-with-hololens-4a6192831a6f)
- https://stackoverflow.com/questions/64532409/how-to-support-on-screen-touch-keyboard-in-hololens-2-directx12-app
- https://stackoverflow.com/questions/61910125/how-to-connect-hololens-2-emulator-with-a-local-udp-sender
- https://stackoverflow.com/questions/74365274/exporting-eye-tracking-data-on-hololens-2

### Some videos that helped me
- [Getting Started with Unity for Hololens2 | Tutorial](https://www.youtube.com/watch?v=dOsYerpKloY)
- Playlist : [Mixed Reality Toolkit (MRTK) Tutorials With Unity](https://www.youtube.com/playlist?list=PLQMQNmwN3FvzWQ1Hyb4XRnVncvCmcU8YY)

Feel free to explore these resources for more in-depth information and guidance on specific aspects of the project.