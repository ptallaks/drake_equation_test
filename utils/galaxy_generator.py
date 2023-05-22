import argparse
import math
import random
from tkinter import Tk, Canvas
from tkinter.ttk import Combobox
from tkinter.font import Font


# actual Milky Way dimensions (light-years)
DISC_RADIUS = 50000
DISC_HEIGHT = 1000
DISC_VOL = math.pi * DISC_RADIUS**2 * DISC_HEIGHT

@interact(scale=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0),
          num_civs=IntSlider(min=1000, max=1000000, step=1000, value=10000))

def scale_galaxy(scale):
    """Scale galaxy dimensions based on radio bubble size (scale)."""
    disc_radius_scaled = round(DISC_RADIUS / scale)
    bubble_vol = 4/3 * math.pi * (scale / 2)**3
    disc_vol_scaled = DISC_VOL / bubble_vol
    return disc_radius_scaled, disc_vol_scaled


def random_polar_coordinates(disc_radius_scaled):
    """Generate uniform random (x, y) point within a disc for 2D display."""
    r = random.random()
    theta = random.uniform(0, 2 * math.pi)
    x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
    y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
    return x, y


def generate_galaxy(scale, num_civs):
    """Generate galaxy based on user inputs."""
    # set up display canvas
    root = Tk()
    root.title("Milky Way galaxy")

    c = Canvas(root, width=1000, height=800, bg='black')
    c.pack()
    c.configure(scrollregion=(-500, -400, 500, 400))

    disc_radius_scaled, disc_vol_scaled = scale_galaxy(scale)

    # other code to generate galaxy display goes here...

    root.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Galaxy Generator')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor for radio bubble size')
    parser.add_argument('--num_civs', type=int, default=10000, help='Number of civilizations')
    args = parser.parse_args()

    generate_galaxy(args.scale, args.num_civs)
