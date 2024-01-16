#funtion 5
import cv2
import pygame
import os
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog


def resize_rectangle_by_percentage(image_file, rectangle_file, percentage):
    # Read the image
    image = cv2.imread(image_file)

    # Read the rectangle data from the file
    with open(rectangle_file, 'r') as f:
        rectangle = tuple(map(int, f.read().split()))

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

def resize_rectangle_by_mouse(image_file, rectangle_file):
    pygame.init()

    # Read the image
    image = cv2.imread(image_file)

    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the image to Pygame surface
    image_pygame = pygame.image.fromstring(image.tobytes(), image.shape[1::-1], "RGB")

    # Create a display surface
    screen = pygame.display.set_mode(image.shape[1::-1])

    # Read the rectangle data from the file
    with open(rectangle_file, 'r') as f:
        rectangle = tuple(map(int, f.read().split()))

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

def read_rectangle_info_from_file(file_path):
    with open(file_path, 'r') as file:
        ix, iy, width, height = map(int, file.readline().split())
    return ix, iy, width, height

# def resize_rectangle_by_percentage_wrapper():
#     # Define some predefined arguments
#     image = cv2.imread('image.png')  # replace 'image.png' with your actual image file
#     rectangle = read_rectangle_info_from_file('rectangle_data.txt')  # replace with your actual rectangle file
#     percentage = simpledialog.askinteger("Input", "What percentage do you want to resize the rectangle to?", parent=np.roots)

#     # Call the original function with the predefined arguments
#     if percentage:
#         return resize_rectangle_by_percentage(image, rectangle, percentage)

# def resize_rectangle_by_mouse_wrapper():
#     # Define some predefined arguments
#     image = cv2.imread('image.png')  # replace 'image.png' with your actual image file
#     rectangle = read_rectangle_info_from_file('rectangle_data.txt')  # replace with your actual rectangle file

#     # Call the original function with the predefined arguments
#     return resize_rectangle_by_mouse(image, rectangle)

def draw_rectangle_and_save(rectangle, temp_file_path, image_size=(500, 500, 3)):
    # Create a white image
    image = np.ones(image_size, dtype=np.uint8) * 255

    # Draw the rectangle on the image
    cv2.rectangle(image, (rectangle[0], rectangle[1]), (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]), (0, 255, 0), 2)

    # Save the image to a temporary file
    cv2.imwrite(temp_file_path, image)

def resize_rectangle_by_percentage_wrapper():
    # Define some predefined arguments
    rectangle_data_path = 'rectangle_data.txt'  # replace with your actual rectangle file
    temp_file_path = 'temp_image.png'  # replace with your actual temporary file
    percentage = 45  # replace with your actual percentage

    rectangle = read_rectangle_info_from_file(rectangle_data_path)
    if rectangle is None:
        raise FileNotFoundError(f"The rectangle data file '{rectangle_data_path}' was not found.")

    draw_rectangle_and_save(rectangle, temp_file_path)

    image = cv2.imread(temp_file_path)
    if image is None:
        raise FileNotFoundError(f"The temporary image file '{temp_file_path}' was not found.")

    # Call the original function with the predefined arguments
    return resize_rectangle_by_percentage(image, rectangle, percentage)

def resize_rectangle_by_mouse_wrapper():
    # Define some predefined arguments
    rectangle_data_path = 'rectangle_data.txt'  # replace with your actual rectangle file
    temp_file_path = 'temp_image.png'  # replace with your actual temporary file

    rectangle = read_rectangle_info_from_file(rectangle_data_path)
    if rectangle is None:
        raise FileNotFoundError(f"The rectangle data file '{rectangle_data_path}' was not found.")

    draw_rectangle_and_save(rectangle, temp_file_path)

    image = cv2.imread(temp_file_path)
    if image is None:
        raise FileNotFoundError(f"The temporary image file '{temp_file_path}' was not found.")

    # Call the original function with the predefined arguments
    return resize_rectangle_by_mouse(image, rectangle)