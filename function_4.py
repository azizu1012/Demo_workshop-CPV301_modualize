# function_4.py

import cv2
import numpy as np
import pygame
from pygame import surfarray
import os
import tkinter as tk
from tkinter import simpledialog, Label, BOTH, YES
from PIL import Image, ImageTk

def rotate_and_move_rectangle_input(angle, screen_limit=1000):
    # Read the rectangle data from the file
    with open('rectangle_data.txt', 'r') as f:
        x, y, width, height = map(int, f.readline().split())

    # Create a black rectangle image with size width x height and an alpha channel
    rectangle = np.zeros((height, width, 4), dtype=np.uint8)
    rectangle[:, :, :3] = 0  # Set BGR channels to 0 (black)
    rectangle[:, :, 3] = 255  # Set alpha channel to 255 (fully opaque)

    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)

    # Perform the rotation on the rectangle for the BGR channels
    rotated_rectangle = cv2.warpAffine(rectangle[:, :, :3], rotation_matrix, (width, height))

    # Create a rotated alpha channel
    rotated_alpha = cv2.warpAffine(rectangle[:, :, 3], rotation_matrix, (width, height))

    # Combine the rotated BGR channels and the rotated alpha channel
    rotated_rectangle = cv2.merge([rotated_rectangle, rotated_alpha])

    # Calculate the new size of the window
    window_size = max(rotated_rectangle.shape[0], rotated_rectangle.shape[1])

    # Create a white background image with size window_size x window_size
    background = np.ones((window_size, window_size, 4), dtype=np.uint8) * 255
    background[:, :, 3] = 255  # Set alpha channel to 255 (fully opaque)

    # Calculate the position to paste the rotated rectangle onto the background
    start_x = (window_size - rotated_rectangle.shape[1]) // 2
    start_y = (window_size - rotated_rectangle.shape[0]) // 2

    # Paste the rotated rectangle onto the background
    background[start_y:start_y+rotated_rectangle.shape[0], start_x:start_x+rotated_rectangle.shape[1]] = rotated_rectangle

    # Convert the image from BGR to RGB
    result = cv2.cvtColor(background, cv2.COLOR_BGRA2RGBA)

    # Save the result to a temporary file
    Image.fromarray(result).save('temp.png')

    return result, (start_x, start_y, rotated_rectangle.shape[1], rotated_rectangle.shape[0])


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
        self.label.pack()  # Allow the label to expand to fill the window
        # Resize the window to fit the image
        self.root.geometry(f"{self.photo.width()}x{self.photo.height()}")
        self.root.deiconify()  # Show the window

    def start(self):
        self.root.mainloop()

def rotate_and_move_rectangle_input_wrapper():
    window = ImageWindow()

    # Ask the user for the rotation angle
    angle = simpledialog.askfloat("Input", "Enter the angle to rotate the rectangle:", parent=window.root)

    # Rotate the rectangle and get the result
    result, rectangle = rotate_and_move_rectangle_input(angle)

    # Save the result to a temporary file
    cv2.imwrite('temp.png', result)

    # Read the temporary file to ensure it can be read
    temp = cv2.imread('temp.png')

    # Convert the result from a NumPy array to a PIL Image
    result_pil = Image.fromarray(result)

    # Display the image
    window.display_image(result_pil)

    # Start the Tkinter event loop
    window.start()

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