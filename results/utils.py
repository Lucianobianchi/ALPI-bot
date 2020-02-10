from scipy.spatial.distance import cdist
import numpy as np

PATH_OFF = 500

def normal_distance_eval(robot_coords, leader_coords):
    robot_dist_to_leader_path = []

    for i, r_coord in enumerate(robot_coords):
        from_i = i - PATH_OFF if i > PATH_OFF else 0
        to_i = i+PATH_OFF
        distances = cdist([r_coord], leader_coords[from_i:to_i])
        min_dist = np.min(distances)
        robot_dist_to_leader_path.append(min_dist)
        
    return robot_dist_to_leader_path

