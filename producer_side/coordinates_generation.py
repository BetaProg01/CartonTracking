import numpy as np
import random as rd
from datetime import datetime, timedelta


# Set constants
PIXEL_PER_HOUR = 16
ANGLE_ADJUSTMENT = 40  #degre

# Load the map
map_annoted = np.load("walkability_array.npy")

# Set map size variables
map_height = len(map_annoted)
map_width = len(map_annoted[0])


########################################################################################## SPAWN 

# Gives random walkable spawn point
def random_spawn ():
    spawn_point_found = False
    
    while not spawn_point_found :
        y_pos = rd.randint(0, map_height-1)
        x_pos = rd.randint(0, map_width-1)

        spawn_point_found = map_annoted[y_pos][x_pos]
    
    return x_pos, y_pos


########################################################################################## MOVEMENT

# Calculate new position from angle
def move (x_pos, y_pos, angle_deg):
    angle_rad = np.radians(angle_deg)
    new_x = int(x_pos + PIXEL_PER_HOUR * np.cos(angle_rad))
    new_y = int(y_pos + PIXEL_PER_HOUR * np.sin(angle_rad))
    
    return new_x, new_y



def x_in_boundaries(x_pos):
    return x_pos >= 0 and x_pos < map_width

def y_in_boundaries (y_pos):
    return y_pos >= 0 and y_pos < map_height



# First vector generation
def generate_initial_vector(x_pos, y_pos):
    move_possible = False
    
    while not move_possible :
        angle_deg = rd.randint(0, 360)
        new_x, new_y = move(x_pos, y_pos, angle_deg)
        move_possible = x_in_boundaries(new_x) and y_in_boundaries(y_pos) and map_annoted[new_y][new_x]
    
    return new_x, new_y, angle_deg

# Next vectors generation
def generate_new_vector(x_pos, y_pos, angle_deg, max_attempts=20):
    angle_step = ANGLE_ADJUSTMENT
    # Try to find a valid move by trying different angles
    # If we fail more than 'max_attemps' times, we try again with a wider angle range until we reach 360
    for angle_offset in range(0, 360, angle_step):
        for _ in range(max_attempts):
            new_angle = (angle_deg + angle_offset) % 360
            new_x, new_y = move(x_pos, y_pos, new_angle)
            if x_in_boundaries(new_x) and y_in_boundaries(new_y) and map_annoted[new_y][new_x]:
                return new_x, new_y, new_angle

    # If we reach here, we failed to find a valid move after trying all angles
    # Generate a completely random value
    return rd.randint(0, map_width-1), rd.randint(0, map_height-1), rd.randint(0, 360)
    
    
    
    

            
########################################################################################## MAIN PROCESS

# Initialization
def init_pos():
    # Spawn
    x_pos, y_pos = random_spawn()
    
    # Get date and time
    date = datetime.now()
    str_date = date.strftime("%d/%m/%Y - %H:%M")
    
    return str_date, x_pos, y_pos

# Make first move 
def first_move(date, x_pos, y_pos):
    # Change time
    new_date = datetime.strptime(date, "%d/%m/%Y - %H:%M")
    new_date = new_date + timedelta(hours=1)
    str_new_date = new_date.strftime("%d/%m/%Y - %H:%M")
    
    # Change position
    new_x, new_y, angle = generate_initial_vector(x_pos, y_pos)
    
    return str_new_date, new_x, new_y, angle


def make_a_move(date, x_pos, y_pos, angle):
    # Change time
    new_date = datetime.strptime(date, "%d/%m/%Y - %H:%M")
    new_date = new_date + timedelta(hours=1)
    str_new_date = new_date.strftime("%d/%m/%Y - %H:%M")
    
    # Change position
    new_x, new_y, new_angle = generate_new_vector(x_pos, y_pos, angle)
    
    return str_new_date, new_x, new_y, new_angle







########################################################################################## EXAMPLE OF USE 

#date, x, y = init_pos()
#print(date, x, y)

#date, x, y, angle = first_move(date, x, y)
#print(date, x, y)

#for i in range(10):
#    date, x, y, angle = make_a_move(date, x, y, angle)
#    print(date, x, y, angle)