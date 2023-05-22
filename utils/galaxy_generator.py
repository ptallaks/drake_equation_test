import tkinter as tk
from random import randint, uniform, random
import math
import ipywidgets as widgets
from IPython.display import display
from PIL import ImageGrab
import ipywidgets as widgets
from IPython.display import clear_output

def generate_galaxy(num_civs, scale):
    # Set up display canvas
    root = tk.Tk()
    root.title("Milky Way galaxy")

    c = tk.Canvas(root, width=1000, height=800, bg='black')
    c.grid()
    c.configure(scrollregion=(-500, -400, 500, 400))

    # Actual Milky Way dimensions (light-years)
    DISC_RADIUS = 50000
    DISC_HEIGHT = 1000
    DISC_VOL = math.pi * DISC_RADIUS**2 * DISC_HEIGHT

    def scale_galaxy():
        """Scale galaxy dimensions based on radio bubble size (scale)."""
        disc_radius_scaled = round(DISC_RADIUS / scale)
        bubble_vol = 4/3 * math.pi * (scale / 2)**3
        disc_vol_scaled = DISC_VOL / bubble_vol
        return disc_radius_scaled, disc_vol_scaled

    def detect_prob(disc_vol_scaled):
        """Calculate probability of galactic civilizations detecting each other."""
        ratio = num_civs / disc_vol_scaled  # ratio of civs to scaled galaxy volume
        if ratio < 0.002:  # set very low ratios to probability of 0
            detection_prob = 0
        elif ratio >= 5:  # set high ratios to probability of 1
            detection_prob = 1
        else:
            detection_prob = -0.004757 * ratio**4 + 0.06681 * ratio**3 - 0.3605 * ratio**2 + 0.9215 * ratio + 0.00826
        return round(detection_prob, 3)

    def random_polar_coordinates(disc_radius_scaled):
        """Generate uniform random (x, y) point within a disc for 2D display."""
        r = random()
        theta = uniform(0, 2 * math.pi)
        x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
        y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
        return x, y

    def spirals(b, r, rot_fac, fuz_fac, arm):
        """Build spiral arms for tkinter display using logarithmic spiral formula."""
        spiral_stars = []
        fuzz = int(0.030 * abs(r))  # randomly shift star locations
        theta_max_degrees = 520
        for i in range(theta_max_degrees):
            theta = math.radians(i)
            x = r * math.exp(b * theta) * math.cos(theta + math.pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
            y = r * math.exp(b * theta) * math.sin(theta + math.pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
            spiral_stars.append((x, y))
        for x, y in spiral_stars:
            if arm == 0 and int(x % 2) == 0:
                c.create_oval(x - 2, y - 2, x + 2, y + 2, fill='white', outline='')
            elif arm == 0 and int(x % 2) != 0:
                c.create_oval(x - 1, y - 1, x + 1, y + 1, fill='white', outline='')
            elif arm == 1:
                c.create_oval(x, y, x, y, fill='white', outline='')

    def star_haze(disc_radius_scaled, density):
        """Randomly distribute faint tkinter stars in galactic disc."""
        for i in range(0, disc_radius_scaled * density):
            x, y = random_polar_coordinates(disc_radius_scaled)
            c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')

    def main():
        """Calculate detection probability & post galaxy display & statistics."""
        disc_radius_scaled, disc_vol_scaled = scale_galaxy()
        detection_prob = detect_prob(disc_vol_scaled)
        # build 4 main spiral arms & 4 trailing arms
        spirals(b=-0.3, r=disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
        spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1.5, arm=1)
        spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
        spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-2.09, fuz_fac=1.5, arm=1)
        spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
        spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)
        spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
        spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
        star_haze(disc_radius_scaled, density=8)

        # Display legend
        c.create_text(-455, -360, fill='white', anchor='w',
                      text='One Pixel = {} LY'.format(scale))
        c.create_text(-455, -330, fill='white', anchor='w',
                      text='Radio Bubble Diameter = {} LY'.format(scale))
        c.create_text(-455, -300, fill='white', anchor='w',
                      text='Probability of detection for {:,} civilizations = {}'.format(num_civs, detection_prob))

        # Post Earth's 225 LY diameter bubble and annotate
        c.create_rectangle(115, 75, 116, 76, fill='red', outline='')
        c.create_text(118, 72, fill='red', anchor='w', text="<---------- Earth's Radio Bubble")


        # Run tkinter loop
        root.mainloop()

    main()

    # Capture the Tkinter canvas as an image
    image = ImageGrab.grab(bbox=(root.winfo_x(), root.winfo_y(), root.winfo_x() + root.winfo_width(), root.winfo_y() + root.winfo_height()))

    # Display the image in the Jupyter notebook cell
    display(image)

# Create interactive widgets
num_civs_slider = widgets.IntSlider(value=15600000, min=0, max=1000000000, step=1000000, description='Number of Civilizations:')
scale_slider = widgets.IntSlider(value=225, min=1, max=5000, step=10, description='Scale:')

def on_generate_button_clicked(b):
    clear_output()
    generate_galaxy(num_civs_slider.value, scale_slider.value)

generate_button = widgets.Button(description='Generate Galaxy')
generate_button.on_click(on_generate_button_clicked)

# Display the widgets and initial galaxy
display(num_civs_slider, scale_slider, generate_button)
generate_galaxy(num_civs_slider.value, scale_slider.value)