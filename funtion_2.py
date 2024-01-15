from PIL import Image
import numpy as np
import cv2

def create_image_without_display(width, height):
    # Create a white image
    image = Image.new('RGB', (width, height), 'white')
    return np.array(image)

def draw_rectangle_on_image():
    # Create a new image every time the function is called
    image = create_image_without_display(1080, 720)
    
    image_copy = np.copy(image)  # Define image_copy here
    drawing = False
    rectangle_done = False
    ix, iy, x, y = -1, -1, -1, -1  # Initialize x and y here
    
    def draw_rectangle_with_mouse(event, ex, ey, flags, param):
        nonlocal ix, iy, drawing, image_copy, rectangle_done, x, y  # Declare image_copy as nonlocal
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = ex, ey
            image_copy = np.copy(image)  # Reset image_copy to the original image
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.rectangle(image_copy, (ix, iy), (ex, ey), (0, 0, 0), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            rectangle_done = True
            x, y = ex, ey  # Update x and y here
            cv2.rectangle(image_copy, (ix, iy), (x, y), (0, 0, 0), -1)
    
    screen_width = 1920  # Replace with your screen width
    screen_height = 1080  # Replace with your screen height

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 540, 360)  # Resize the window to be smaller
    cv2.moveWindow('image', (screen_width - 540) // 2, (screen_height - 360) // 2)  # Move the window to the center of the screen
    cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)  # Make the window stay on top of all other applications
    cv2.setMouseCallback('image', draw_rectangle_with_mouse)
    max_iterations = 10000
    iterations = 0
    while True:
        cv2.imshow('image', image_copy)
        k = cv2.waitKey(1) & 0xFF
        if k == 27 or rectangle_done or iterations > max_iterations or cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break
        iterations += 1
    if rectangle_done:
        cv2.destroyWindow('image')  # Destroy only the 'image' window
        cv2.namedWindow('F2_image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('F2_image', 540, 360)  # Resize the second window to be the same size as the first one
        cv2.moveWindow('F2_image', (screen_width - 540) // 2, (screen_height - 360) // 2)  # Move the second window to the center of the screen
        cv2.setWindowProperty('F2_image', cv2.WND_PROP_TOPMOST, 1)  # Make the second window stay on top of all other applications
        cv2.imshow('F2_image', image_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Save the rectangle data to a file
        with open('rectangle_data.txt', 'w') as f:
            f.write(f'{ix} {iy} {abs(x - ix)} {abs(y - iy)}')

    return ix, iy, abs(x - ix), abs(y - iy)  # Return the rectangle data