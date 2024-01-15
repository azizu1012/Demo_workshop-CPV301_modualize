# Function 1: Create a white background
import numpy as np
import cv2

def create_white_background(width, height):
    # Create a new image with white background
    image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Create a window named 'Image'
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    
    # Attempt to set the window to be topmost
    cv2.setWindowProperty('Image', cv2.WND_PROP_TOPMOST, 1)

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image