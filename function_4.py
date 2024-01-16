# function_4.py

import cv2
import numpy as np
import pygame
from pygame import surfarray
import os
import tkinter as tk
from tkinter import simpledialog, Label, BOTH, YES
from PIL import Image, ImageTk

def rotate_and_move_rectangle_input(angle):
    # Read the rectangle data from the file
    with open('rectangle_data.txt', 'r') as f:
        x, y, width, height = map(int, f.readline().split())

    # Get the screen resolution
    screen_width = os.get_terminal_size().columns
    screen_height = os.get_terminal_size().lines

    # Calculate the scale factor if the rectangle exceeds the screen size
    scale_factor = min(screen_width / width, screen_height / height, 1)

    # Scale the rectangle dimensions
    width = int(width * scale_factor) // 2
    height = int(height * scale_factor) // 2

    # Calculate the new size of the window
    window_size = max(width, height)

    # Create a white background image with size window_size x window_size
    image = np.ones((window_size, window_size, 3), dtype=np.uint8) * 255

    # Get the rectangle's center
    center_x = window_size // 2
    center_y = window_size // 2

    # Draw the rectangle at the center of the image
    cv2.rectangle(image, (center_x - width // 2, center_y - height // 2), (center_x + width // 2, center_y + height // 2), (0, 0, 0), -1)

    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)

    # Perform the rotation on the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)

    # Perform the rotation on the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

    # Scale the image
    rotated_image = cv2.resize(rotated_image, (0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)

    # Save the image to a file
    cv2.imwrite('rotated_image.png', rotated_image)

    # Convert the image from BGR to RGB
    rotated_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)

    return rotated_image, (center_x - width // 2, center_y - height // 2, width, height)

def rotate_and_move_rectangle_mouse(image_path, rectangle, angle=None):
    # Read the rectangle data from the file
    with open('rectangle_data.txt', 'r') as f:
        x, y, width, height = map(int, f.readline().split())

    # Initialize pygame
    pygame.init()

    # Get the screen resolution
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Calculate the scale factor
    scale_factor = min(screen_width / width, screen_height / height, 1/3)

    # Scale the rectangle dimensions
    width = int(width * scale_factor)
    height = int(height * scale_factor)

    # Calculate the maximum dimension of the rectangle when rotated
    max_dim = max(width, height) * 2

    # Create a window with the same size as the max_dim
    screen = pygame.display.set_mode((max_dim, max_dim))

    # Create a white background image with size max_dim x max_dim
    image = np.ones((max_dim, max_dim, 3), dtype=np.uint8) * 255

    # Create a Pygame surface from the image
    image = pygame.image.fromstring(image.tostring(), (max_dim, max_dim), 'RGB')

    # Initialize a clock object
    clock = pygame.time.Clock()

    # Initialize angle
    angle = 0

    # Create a surface for the rectangle
    rect_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)

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
                dx, dy = mx - max_dim // 2, my - max_dim // 2
                angle = -np.arctan2(dy, dx) * 360 / np.pi

        # Fill the screen with white color
        screen.fill((255, 255, 255))

        # Draw the rectangle on the surface
        rect_surface.fill((255, 255, 255, 0))
        pygame.draw.rect(rect_surface, (0, 0, 0), (max_dim // 2 - width // 2, max_dim // 2 - height // 2, width, height))

        # Rotate the surface
        rotated_surface = pygame.transform.rotate(rect_surface, angle)

        # Draw the rotated surface at the center of the screen
        screen.blit(rotated_surface, (max_dim // 2 - rotated_surface.get_width() // 2, max_dim // 2 - rotated_surface.get_height() // 2))

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

    return image, (x, y, max_dim, max_dim)

SCALE_FACTOR = 10  # Adjust this value to scale the image

class ImageWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.withdraw()  # Hide the window until we are ready to show it
        self.photo = None
        self.label = None

    def display_image(self, image):
        if self.root is not None:
            self.root.destroy()  # Destroy the old window
        self.root = tk.Toplevel()  # Create a new window
        self.photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()
        # Resize the window to fit the image
        self.root.geometry(f"{image.width*SCALE_FACTOR+5}x{image.height*SCALE_FACTOR+5}")
        self.root.deiconify()  # Show the window


    def start(self):
        self.root.mainloop()

def rotate_and_move_rectangle_input_wrapper():
    window = ImageWindow()

    # The rest of your code remains the same
    angle = simpledialog.askfloat("Input", "Enter the angle to rotate the rectangle:", parent=window.root)
    result, rectangle = rotate_and_move_rectangle_input(angle)

    # Convert the result from a NumPy array to a PIL Image
    result_pil = Image.fromarray(result)

    window.display_image(result_pil)
    window.start()  # Start the Tkinter event loop

    return result, rectangle, window

def rotate_and_move_rectangle_mouse_wrapper():
    # Initialize pygame
    pygame.init()

    # Read the rectangle data from the file
    with open('rectangle_data.txt', 'r') as f:
        x, y, width, height = map(int, f.readline().split())
    rectangle = (x, y, width, height)

    # Define the image path here
    image_path = 'path_to_your_image.png'  # replace with your image path

    # Define the initial angle here
    angle = 0  # replace with your desired initial angle

    rotate_and_move_rectangle_mouse(image_path, rectangle, angle)