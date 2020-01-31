from scipy.spatial.distance import cdist
import numpy as np

def normal_distance_eval(robot_coords, leader_coords):
    robot_dist_to_leader_path = []

    for r_coord in robot_coords:
        distances = cdist([r_coord], leader_coords)
        min_dist = np.min(distances)
        robot_dist_to_leader_path.append(min_dist)
        
    return robot_dist_to_leader_path, np.sum(robot_dist_to_leader_path)

