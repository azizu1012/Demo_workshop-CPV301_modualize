# function_4.py

import cv2
import numpy as np
import pygame

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

    # Save the image to a file
    cv2.imwrite('rotated_image.png', result)

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
    max_dim = max(width, height) * 2

    # Create a window with the maximum dimension
    screen = pygame.display.set_mode((max_dim, max_dim))

    # Create a surface for the rectangle
    rect_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, (0, 0, 0), (x, y, width, height))

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

        # Draw the rectangle on the surface
        rect_surface.fill((255, 255, 255, 0))
        pygame.draw.rect(rect_surface, (0, 0, 0), (x, y, width, height))

        # Rotate the surface
        rotated_surface = pygame.transform.rotate(rect_surface, angle)

        # Draw the rotated surface at the center of the screen
        screen.blit(rotated_surface, (max_dim // 2 - rotated_surface.get_width() // 2, max_dim // 2 - rotated_surface.get_height() // 2))

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

    return image, (x, y, max_dim, max_dim)

def read_rectangle_info_from_file(file_path):
    with open(file_path, 'r') as file:
        ix, iy, width, height = map(int, file.readline().split())
    return ix, iy, width, height

def rotate_and_move_rectangle_input_wrapper():
    # Define some predefined arguments
    image = cv2.imread('image.png')  # replace 'image.png' with your actual image file
    rectangle = read_rectangle_info_from_file('rectangle_data.txt')  # replace with your actual rectangle file
    angle = 45  # replace with your actual angle

    # Call the original function with the predefined arguments
    return rotate_and_move_rectangle_input(image, rectangle, angle)

def rotate_and_move_rectangle_mouse_wrapper():
    # Define some predefined arguments
    image = cv2.imread('image.png')  # replace 'image.png' with your actual image file
    rectangle = read_rectangle_info_from_file('rectangle_data.txt')  # replace with your actual rectangle file

    # Call the original function with the predefined arguments
    return rotate_and_move_rectangle_mouse(image, rectangle)