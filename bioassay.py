import cv2
import numpy as np

# Definisikan skala warna RGB yang sesuai dengan paper
# Contoh: warna dan densitas berdasarkan tabel 1 dan 2 pada dokumen.
# Definisikan skala warna RGB yang sesuai dengan paper
# Warna dan densitas berdasarkan tabel 1 dan 2 pada dokumen.
density_scale = {
    "S1": {"color": [85, 60, 50], "density": ">597x10^4 cells/mL"},
    "S2": {"color": [100, 75, 65], "density": "457-597x10^4 cells/mL"},
    "S3": {"color": [120, 95, 80], "density": "311-457x10^4 cells/mL"},
    "S4": {"color": [140, 115, 100], "density": "267-311x10^4 cells/mL"},
    "S5": {"color": [160, 135, 120], "density": "202-267x10^4 cells/mL"},
    "S6": {"color": [180, 155, 140], "density": "160-202x10^4 cells/mL"},
    "S7": {"color": [200, 175, 160], "density": "134-160x10^4 cells/mL"},
    "S8": {"color": [220, 195, 180], "density": "108-134x10^4 cells/mL"},
    "S9": {"color": [240, 215, 200], "density": "78-108x10^4 cells/mL"},
    "S10": {"color": [255, 235, 220], "density": "<78x10^4 cells/mL"}
}


def find_nearest_density(color, density_scale):
    min_dist = float('inf')
    closest_match = None
    for key, value in density_scale.items():
        dist = np.linalg.norm(np.array(color) - np.array(value["color"]))
        if dist < min_dist:
            min_dist = dist
            closest_match = key
    return closest_match

# Fungsi untuk mendapatkan warna rata-rata
def get_average_color(image, x, y, w, h):
    roi = image[y:y+h, x:x+w]
    avg_color = np.mean(roi, axis=(0, 1))
    return avg_color

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        break
    
    # Define area of interest (ROI)
    height, width, _ = frame.shape
    roi_x, roi_y = width // 4, height // 4
    roi_w, roi_h = width // 2, height // 2
    
    # Get average color in the ROI
    avg_color = get_average_color(frame, roi_x, roi_y, roi_w, roi_h)
    
    # Find the closest match in the density scale
    closest_match = find_nearest_density(avg_color, density_scale)
    density_info = density_scale[closest_match]["density"]
    
    # Display density information on the image
    cv2.putText(frame, f"Density: {density_info}", (110, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Draw the ROI and color patch
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 255, 255), 2)
    color_patch = np.zeros((50, 100, 3), np.uint8)
    color_patch[:] = avg_color
    frame[0:50, 0:100] = color_patch
    
    # Display the frame
    cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
