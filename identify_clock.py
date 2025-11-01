import cv2
import numpy as np


def identify_red_clocks(image):
    if image is None:
        raise ValueError("Invalid image provided.")

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define vibrant red color range in HSV
    lower_red1 = np.array([0, 190, 240])  # Lower range for the specific red
    upper_red1 = np.array([5, 210, 255])
    lower_red2 = np.array([175, 190, 240])  # Upper range for the specific red (wrap-around)
    upper_red2 = np.array([180, 210, 255])

    # Create masks for red
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2

    # Find contours in the mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers = []  # List to store the center horizontal and topmost vertical coordinates

    # Iterate through contours to find the red clock
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10:  # Adjust area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2  # Center horizontal
            topmost_y = y  # Topmost vertical
            centers.append((center_x, topmost_y))

            # Draw the bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Draw the center and topmost point
            cv2.circle(image, (center_x, topmost_y), 5, (255, 0, 0), -1)

    # Show the result (optional)
    cv2.imshow("Detected Clock with Bounding Boxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return centers


# Example usage
image = cv2.imread("screenshots/enemy_clock.png")
if image is None:
    raise ValueError("Image not found or invalid path.")

centers = identify_red_clocks(image.copy())
print("Center horizontal and topmost vertical coordinates:", centers)