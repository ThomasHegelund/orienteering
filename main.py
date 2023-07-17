from math import dist
from dataclasses import dataclass
import csv
from random import choice

@dataclass
class CheckPoint:
    id: int
    x: int
    y: int
     

def euclidean_distance(point_a: CheckPoint, point_b: CheckPoint):
    point_a_iterable = (point_a.x, point_a.y)
    point_b_iterable = (point_b.x, point_b.y)

    return convert_distance_to_meter(dist(point_a_iterable, point_b_iterable))


def convert_distance_to_meter(distance: float):
    return distance * 10

def load_check_points(path: str):
    with open(path, newline='') as csvfile:
        check_points = csv.reader(csvfile, delimiter=";")
        next(check_points, None) # skip header

        check_point_objects = []
        for check_point in check_points:
            check_point_object = CheckPoint(*map(int,check_point)) # NEED TO FORCE TO INT
            check_point_objects.append(check_point_object)

    return check_point_objects

def validate_number_input(input_text: str):
    while True:
        user_input = input(input_text)
        if user_input.isnumeric() is True:
            break
        print('Input is not a number. Try again:') 
    
    return float(user_input)

check_points = load_check_points('checkpoints.csv')

chosen_check_points = []

n_check_points = int(validate_number_input('How many check points do you maximum want? '))
max_total_distance = validate_number_input('How long do you max want the route to be (in meters)? ')

total_distance = 0
current_distance = 0

last_check_point = check_points[53]
chosen_check_points.append(last_check_point)
check_points.remove(last_check_point)

for _ in range(n_check_points):
    distance = 0
    first_run = True
    check_points_avaliable = True

    while first_run or total_distance > max_total_distance:
        if len(check_points) == 0:
            check_points_avaliable = False
            break

        first_run = False
        total_distance -= distance

        new_check_point = choice(check_points)

        distance = euclidean_distance(last_check_point, new_check_point)
        total_distance += distance
    
        check_points.remove(new_check_point)
        
    if check_points_avaliable:
        chosen_check_points.append(new_check_point)

print("The route is:")
print("->".join(map(lambda x: str(x.id), chosen_check_points)))
print(f"The total distance is {total_distance:.2f} m")
