import pygame
import numpy as np
import os

# Function 3: Move the rectangle
def move_rectangle():
    # Read the rectangle data from 'rectangle_data.txt'
    with open('rectangle_data.txt', 'r') as f:
        x, y, width, height = map(int, f.readline().split())

    # Create a white background image with size 800x600
    image = np.ones((600, 800, 3), dtype=np.uint8) * 255

    # Create a Pygame surface from the image
    image = pygame.image.fromstring(image.tostring(), (800, 600), 'RGB')

    # Create a window with the same size as the image
    screen = pygame.display.set_mode((800, 600))

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
        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, width, height))

        # Update the display
        pygame.display.flip()

    # Save the image to 'image_change_copy.jpg'
    pygame.image.save(screen, 'image_change_copy.jpg')

    # Quit pygame
    pygame.quit()