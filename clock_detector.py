import cv2
import numpy as np
from constants import *
from state import Position


class ClockDetector:

    @staticmethod
    def _get_screenshot_tile_xy(x, y):
        tile_x = round(((x * DISPLAY_WIDTH / SCREENSHOT_WIDTH - TILE_INIT_X) / TILE_WIDTH) - 0.5)
        tile_y = round(
            ((DISPLAY_HEIGHT - TILE_INIT_Y - y * DISPLAY_HEIGHT / SCREENSHOT_HEIGHT) / TILE_HEIGHT) - 0.5
        )
        return tile_x, tile_y

    @staticmethod
    def draw_bounding_boxes(image, contours):
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Draw the bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw dots for the corners and center
            corners = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
            center = (x + w // 2, y + h // 2)
            for corner in corners:
                cv2.circle(image, corner, 5, (255, 0, 0), -1)  # Blue dots for corners
            cv2.circle(image, center, 5, (0, 0, 255), -1)  # Red dot for center

        # Display the image with bounding boxes and dots
        cv2.imshow("Detected Clocks with Dots", image)
        #cv2.waitKey(0)

    @staticmethod
    def identify_clocks(_image):
        MIN_AREA = 10
        if _image is None:
            raise ValueError("Invalid image provided.")

        image = cv2.cvtColor(np.array(_image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("clock_detector.png", image)
        #print(image)
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define vibrant red color range in HSV
        # lower_red1 = np.array([0, 190, 240])
        # upper_red1 = np.array([5, 210, 255])
        # lower_red2 = np.array([175, 190, 240])
        # upper_red2 = np.array([180, 210, 255])

        # Tweaked for mac
        lower_red1 = np.array([0, 210, 235])
        upper_red1 = np.array([5, 255, 255])
        lower_red2 = np.array([175, 210, 235])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for red
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 | mask2

        # Prevent overtime detection
        # Calculate bounds for the middle 95% of the width
        image_width = image.shape[1]
        lower_bound = int(image_width * 0.025)
        upper_bound = int(image_width * 0.975)

        # Zero out pixels outside the middle 95% of the width
        red_mask[:, :lower_bound] = 0
        red_mask[:, upper_bound:] = 0

        # Find contours in the mask
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Optional: Draw bounding boxes and dots (can be commented out later)
        ClockDetector.draw_bounding_boxes(image, contours)

        clocks = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > MIN_AREA:
                x, y, w, h = cv2.boundingRect(contour)
                center_x, top_y = x + w/2, y
                print("center_x, top_y", center_x, top_y)
                tile_x, tile_y = ClockDetector._get_screenshot_tile_xy(center_x, top_y)
                position = Position(tile_x, tile_y)
                clocks.append(position)

        return clocks