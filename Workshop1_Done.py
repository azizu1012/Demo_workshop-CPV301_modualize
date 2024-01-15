import cv2
import math
import pygame
import os
import numpy as np
from PIL import Image
import tkinter as tk
import tempfile
from tkinter import messagebox

# Function 1: Create a white background
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

# Function 2: Draw a rectangle on the image
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
        
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

        # Save the image to the temporary file
        cv2.imwrite(temp_file.name, image_copy)

    return image_copy, ix, iy, abs(x - ix), abs(y - iy)  # Return the image and rectangle

    # return ix, iy, x - ix, y - iy  # Return None to delete the image

#Function 3: Move the rectangle
def move_rectangle(image, rectangle):
    # Initialize the pygame module
    pygame.init()

    # Convert the OpenCV image (BGR) to a Pygame image (RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.rot90(image)
    image = pygame.surfarray.make_surface(image)

    # Get the rectangle coordinates
    x, y, width, height = rectangle

    # Variables for storing the updated rectangle position
    dx, dy = 0, 0

    # Variable for storing the state of the mouse button
    is_dragging = False

    # Callback function for handling mouse events
    def mouse_event(event):
        nonlocal dx, dy, is_dragging, x, y
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Start dragging
            is_dragging = True
            dx, dy = event.pos[0] - x, event.pos[1] - y
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                # Update the rectangle position based on the mouse position
                x, y = event.pos[0] - dx, event.pos[1] - dy
        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging
            is_dragging = False

    # Create a window
    screen = pygame.display.set_mode((image.get_width(), image.get_height()))

    # Set the title of the window
    pygame.display.set_caption("F3_moved")

    # Loop until the user clicks the close button
    done = False

    while not done:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                mouse_event(event)

        # Draw the rectangle at the updated position
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, width, height))

        # Update the display
        pygame.display.flip()

    # Create a temporary file
    temp_fd, temp_file = tempfile.mkstemp(suffix='.jpg')
    os.close(temp_fd)

    # Save the image to the temporary file
    pygame.image.save(screen, temp_file)

    # Quit pygame
    pygame.quit()

#Funtion 4: Rotate the rectangle
def rotate_and_move_rectangle_input(image, rectangle, angle):
    # Get the rectangle's center
    center_x = rectangle[0] + rectangle[2] // 2
    center_y = rectangle[1] + rectangle[3] // 2

    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)

    # Perform the rotation on the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

    # Create a mask of the rectangle
    mask = np.zeros_like(image)
    cv2.rectangle(mask, (rectangle[0], rectangle[1]), (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]), (255, 255, 255), -1)

    # Rotate the mask
    rotated_mask = cv2.warpAffine(mask, rotation_matrix, (image.shape[1], image.shape[0]))

    # Create a white background
    white_background = np.ones_like(image) * 255

    # Apply the mask to the rotated image
    result = np.where(rotated_mask==255, rotated_image, white_background)

    # Display the image
    cv2.imshow('Rotated Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result, rectangle

def rotate_and_move_rectangle_mouse(image, rectangle, angle=None):
    # Get the rectangle coordinates
    x, y, width, height = rectangle

    # Initialize pygame
    pygame.init()

    # Initialize a clock object
    clock = pygame.time.Clock()


    # Initialize angle
    angle = 0

    # Calculate the maximum dimension of the rectangle when rotated
    max_dim = int(np.sqrt(width**2 + height**2))

    # Create a window with the maximum dimension
    screen = pygame.display.set_mode((max_dim, max_dim))

    # Create a surface for the rectangle
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, (0, 0, 0), rect_surface.get_rect())

    # Create a larger surface to contain the rectangle
    larger_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)

    # Calculate the center of the larger surface
    center_x, center_y = max_dim // 2, max_dim // 2

    # Main loop
    done = False
    while not done:
        # Limit the framerate to 60 FPS
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEMOTION:
                # Calculate the angle based on the mouse position relative to the rectangle center
                mx, my = pygame.mouse.get_pos()
                dx, dy = mx - (x + width // 2), my - (y + height // 2)
                angle = -np.arctan2(dy, dx) * 360 / np.pi

        # Fill the screen with white color
        screen.fill((255, 255, 255))

        # Clear the larger surface
        larger_surface.fill((0, 0, 0, 0))

        # Draw the rectangle on the larger surface
        larger_surface.blit(rect_surface, (center_x - width // 2, center_y - height // 2))

        # Rotate the larger surface
        rotated_surface = pygame.transform.rotate(larger_surface, angle)

        # Draw the rotated surface at the center of the screen
        screen.blit(rotated_surface, (center_x - rotated_surface.get_width() // 2, center_y - rotated_surface.get_height() // 2))
        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

    return image, (x, y, width, height)

#Funtion 5: Resize the rectangle
def resize_rectangle_by_percentage(image, rectangle, percentage):
    # Get the rectangle coordinates
    x, y, width, height = rectangle

    # Calculate the new width and height
    new_width = max(1, int(width * (percentage / 100)))  # Ensure new_width is at least 1
    new_height = max(1, int(height * (percentage / 100)))  # Ensure new_height is at least 1

    # Calculate the new x and y coordinates to keep the rectangle centered
    x = max(0, x + (width - new_width) // 2)  # Ensure x is not negative
    y = max(0, y + (height - new_height) // 2)  # Ensure y is not negative

    # Update the rectangle coordinates
    rectangle = (x, y, new_width, new_height)

    # Create a larger background image
    background = np.ones((max(image.shape[0], new_height)*2, max(image.shape[1], new_width)*2, 3), dtype=np.uint8) * 255

    # Calculate the offset to center the resized image on the larger background
    offset_x = (background.shape[1] - new_width) // 2
    offset_y = (background.shape[0] - new_height) // 2

    # Place the resized image onto the larger background
    background[offset_y:offset_y+new_height, offset_x:offset_x+new_width] = image[y:y+new_height, x:x+new_width]

    # Draw the rectangle with the updated size on the larger background
    cv2.rectangle(background, (rectangle[0]+offset_x, rectangle[1]+offset_y), 
                  (rectangle[0]+offset_x + rectangle[2], rectangle[1]+offset_y + rectangle[3]), (0, 0, 0), -1)

    # Display the image
    cv2.namedWindow('Resized Rectangle', cv2.WINDOW_NORMAL)
    cv2.imshow('Resized Rectangle', background)

    # Resize the window and center it on the screen
    screen_width = 800
    screen_height = 600
    cv2.resizeWindow('Resized Rectangle', screen_width, screen_height)
    cv2.moveWindow('Resized Rectangle', screen_width // 2, screen_height // 2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return background, rectangle

def resize_rectangle_by_mouse(image, rectangle):
    pygame.init()

    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the image to Pygame surface
    image_pygame = pygame.image.fromstring(image.tobytes(), image.shape[1::-1], "RGB")

    # Create a display surface
    screen = pygame.display.set_mode(image.shape[1::-1])

    # Create a rectangle
    rect = pygame.Rect(*rectangle)

    # Variables to keep track of which side to resize
    resize_left = False
    resize_right = False
    resize_top = False
    resize_bottom = False

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check which side of the rectangle the mouse is on
                if abs(event.pos[0] - rect.left) < 30:
                    resize_left = True
                elif abs(event.pos[0] - rect.right) < 30:
                    resize_right = True
                if abs(event.pos[1] - rect.top) < 30:  
                    resize_top = True
                elif abs(event.pos[1] - rect.bottom) < 30:
                    resize_bottom = True
            elif event.type == pygame.MOUSEBUTTONUP:
                # Reset all resize flags
                resize_left = resize_right = resize_top = resize_bottom = False
            elif event.type == pygame.MOUSEMOTION:
                # Resize the rectangle based on the mouse position
                if resize_left:
                    rect.width += rect.x - event.pos[0]
                    rect.x = event.pos[0]
                if resize_right:
                    rect.width = event.pos[0] - rect.x
                if resize_top:
                    rect.height += rect.y - event.pos[1]
                    rect.y = event.pos[1]
                if resize_bottom:
                    rect.height = event.pos[1] - rect.y

        # Fill the screen with white
        screen.fill((255, 255, 255))

        # Draw the filled rectangle
        pygame.draw.rect(screen, (0, 0, 0), rect)

        pygame.display.flip()  # Update the display

    pygame.quit()

    return image, (rect.x, rect.y, rect.width, rect.height)

# Menu to run the functions
def main():
    # Menu to run the functions
    image = None
    rectangle = None
    while True:
        print("1. Create a white background")
        print("2. Draw a rectangle on the image")
        print("3. Move the rectangle")  # Always display this option
        print("4. Rotate the rectangle")
        print("5. Resize the rectangle")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            # Create a white background
            image = create_white_background(800, 600)
            print("Image created.")
        elif choice == '2':
            # Draw a rectangle on the image
            if image is None:  # Check if image exists
                print("1. Cancel")
                print("2. Continue without Function 1")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1':
                    continue
                elif sub_choice == '2':
                    image = create_image_without_display(1080, 720)
            image, *rectangle = draw_rectangle_on_image()  # Update the image and rectangle
        elif choice == '3':
            # Move the rectangle
            if rectangle:  # Check if rectangle exists
                image = move_rectangle(image, rectangle)
                print("Press Q to stop & close function")
            else:
                print("Not found Rectangle, roll back to F2 to draw it.")
        elif choice == '4':
            # Rotate the rectangle
            if rectangle:  # Check if rectangle exists
                print("1. Rotate by mouse")
                print("2. Rotate by input angle")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1':
                    image, rectangle = rotate_and_move_rectangle_mouse(image, rectangle)  # Update the image and rectangle
                    print("Press Q to stop & close function")
                elif sub_choice == '2':
                    angle = float(input("Enter the rotation angle (in degrees): "))
                    image, rectangle = rotate_and_move_rectangle_input(image, rectangle, angle)  # Update the image and rectangle
                    print("Press Q to stop & close function")
            else:
                print("Not found Rectangle, roll back to F2 to draw it.")
        elif choice == '5':
            # Resize the rectangle
            if rectangle:  # Check if rectangle exists
                print("1. Resize by mouse")
                print("2. Resize by percentage")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1':
                    image, rectangle = resize_rectangle_by_mouse(image, rectangle)  # Update the image and rectangle
                    print("Press Q to stop & close function")
                elif sub_choice == '2':
                    percentage = int(input("Enter the percentage (100, 200, 300, etc..()): "))
                    image, rectangle = resize_rectangle_by_percentage(image, rectangle, percentage)  # Update the image and rectangle
                    print("Press Q to stop & close function")
            else:
                print("Not found Rectangle, roll back to F2 to draw it.")
        elif choice == '6':
            break

if __name__ == "__main__":
    main()