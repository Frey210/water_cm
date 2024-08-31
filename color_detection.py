import cv2
import numpy as np

def get_average_color(image, x, y, w, h):
    # Crop the region of interest
    roi = image[y:y+h, x:x+w]
    # Convert to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Calculate the average color of the ROI
    average_color = np.mean(hsv_roi, axis=(0, 1))
    return average_color

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        break
    
    # Define the area of interest (e.g., the central part of the image)
    height, width, _ = frame.shape
    roi_x, roi_y = width // 4, height // 4
    roi_w, roi_h = width // 2, height // 2
    
    # Get the average color in the region of interest
    avg_color_hsv = get_average_color(frame, roi_x, roi_y, roi_w, roi_h)
    avg_color_bgr = cv2.cvtColor(np.uint8([[avg_color_hsv]]), cv2.COLOR_HSV2BGR)[0][0]
    color_hex = rgb_to_hex(avg_color_bgr)
    
    # Create a color patch
    color_patch = np.zeros((50, 100, 3), np.uint8)
    color_patch[:] = avg_color_bgr
    
    # Place the color patch in the top-left corner of the frame
    frame[0:50, 0:100] = color_patch
    
    # Place the hex color text beside the color patch
    cv2.putText(frame, color_hex, (110, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Draw the region of interest (ROI)
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 255, 255), 2)
    
    # Display the resulting frame
    cv2.imshow('Camera', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
