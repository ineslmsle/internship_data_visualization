import haversine
import sys

STOP_ID=0
STOP_CODE=1
STOP_NAME=2
STOP_DESC=3
STOP_LAT=4
STOP_LON=5
ZONE_ID=6
STOP_URL=7
LOCATION_TYPE=8
PARENT_STATION=9

x_dcu_center = 53.3850
y_dcu_center = -6.2578

#usage
n = len(sys.argv)
if n > 2:
    print("Usage: python3 get_stops_in_circle.py <diameter of the circle (meters)>")
    sys.exit()

if n == 2:
    if(sys.argv[1].isdigit()):
        circle_radius_meters = int(sys.argv[1])
    else:
        print("The diameter of the circle must be a positive integer")
        sys.exit()
else:
    #default value
    circle_radius_meters = 500


with open('stops.txt', 'r') as f: 
    # Skip the header
    next(f) 
    count = 0
    # Read and process the remaining lines 
    for line in f: 
        if "\"" in line:
            continue

        line = line.split(",")
        x_stop = float(line[STOP_LAT])
        y_stop = float(line[STOP_LON])

        distance=haversine.haversine((x_stop, y_stop), 
                                     (x_dcu_center, y_dcu_center), 
                                      unit=haversine.Unit.METERS)
        
        if distance < circle_radius_meters:
            count += 1
            print(str(line[STOP_CODE])  + " " 
                  + str(line[STOP_NAME]) + " (" + str(int(distance)) + "m)")

        
    print(str(count) + " stops in the circle of " 
          + str(circle_radius_meters) + " meters from DCU center")