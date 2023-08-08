
# Total distance factor of the Region of Interest
ROI_VEHICLES = 8

# The score/weights for each position in a line
SCORE = [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

# Min and Max of Traffic Pattern

VALIDATION = 1

TIME_SLEEP = 1

# N and S Turning
NS_TURN_MIN = 10 * VALIDATION
NS_TURN_MAX = 60 * VALIDATION

# N and S Through
NS_STRAIGHT_MIN = 30 * VALIDATION
NS_STRAIGHT_MAX = 120 * VALIDATION

# E and W Turning
EW_TURN_MIN = 10 * VALIDATION
EW_TURN_MAX = 30 * VALIDATION

# E and W Through
EW_STRAIGHT_MIN = 30 * VALIDATION
EW_STRAIGHT_MAX = 60 * VALIDATION

# Wait Time
MAX_WAIT_TIME = 240 * VALIDATION

# Min Active Signal Time
MIN_ACTIVE_TIME_SIGNAL = 8 * VALIDATION

# Number of Vehicles per line for conditional Active Limits
VEHICLE_THRESHOLD = 5

# Cycle Order
# NS_TURN (1) -> NS_STRAIGHT (2) -> EW_TURN (3) -> EW_STRAIGHT (4)

CYCLE_ORDER = {1:2,2:3,3:4,4:1}

# Traffic Pattern Vehicle Probability

NS_TURNING_PROBABILITY = 0.2
NS_STRAIGHT_PROBABILITY = 0.6
EW_TURNING_PROBABILITY = 0.1
EW_STRAIGHT_PROBABILITY = 0.5


SIGNAL = {1 : [(12,15),(11,8)],
          2 : [(8,13),(15,10)],
          3 : [(15,11),(8,12)],
          4 : [(13,15),(10,8)]}


CURRENT_CYCLE = {1 : [(12,0),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(11,23),(11,22),(11,21),(11,20),(11,19),(11,18),(11,17),(11,16)],
                 2 : [(23,13),(22,13),(21,13),(20,13),(19,13),(18,13),(17,13),(16,13),(0,10),(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10)],
                 3 : [(23,12),(22,12),(21,12),(20,12),(19,12),(18,12),(17,12),(16,12),(0,11),(1,11),(2,11),(3,11),(4,11),(5,11),(6,11),(7,11)],
                 4 : [(10,23),(10,22),(10,21),(10,20),(10,19),(10,18),(10,17),(10,16),(13,0),(13,1),(13,2),(13,3),(13,4),(13,5),(13,6),(13,7)]}


# PyGame Configurations

CELL_SIZE = 20
MARGIN = 2
FONT_SIZE = 20
SCREEN_SIZE = (840, 640) 