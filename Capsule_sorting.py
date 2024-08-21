import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Initialize servo pins
top_servo_pin = 18
bottom_servo_pin = 19
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(top_servo_pin, GPIO.OUT)
GPIO.setup(bottom_servo_pin, GPIO.OUT)
top_servo = GPIO.PWM(top_servo_pin, 50)
bottom_servo = GPIO.PWM(bottom_servo_pin, 50)
top_servo.start(0)
bottom_servo.start(0)


# Function to control servos
def move_servos(top_angle, bottom_angle):
    # Adjust duty cycle calculation for clockwise movement
    top_servo.ChangeDutyCycle((180 - top_angle) / 18 + 2)
    bottom_servo.ChangeDutyCycle((bottom_angle) / 18 + 2)
    time.sleep(0.02)  # Wait for movement
    top_servo.ChangeDutyCycle(0)  # Stop servo
    bottom_servo.ChangeDutyCycle(0)  # Stop servo


# Main function for color detection and sorting
def color_sorting():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
    no_color_detected_time = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define range of colors in HSV
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])
        lower_blue = np.array([90, 100, 100])
        upper_blue = np.array([110, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        lower_purple = np.array([140, 100, 100])
        upper_purple = np.array([160, 255, 255])
        
        # Threshold the HSV image to get only desired colors
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
        
        # Check if any color detected
        detected_color = None
        if np.sum(mask_red) > 0:
            detected_color = "Orange"
            move_servos(90, 30)  # Adjust angles as per your setup
            time.sleep(1)
        elif np.sum(mask_green) > 0:
            detected_color = "Green"
            move_servos(90, 60)  # Adjust angles as per your setup
            time.sleep(1)
        elif np.sum(mask_blue) > 0:
            detected_color = "Blue"
            move_servos(90, 90)  # Adjust angles as per your setup
            time.sleep(1)
        elif np.sum(mask_yellow) > 0:
            detected_color = "Invalid"
            move_servos(90, 0)  # Adjust angles as per your setup
            time.sleep(1)
        elif np.sum(mask_purple) > 0:
            detected_color = "Invalid"
            move_servos(90, 0)  # Adjust angles as per your setup
            time.sleep(1)
        else:
            detected_color = "None"
            move_servos(0, 0)  # No color detected, keep servos idle
            if no_color_detected_time is None:
                no_color_detected_time = time.time()
            elif time.time() - no_color_detected_time > 5:
                move_servos(45, 1)  
                time.sleep(1)  # Delay for 2 seconds
                no_color_detected_time = None

        
        # Print detected color
        print("Detected Color:", detected_color)
        
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Call the main function
color_sorting()
