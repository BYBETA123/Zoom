from PIL import Image, ImageTk
import tkinter as tk
import mss
import ctypes

FPS = 240  # Frames per second for screen capture
BOX_CONSTANT = 200  # Adjust to set the size of the box around the cursor

V_BOX_CONSTANT = 200
V_BOX_ORIGINAL = 200
H_BOX_CONSTANT = 200
H_BOX_ORIGINAL = 200

RATIO_CONSTANT = 0.5  # Adjust to resize the displayed image
#inital setups
currentx = 0
currenty = 0
currentcolor = (0, 0, 0)


# Struct to store cursor position
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_position():
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    hdc = ctypes.windll.user32.GetDC(0)
    color = ctypes.windll.gdi32.GetPixel(hdc, cursor.x, cursor.y)
    ctypes.windll.user32.ReleaseDC(0, hdc)
    color = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff) # Convert to RGB
    return cursor.x, cursor.y, color

# Function to capture the screen across multiple monitors
def capture_screen():
    global BOX_CONSTANT

    # Initialize mss
    with mss.mss() as sct:
        global currentx, currenty, currentcolor
        x, y, currentcolor = get_mouse_position()
        currentx, currenty= x, y
        #set the box around the cursor
        bbox_mouse = (x - H_BOX_CONSTANT, y - V_BOX_CONSTANT, x + H_BOX_CONSTANT, y + V_BOX_CONSTANT)

        screenshot = sct.grab(bbox_mouse)


        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
    return img

def getHex(color):
    #Return the hex value with capital lettesr
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

# Function to update the displayed image in a tkinter window
def update_image(label, rinfo2, rinfo3, rinfo4):
    global RATIO_CONSTANT
    # Capture the screen across all monitors
    img = capture_screen()
    
    # Resize for display if necessary (adjust dimensions)
    img_resized = img.resize((400, 400))  # This is to make sure the image fits in the window
    img_tk = ImageTk.PhotoImage(img_resized)
    
    # Update the label widget with the new image
    label.configure(image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    global currentx, currenty, currentcolor
    rinfo2.configure(text = f"X: {currentx} Y: {currenty}")
    rinfo3.configure(text = f"Color: {currentcolor}")
    rinfo4.configure(text = f"Hex Code: {getHex(currentcolor)}")


    # Schedule the next update
    global FPS
    label.after((1000//FPS), update_image, label, rinfo2, rinfo3, rinfo4)  # Update every second (1000 ms)

def update_zoom_slider(event, z):
    global V_BOX_CONSTANT, H_BOX_CONSTANT, V_BOX_ORIGINAL, H_BOX_ORIGINAL
    #Assign the new constnat
    V_BOX_CONSTANT = int(V_BOX_ORIGINAL * 1/z.get())
    H_BOX_CONSTANT = int(H_BOX_ORIGINAL * 1/z.get())
    #fix the constants to the upper limmits of the
    return

def update_horizontal_slider(event, h, z):
    global H_BOX_CONSTANT, H_BOX_ORIGINAL
    #Assign the new constnat
    H_BOX_ORIGINAL = h.get()
    H_BOX_CONSTANT = int(h.get() * 1/z.get())
    return


def update_vertical_slider(event, v, z):
    global V_BOX_CONSTANT, V_BOX_ORIGINAL
    #Assign the new constnat
    V_BOX_ORIGINAL = v.get()
    V_BOX_CONSTANT = int(v.get() * 1/z.get())
    return

if __name__ == "__main__":

    # Set up the tkinter window
    root = tk.Tk()
    root.title("I'm too blind to see this")


    lFrame = tk.Frame(root)
    lFrame.pack(side = tk.LEFT)
    rFrame = tk.Frame(root)
    rFrame.pack(side = tk.RIGHT)
    # Initial capture of all screens
    initial_img = capture_screen()

    # Resize the initial image for display
    initial_img_resized = initial_img.resize((400, 400))  # Adjust as needed
    img_tk = ImageTk.PhotoImage(initial_img_resized)

    # Create a label to display the image
    label = tk.Label(lFrame, image=img_tk)
    label.image = img_tk
    label.pack()


    rlabel = tk.Label(rFrame, text = "Zoom Scale")
    rlabel.pack()


    rZoom = tk.Scale(rFrame, from_ = 1, to=10, orient = tk.HORIZONTAL, resolution = 0.1)
    rZoom.set(1) #Set the default value
    rZoom.bind("<ButtonRelease-1>", lambda event: update_zoom_slider(event, rZoom))
    rZoom.pack()

    rHBox = tk.Scale(rFrame, from_ = 10, to=500, orient = tk.HORIZONTAL, resolution = 10)
    rHBox.set(200) #Set the default value
    rHBox.bind("<ButtonRelease-1>", lambda event: update_horizontal_slider(event, rHBox, rZoom))
    rHBox.pack()

    rVBox = tk.Scale(rFrame, from_ = 10, to=500, orient = tk.HORIZONTAL, resolution = 10)
    rVBox.set(200) #Set the default value
    rVBox.bind("<ButtonRelease-1>", lambda event: update_vertical_slider(event, rVBox, rZoom))
    rVBox.pack()

    rinfo2 = tk.Label(rFrame, text = f"X: {currentx} Y: {currenty}", width = 20)
    rinfo2.pack()

    rinfo3 = tk.Label(rFrame, text = currentcolor, width = 20)
    rinfo3.pack()

    rinfo4 = tk.Label(rFrame, text = f"Hex Code: {getHex(currentcolor)}", width = 20)
    rinfo4.pack()

    # Start the periodic update
    update_image(label, rinfo2, rinfo3, rinfo4) # For the area around the cursor

    # Run the tkinter event loop
    root.mainloop()