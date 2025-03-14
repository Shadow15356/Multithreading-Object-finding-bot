import datetime #importing date time library to get current date and time of found person
import time
import threading#enables threading in the code so that functions can run in parallel
from xgoedu import XGOEDU
from xgolib import XGO

XGO_lite = XGO("xgolite")
XGO_edu = XGOEDU()

# Global variables for my functions
speed = None  
found_object = None  

# Function to determine age and set speed gonna run first
def age_adaptation():
    global speed
    print("Starting Age Detection")  #debugging text letting me know how far the code has come
    result = XGO_edu.agesex()
    
    if result is not None:
        face = result[1]#finding the age which is in the second position of the array, aka 1 as computer counts from 0
        print(f"Detected Age Group: {face}")

        if face in ("(0-2)", "(4-6)", "(8-12)", "(15-20)"):# using the possibilities from the spec sheet im adjusting speed
            speed = 10#speed changes depending on person to lead rescuer to rescuee
            XGO_lite.motor_speed(255)#changes servo speed to to preserve battery in some cases and to use more in others
        elif face in ("(25-32)", "(38-43)"):
            speed = 15
            XGO_lite.motor_speed(128)
        elif face in ("(48-53)", "(60-100)"):
            speed = 20
            XGO_lite.motor_speed(1)
        else:
            speed = 14
        
        print(f"Set Speed to: {speed}")
    else:
        print("No Face Detected! Retrying...")
        time.sleep(2)
        age_adaptation()  # Retry if no face is detected

# Function to detect an object using YOLO
def yolo_detection():
    global found_object
    print("Starting YOLO Object Detection...")
    
    while True:
        detected = XGO_edu.yoloFast()
        
        if detected:
            print(f"YOLO detected: {detected}")  # Always print what is seen

            if detected[0] == "person":  #react to person
                found_object = detected  #store found person
                print(f"Target person detected at X={found_object[1][0]}")#updates users at terminal
            else:
                found_object = None  # Ignore other objects
                print("Ignoring non-bottle object")
        else:
            found_object = None
            print("No object detected")

        time.sleep(0.1)  # Frequent scanning for responsiveness to go along with threading

# Function to control turning and movement while trying to find a person 
def navigation():
    global found_object, speed

    while speed is None:
        print("Waiting for Age Detection to Set Speed...")
        time.sleep(0.5)  # Wait until speed is set

    print("Starting Navigation...")

    while True:
        if found_object:
            x = found_object[1][0]  # X-coordinate of detected object
            print(f"Found {found_object[0]} at X={x}")

            # Turning to align with the bottle if not already aligned
            if x < 122:
                print("Turning right to align")
                XGO_lite.turn(50)  # Turn slightly to the left
                time.sleep(0.5)  # Pause after turn
                XGO_lite.turn(0)  # Stop turning
                time.sleep(0.5)  # Pause for stabilization
            elif x > 222:
                print("Turning left to align")
                XGO_lite.turn(-50)  # Turn slightly to the right
                time.sleep(0.5)  # Pause after turn
                XGO_lite.turn(0)  # Stop turning
                time.sleep(0.5)  # Pause for stabilization
            else:
                print("Turning left to align")
                XGO_lite.turn(50)  # Turn slightly to the left
                time.sleep(1.3)  # Pause after turn
                XGO_lite.turn(0)  # Stop turning
                time.sleep(0.5)  # Pause for stabilization
                print("person aligned, moving towards them...")
                XGO_lite.move_x(speed)  # Move forward towards the bottle
                time.sleep(3.2)  # Move slowly towards the bottle
                XGO_edu.lcd_picture("sad.jpg")#just some dog emotion i  the form of a jpg file
                XGO_edu.xgoSpeaker("sad.wav")
                XGO_lite.action(12)#calls on action operater to make the dog sit
                foundag= age_adaptation()#uses same function again to determine age of found body
                time.sleep(2)
                now = datetime.datetime.now()
                print(f" person found at {now} identified to be approximately {foundag}")
                time.sleep(5)
                identified_age=age_adaptation()
                
                print("moving to container")
                XGO_lite.move_x(0)
                print("Moving forward towards the bottle...")
                
                
                # After moving forward the robot can 
                print("Turning back to align more...")
                XGO_lite.turn(-50)  # Turn back towards the person
                time.sleep(1)  # Pause after turn
                XGO_lite.turn(0)  # Stop turning
                time.sleep(0.5)

        else:
            print("No object found, scanning... Turning slightly")
            XGO_lite.turn(-10)  # Incremental turning while scanning
            time.sleep(0.5)  # Pause before checking again

#main
if __name__ == "__main__":
    print("Starting Robot Sequence...")

    
    age_adaptation()# Finds the co-workers age so the dog doesnt scurry off out of sight too quickly, also a good point to compare multithreading
    time.sleep(2)  # Allow some time to process

    # Starting YOLO recognition and navigation functions in separate threads
    yolo_thread = threading.Thread(target=yolo_detection, daemon=True)#targets the yolo_detection class to thread, also set daemon to true so it ends when main ends
    navigation_thread = threading.Thread(target=navigation, daemon=True)

    yolo_thread.start()
    navigation_thread.start()

    # Keep the program running
    while True:
        time.sleep(1)


