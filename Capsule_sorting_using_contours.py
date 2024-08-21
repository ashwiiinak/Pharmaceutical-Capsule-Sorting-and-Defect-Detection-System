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
        colors = {
            "Red": ([0, 100, 100], [10, 255, 255]),
            "Green": ([50, 100, 100], [70, 255, 255]),
            "Blue": ([90, 100, 100], [110, 255, 255]),
            "Yellow": ([20, 100, 100], [30, 255, 255]),
            "Purple": ([140, 100, 100], [160, 255, 255])
        }
        
        detected_color = None
        
        for color, (lower, upper) in colors.items():
            # Threshold the HSV image to get only desired color
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check if any contour is found
            if contours:
                detected_color = color
        
                # Calculate centroid of each contour and draw circle
                for cnt in contours:
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)  # Draw circle at centroid
                # Move servos based on detected color
                if detected_color == "Red":
                    move_servos(90, 30)  # Adjust angles as per your setup
                elif detected_color == "Green":
                    move_servos(90, 60)  # Adjust angles as per your setup
                elif detected_color == "Blue":
                    move_servos(90, 90)  # Adjust angles as per your setup
                elif detected_color == "Yellow":
                    move_servos(90, 0)  # Adjust angles as per your setup
                elif detected_color == "Purple":
                    move_servos(90, 0)  # Adjust angles as per your setup
                time.sleep(1)
                break

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
