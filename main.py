import tkinter as tk
from PIL import Image, ImageTk

# Set up the main window
root = tk.Tk()
root.title("Space Invaders")
root.resizable(False, False)
root.geometry("800x600")

# Create the canvas for the game
canvas = tk.Canvas(root, width=800, height=600, bg="black")
canvas.pack()

# Load the spaceship image
spaceship_image = Image.open(
    r"C:\Users\Siris\Desktop\GitHub Projects 100 Days NewB\_24_0099__Day95_Pro_Portfolio_Project_Alien_Invaders__241001\NewProject\r00_env_START\r07\spaceship.png")
spaceship_image = spaceship_image.resize((40, 40), Image.Resampling.LANCZOS)  # Resize image to fit
spaceship_photo = ImageTk.PhotoImage(spaceship_image)

# Spaceship properties
spaceship_x = 380  # starting x position of the spaceship
spaceship_y = 550  # fixed y position (near the bottom of the window)
spaceship_speed = 20

# Create the spaceship using the image
spaceship = canvas.create_image(spaceship_x, spaceship_y, image=spaceship_photo, anchor="nw")

# Variable to keep track of the active bullet
active_bullet = None

# List to keep track of barriers and their pixel positions
barriers = []

# Function to move the spaceship left
def move_left(event):
    x1, y1 = canvas.coords(spaceship)
    if x1 > 0:
        canvas.move(spaceship, -spaceship_speed, 0)

# Function to move the spaceship right
def move_right(event):
    x1, y1 = canvas.coords(spaceship)
    if x1 < 760:  # Make sure spaceship doesn't move past the right edge of the screen
        canvas.move(spaceship, spaceship_speed, 0)

# Function to fire a bullet (only one active bullet at a time)
def fire_bullet(event):
    global active_bullet
    # If there's already an active bullet, do nothing
    if active_bullet is not None:
        return

    # Create a new bullet
    x1, y1 = canvas.coords(spaceship)
    bullet = canvas.create_rectangle(x1 + 20 - 2, y1 - 10, x1 + 20 + 2, y1, fill="red")
    active_bullet = bullet
    move_bullet()

# Function to check if a bullet hits a barrier and remove the pixel
def check_collision_and_chip():
    global active_bullet

    if active_bullet is None:
        return

    bullet_coords = canvas.coords(active_bullet)
    bullet_x = bullet_coords[0] + 2  # Center of the bullet
    bullet_y = bullet_coords[1]

    # Check each barrier (each pixel block)
    for barrier_item in barriers:
        pixel_x, pixel_y, pixel_rectangle = barrier_item
        if pixel_x <= bullet_x <= pixel_x + 5 and pixel_y <= bullet_y <= pixel_y + 5:
            # Delete the pixel from the canvas
            canvas.delete(pixel_rectangle)
            barriers.remove(barrier_item)  # Remove the pixel from the barriers list

            # Remove the bullet after collision
            canvas.delete(active_bullet)
            active_bullet = None
            return

# Function to move the active bullet
def move_bullet():
    global active_bullet
    if active_bullet is not None:
        # Check if the active_bullet still exists before getting its coordinates
        try:
            bullet_coords = canvas.coords(active_bullet)
        except tk.TclError:
            return  # The bullet has been deleted, so we stop here

        canvas.move(active_bullet, 0, -10)
        check_collision_and_chip()  # Check for collision with barriers

        # If the bullet goes off-screen, remove it
        if bullet_coords[1] < 0:
            canvas.delete(active_bullet)
            active_bullet = None  # Reset the active bullet variable

    # Continue moving the bullet until it goes off-screen or is deleted
    if active_bullet is not None:
        root.after(50, move_bullet)

# Function to create barriers manually (pixel blocks)
def create_barriers():
    barrier_y = spaceship_y - 150  # 150 pixels above the spaceship
    barrier_spacing = 160  # Evenly space the barriers horizontally
    pixel_size = 5  # Each pixel block will be 5x5 on the canvas

    # Shape of the barrier represented as a grid (1 = solid, 0 = empty)
    barrier_shape = [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    ]

    for i in range(4):  # Create four barriers
        barrier_x = 130 + i * barrier_spacing  # Shifted 20 pixels to the left from previous position

        # Create the barrier block by block using the shape
        for row in range(len(barrier_shape)):
            for col in range(len(barrier_shape[0])):
                if barrier_shape[row][col] == 1:
                    pixel_rectangle = canvas.create_rectangle(
                        barrier_x + col * pixel_size, barrier_y + row * pixel_size,
                        barrier_x + (col + 1) * pixel_size, barrier_y + (row + 1) * pixel_size,
                        fill="green", outline=""
                    )
                    barriers.append([barrier_x + col * pixel_size, barrier_y + row * pixel_size, pixel_rectangle])

# Create barriers on the screen
create_barriers()

# Bind key events to spaceship movement and firing
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<space>", fire_bullet)

# Start the game loop
root.mainloop()
