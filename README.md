GestureMate is a project that leverages the powerof computer vision. It is a touchless interactive system that allows users to control screen brightness and volume using hand gestures captured by a webcam.
# GestureMate: Hand Gesture based Brightness and Volume Control

Programming Language: **Python**

Libraries: 
- OpenCV – handles video captures and frame processing
- MediaPipe – Utilized for accurate hand landmark detection, tracking and recognition.
- NumPy – for numerical operations, including interpolating the volume and brightness level.
- Flask – to link the front-end and back-end, serving real-time
- video feeds and processing gestures.
- Pycaw: to control audio volume via gesture input.
- Python (Backend processing)
- HTML/CSS/JavaScript (Frontend interface)

## **Note: Left hand is for controlling brightness of the system and Right hand is for controlling the volume of the system.**

# Working of the project
![Screenshot 2024-11-25 002926](https://github.com/user-attachments/assets/c3f7fcd7-96a5-4c63-b92d-0c1dc9d5f20c)

1.	Hand Detection and Tracking:
- Video Capture: The webcam captures video frames in real-time.
- Image Preprocessing: Each frame is preprocessed to enhance image quality and facilitate hand detection.
-	Hand Landmark Detection: MediaPipe's hand landmark detection model is used to identify key points on the hand, such as fingertips, wrist, and palm.
-	Hand Tracking: The detected hand landmarks are tracked across consecutive frames to ensure smooth and accurate gesture recognition.
2.	Gesture Recognition:
-	Feature Extraction: Relevant features, such as the distance between specific landmarks or the angle between fingers, are extracted from the detected hand.
-	Gesture Mapping: Recognized gestures are mapped to specific control actions, such as increasing or decreasing brightness or volume.
3.	Control Signal Generation:
-	System Interaction: Once a gesture is recognized, the system generates appropriate control signals to interact with the device's operating system or hardware.
-	Brightness Control: The system can send commands to the operating system to adjust the screen brightness level.
-	Volume Control: The system can interface with the audio output device to control the volume level.
4.	User Interface:
=	Video Feed: A live video feed displays the hand gestures being recognized by the system.
-	Gesture Hints: On-screen prompts or tutorials can guide users on how to perform specific gestures.
