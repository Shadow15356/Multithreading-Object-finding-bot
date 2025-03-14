# Multithreading-Object-finding-bot_XGO_EDU
XGO Rescue Dog - AI-Powered Search & Rescue Robot
This project utilizes the XGO Lite robotic dog and XGO EDU module to perform search and rescue operations. The robot detects a professional, estimates their age and  navigates towards an injured person while adjusting its speed based on their estimated mobility. It uses YOLO object detection, servo-based navigation, and multithreading to efficiently locate and approach people in need.

Features
Age-Based Speed Adaptation - Adjusts movement speed based on detected age group.
Real-Time YOLO Object Detection - Uses YOLO Fast to detect and track people.
Autonomous Navigation - Aligns and moves toward detected individuals.
Emotional Response - Displays facial expressions and sounds based on detection.
Multi-Threaded Processing - Runs object detection and navigation in parallel for real-time operation.

Hardware Components
XGO Lite (Quadruped Robot)
XGO EDU (Advanced AI & Vision Module)
Servo Motors (For movement and head rotation)
LCD Display (For emotional expressions)
Speaker (For sound-based feedback)

Code Breakdown
 1. Age-Based Speed Adjustment (age_adaptation())
Uses the XGO EDU’s facial recognition to estimate the age of detected individuals.
Sets movement speed based on the age group for optimal rescue speed.
Age Group	Speed	Motor Power
0-20 years	10	255 (Fastest)
25-43 years	15	128 (Medium)
48-100 years	20	1 (Slowest)
 2. Object Detection (YOLO) (yolo_detection())
Uses YOLO to detect objects in real-time.
Filters results to track only "person" objects for rescue operations.
Updates found_object with the detected person's position.
 3. Navigation & Movement (navigation())
Waits until speed is set from age_adaptation().
Aligns the robot to face the detected person using X-coordinate analysis.
Moves towards the person while continuously adjusting direction.
Displays sad.jpg and plays sad.wav if it detects distress.
Turns around and moves towards a container after rescue.
Multithreading Implementation
The program runs YOLO detection and navigation in parallel using Python’s threading module:

yolo_thread = threading.Thread(target=yolo_detection, daemon=True)
navigation_thread = threading.Thread(target=navigation, daemon=True)

yolo_thread.start()
navigation_thread.start()
This ensures real-time responsiveness while scanning and navigating.

Future Improvements
 Enhance Object Tracking - Implement continuous tracking instead of re-detecting every frame.
 Add GPS/IMU Integration - Improve pathfinding with real-world positioning.
 Cloud Data Logging - Store detection data online for monitoring and analysis.

