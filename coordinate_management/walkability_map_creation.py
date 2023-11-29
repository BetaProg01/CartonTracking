# Imports
from PIL import Image
import numpy as np

################################################################

# Load the image
image = Image.open("images/Middle_Earth_Map_colored.png")
image_array = np.array(image)

# Removing alpha canal
image_array = image_array[:, :, :3]

# Define non-walkable color
NON_WALKABLE_COLOR = np.array([255, 0, 0])

# Create boolean arrays for walkable or non-walkable
walkable_array = np.all(image_array != NON_WALKABLE_COLOR, axis=-1)

# Save map_array to a file using numpy
np.save("walkability_array.npy", walkable_array)