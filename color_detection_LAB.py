import cv2
import numpy as np

def get_average_color_lab(image, x, y, w, h):
    # Crop the region of interest
    roi = image[y:y+h, x:x+w]
    # Convert to LAB color space
    lab_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
    # Calculate the average color of the ROI
    average_color = np.mean(lab_roi, axis=(0, 1))
    return average_color

def lab_to_rgb(color):
    return cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_LAB2BGR)[0][0]

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        break
    
    # Define the area of interest (e.g., the central part of the image)
    height, width, _ = frame.shape
    roi_x, roi_y = width // 4, height // 4
    roi_w, roi_h = width // 2, height // 2
    
    # Get the average color in LAB space
    avg_color_lab = get_average_color_lab(frame, roi_x, roi_y, roi_w, roi_h)
    avg_color_bgr = lab_to_rgb(avg_color_lab)
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
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
