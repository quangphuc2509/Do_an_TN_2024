import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from detection_line_2 import *

class ImageResizerApp:
    def __init__(self, root, image, x, y):
        self.root = root
        
        # Load image using OpenCV
        self.cv_image = image
        self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
        self.image_height, self.image_width = self.cv_image.shape[:2]

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=350, height=500, bg='white')
        self.canvas.place(x=x, y = y)

        # Convert image to PIL format
        self.image = Image.fromarray(self.cv_image)
        self.photo = ImageTk.PhotoImage(self.image)

        # Display the image on the canvas
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Bind mouse events to functions
        self.canvas.bind("<MouseWheel>", self.resize_image)
        self.canvas.bind("<Motion>", self.update_mouse_position)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_image)
        self.canvas.bind("<Button-3>", self.show_coordinates)

        # Initial state variables
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.pan_start_x = 0
        self.pan_start_y = 0
        
        # Create a track bar (Scale) to adjust image scale
        self.scale_var = tk.DoubleVar(value=1.0)
        self.scale_bar = tk.Scale(root, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, label="Scale", 
                                  variable=self.scale_var, command=self.update_scale, width=15, length=200)
        self.scale_bar.place(x=x, y=y+520)

    def update_mouse_position(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def pan_image(self, event):
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.offset_x = min(max(self.offset_x - dx, 0), int(self.image_width * self.scale) - self.canvas.winfo_width())
        self.offset_y = min(max(self.offset_y - dy, 0), int(self.image_height * self.scale) - self.canvas.winfo_height())
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.redraw_image()

    def resize_image(self, event):
        # Change scale factor based on scroll direction
        if event.delta > 0:
            self.scale += 0.05
        else:
            self.scale -= 0.05

        # Ensure scale is within bounds
        self.scale = max(0.1, min(self.scale, 10.0))

        # Adjust offsets to keep image centered
        self.offset_x = 0
        self.offset_y = 0

        # Redraw the image with new scale
        self.redraw_image()
    
    def update_scale(self, value):
        self.scale = float(value)
        self.offset_x = 0
        self.offset_y = 0
        self.redraw_image()

    def redraw_image(self):
        # Calculate new dimensions
        new_width = int(self.image_width * self.scale)
        new_height = int(self.image_height * self.scale)

        # Resize the image
        resized_cv_image = cv2.resize(self.cv_image, (new_width, new_height))

        # Calculate the region to display based on current offsets
        end_x = min(self.offset_x + self.canvas.winfo_width(), new_width)
        end_y = min(self.offset_y + self.canvas.winfo_height(), new_height)
        cropped_cv_image = resized_cv_image[self.offset_y:end_y, self.offset_x:end_x]

        # Convert resized and cropped image to PIL format and update the canvas
        resized_image = Image.fromarray(cropped_cv_image)
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def show_coordinates(self, event):
        # Calculate the actual coordinates on the original image
        actual_x = int((self.offset_x + event.x) / self.scale)
        actual_y = int((self.offset_y + event.y) / self.scale)
        print(f"Mouse coordinates on image: ({actual_x}, {actual_y})")
        
class main_GUI(Detection_line):
    def __init__(self, root, image):
        super().__init__(image)
        self.root = root
        self.image = image
        
        self.app1 = ImageResizerApp(self.root, self.image, x=50, y=10)
        self.app2 = ImageResizerApp(self.root, self.edges_image, x=410, y=10)
        self.app3 = ImageResizerApp(self.root, self.curves_image, x=780, y=10)
        self.app4 = ImageResizerApp(self.root, self.image, x=1140, y=10)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Resizer with Fixed Frame")
    root.state('zoomed')
    
    url = r"F:\DATN_HK2_2024\camera_img\line15.jpg"
    image = cv2.imread(url)
    main_GUI(root, image)
    root.mainloop()
