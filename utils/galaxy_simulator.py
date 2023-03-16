import tkinter as tk
from random import randint, uniform, random
import math
#=============================================================================
# MAIN INPUT   

# scale (radio bubble diameter) in light-years:
SCALE = 225 # enter 225 to see Earth's radio bubble   

# number of advanced civilizations from the Drake equation:
NUM_CIVS = 15600000

#=============================================================================”

# set up display canvas
root = tk.Tk()
root.title("Milky Way galaxy")

c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

# actual Milky Way dimensions (light-years)
DISC_RADIUS = 50000
DISC_HEIGHT = 1000
DISC_VOL = math.pi * DISC_RADIUS**2 * DISC_HEIGHT
