import numpy as np
import sys
import math
def get_trash_locations(latitude,longitude):
    with open('trash_locations.txt', 'r') as fp:
        trash_locations = fp.read()

        #seperate based on new lines
        trash_locations = trash_locations.split('\n')
    
    trash_lists = []
    #get trash locations within 2 miles
    for next_location in trash_locations:
        #split based on spaces
        next_location = next_location.split(' ')

        #convert to floats
        next_latitude = float(next_location[0])
        next_longitude = float(next_location[1])

        #calculate distance
        distance = calculate_distance((latitude,longitude),(next_latitude,next_longitude))
        if(distance<2):
            next_distance_travelled = float(next_location[2])
            next_magnitude = float(next_location[3])
            trash_lists.append([next_latitude,next_longitude,next_distance_travelled,next_magnitude])
    print(trash_lists, file=sys.stderr)
    return trash_lists

def calculate_distance(p1,p2):
    lat1 = p1[0]
    lon1 = p1[1]
    lat2 = p2[0]
    lon2 = p2[1]
    #calculates distance between two points on the earth
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 3958.8
    c = 2 * math.asin(math.sqrt(a))
    distance = rad * c
    print(distance, file=sys.stderr)
    return distance