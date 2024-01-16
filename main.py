# main.py

from PIL import Image, ImageTk
import shutil
import tempfile
import os
from os import remove
from tkinter import Tk, Button, Label, Frame, PhotoImage, Entry, Menu, Menubutton
from tkinter.filedialog import askopenfilename
from funtion_1 import create_white_background
from funtion_2 import create_image_without_display, draw_rectangle_on_image
from funtion_3 import move_rectangle
from function_4 import rotate_and_move_rectangle_input, rotate_and_move_rectangle_mouse, rotate_and_move_rectangle_input_wrapper, rotate_and_move_rectangle_mouse_wrapper
from funtion_5 import resize_rectangle_by_percentage_wrapper, resize_rectangle_by_mouse_wrapper, resize_rectangle_by_percentage, resize_rectangle_by_mouse

def main():
    root = Tk()
    root.geometry("780x460")  # Set the window size
    root.title("Image Processing")  # Set the window title

    # Use the dimensions from root.geometry()
    screen_width = 780
    screen_height = 460

    def load_bg_image():
        bg_image_path = askopenfilename(filetypes=[("Image files", "*.jpg *.png")])  # Open a file dialog for the user to select an image file
        if bg_image_path:
            image = Image.open(bg_image_path)
            image = image.resize((screen_width, screen_height), Image.LANCZOS)  # Resize the image
            root.bg_image = ImageTk.PhotoImage(image)  # Store the ImageTk.PhotoImage object as an attribute of root
            bg_label = Label(root, image=root.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set the label size to the window size
            root.lift_buttons()  # Lift the buttons above the background image

    load_bg_button = Button(root, text="Load Background Image", command=load_bg_image)
    load_bg_button.pack()

    frame = Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame
    # Store the frame in a root attribute so it can be accessed later
    root.buttons_frame = frame

    # Add a method to root to lift the buttons above the background image
    def lift_buttons(self):
        self.buttons_frame.lift()

    root.lift_buttons = lift_buttons.__get__(root, Tk)

    button1 = Button(frame, text="Create a white background", command=lambda: create_white_background(1080, 720), highlightthickness=0, bd=1)
    button1.pack()

    button2 = Button(frame, text="Draw a rectangle on an image", command=draw_rectangle_on_image, highlightthickness=0, bd=1)
    button2.pack()

    button3 = Button(frame, text="Move a rectangle on an image", command=move_rectangle, highlightthickness=0, bd=1)
    button3.pack()

    # Create a menubutton
    button4 = Menubutton(frame, text="Rotate Image", relief="raised")
    button4.pack()

    # Create a menu
    function_4_menu = Menu(button4, tearoff=0)
    button4.config(menu=function_4_menu)

    # Create a submenu
    rotate_submenu = Menu(function_4_menu, tearoff=0)

    # Add commands to the submenu
    rotate_submenu.add_command(label="By Input", command=rotate_and_move_rectangle_input_wrapper)
    rotate_submenu.add_command(label="By Mouse", command=rotate_and_move_rectangle_mouse_wrapper)

    # Add the submenu to the main menu
    function_4_menu.add_cascade(label="Rotate", menu=rotate_submenu)

    # Add a new button for clearing the rectangle data file
    def clear_rectangle_data():
        if os.path.exists('rectangle_data.txt'):
            remove('rectangle_data.txt')

    # Create a menubutton for function_5
    button5 = Menubutton(frame, text="Resize Rectangle", relief="raised")
    button5.pack()

    # Create a menu for function_5
    function_5_menu = Menu(button5, tearoff=0)
    button5.config(menu=function_5_menu)

    # Add commands to the function_5 menu
    function_5_menu.add_command(label="By Percentage", command=resize_rectangle_by_percentage_wrapper)
    function_5_menu.add_command(label="By Mouse", command=resize_rectangle_by_mouse_wrapper)

    button_clear = Button(frame, text="Clear data of rectangle", command=clear_rectangle_data, highlightthickness=0, bd=1)
    button_clear.pack()

    # Call 'clear_rectangle_data' when the window is closed
    def on_close():
        clear_rectangle_data()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    main()