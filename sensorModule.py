import threading
import time
import random
import config

#####################################################################################################################################

# VehcilceStack to keep track of all the vehicles flow in a lane


class VehicleStack:

    def __init__(self, sensorROI):

        self.val = 0

        self.ROIsize = sensorROI

        # Initial state of the lane with 0 vehicles

        self.NT = [0] * sensorROI
        self.ST = [0] * sensorROI
        
        self.NS = [0] * sensorROI
        self.SS = [0] * sensorROI

        self.WT = [0] * sensorROI
        self.ET = [0] * sensorROI

        self.WS = [0] * sensorROI
        self.ES = [0] * sensorROI

        # Here lets say pattern = [0,0,0,0,0,0,0,0] -> pattern[-1] is the position near to signal (starting position) and pattern[0] is the last position farther from signal

        '''Dictionary containing the lane for each cycle patter
           1 -> N and S turning
           2 -> N and S through
           3 -> E and W turning
           4 -> E and W through'''

        self.vehicleCache = {1:[self.NT,self.ST],
                             2:[self.NS,self.SS],
                             3:[self.WT ,self.ET],
                             4:[self.WS,self.ES]}
        
        # Traffic pattern mapped with MIN and MAX Active time

        self.vehicleLimits = {1:[config.NS_TURN_MIN,config.NS_TURN_MAX],
                              2:[config.NS_STRAIGHT_MIN,config.NS_STRAIGHT_MAX],
                              3:[config.EW_TURN_MIN,config.EW_TURN_MAX],
                              4:[config.EW_STRAIGHT_MIN,config.EW_STRAIGHT_MAX]}

        # Initially the waitTime of each position is set to 0

        self.waitTime = [[0,0],[0,0],[0,0],[0,0]]

        # Score of each position of a lane to implement highest throughput

        self.score = config.SCORE

        self.cycleOrder = config.CYCLE_ORDER

        self.cycleTime = time.time()

        self.cycle = 1

        self.condition = False



######################################################################################################################################

# VehicleProbability is a class that returns the probability of vehicles showing up in the 4 traffic patterns

class VehicleProbability:
    
    def GetNS_TurningProbability(self):

        return 1 if random.random() <= config.NS_TURNING_PROBABILITY else 0
    
    def GetNS_StraightProbability(self):

        return 1 if random.random() <= config.NS_STRAIGHT_PROBABILITY else 0
    
    def GetWE_TurningProbability(self):

        return 1 if random.random() <= config.EW_TURNING_PROBABILITY else 0
    
    def GetWE_StraightProbability(self):

        return 1 if random.random() <= config.EW_STRAIGHT_PROBABILITY else 0
        

######################################################################################################################################

    
# Cycle 1 is the Vehicle Pattern 1 which is N and S turning traffic


class Cycle1:

    def __init__(self, vehicleInstance, vehicleProbab):

        self.vehicleInstance = vehicleInstance
        self.vehicleProbab = vehicleProbab

    
    def timerUpdate(self):

        # To check if the current cycle is this Vehicle Pattern

        if self.vehicleInstance.cycle == 1:

            # If yes then keep the vehicle flowing by popping out the last eement which is the first vehicle in the stack
            # Then either insert a new vehicle or dont insert a new vehicle with the probability condition provided for this vehicle pattern

            self.vehicleInstance.NT.pop()
            self.vehicleInstance.NT.insert(0, self.vehicleProbab.GetNS_TurningProbability())

            self.vehicleInstance.ST.pop()
            self.vehicleInstance.ST.insert(0, self.vehicleProbab.GetNS_TurningProbability())

        else:

            # If the current cycle is not this cycle then stack up the vehicles in the Region of Interest

            cur_NT = [0]* self.vehicleInstance.ROIsize

            cur_ST = [0]* self.vehicleInstance.ROIsize

            # Loop to check the current line progression and move the vehicle up the lane if the next position to the right is 0
            # Time complexity to do this is O(n) -> n being 8 here.

            for i in range(self.vehicleInstance.ROIsize-1, -1, -1):

                if self.vehicleInstance.NT[i] == 1:

                    cur_NT[i] = 1

                elif i > 0:

                    if self.vehicleInstance.NT[i-1] == 1:

                        cur_NT[i] = 1
                        self.vehicleInstance.NT[i-1] = 0

                
                if self.vehicleInstance.ST[i] == 1:

                    cur_ST[i] = 1


                elif i > 0:

                    if self.vehicleInstance.ST[i-1] == 1:

                        cur_ST[i] = 1
                        self.vehicleInstance.ST[i-1] = 0

            self.vehicleInstance.NT = cur_NT[:]
            self.vehicleInstance.ST = cur_ST[:]

            # If the last position is 0 then call the probability function to get either 1 or 0

            if self.vehicleInstance.NT[0] == 0:

                self.vehicleInstance.NT[0] = self.vehicleProbab.GetNS_TurningProbability()

            if self.vehicleInstance.ST[0] == 0:

                self.vehicleInstance.ST[0] = self.vehicleProbab.GetNS_TurningProbability()

            # If the 1st position has vehicle (1) then start incresing the wait time

            if self.vehicleInstance.NT[-1] == 1:

                self.vehicleInstance.waitTime[0][0]+=1
            
            if self.vehicleInstance.ST[-1] == 1:

                self.vehicleInstance.waitTime[0][1]+=1

        self.vehicleInstance.vehicleCache[1][0] = self.vehicleInstance.NT
        self.vehicleInstance.vehicleCache[1][1] = self.vehicleInstance.ST



########################################################################################################################################


# Cycle 2 is the Vehicle Pattern 2 which is N and S through traffic

class Cycle2:

    def __init__(self, vehicleInstance, vehicleProbab):

        self.vehicleInstance = vehicleInstance
        self.vehicleProbab = vehicleProbab

    def timerUpdate(self):

        # To check if the current cycle is this Vehicle Pattern
    
        if self.vehicleInstance.cycle == 2:

            # If yes then keep the vehicle flowing by popping out the last eement which is the first vehicle in the stack
            # Then either insert a new vehicle or dont insert a new vehicle with the probability condition provided for this vehicle pattern

            self.vehicleInstance.NS.pop()
            self.vehicleInstance.NS.insert(0, self.vehicleProbab.GetNS_StraightProbability())

            self.vehicleInstance.SS.pop()
            self.vehicleInstance.SS.insert(0, self.vehicleProbab.GetNS_StraightProbability())

        else:

            # If the current cycle is not this cycle then stack up the vehicles in the Region of Interest

            cur_NS = [0]* self.vehicleInstance.ROIsize

            cur_SS = [0]* self.vehicleInstance.ROIsize

            # Loop to check the current line progression and move the vehicle up the lane if the next position to the right is 0
            # Time complexity to do this is O(n) -> n being 8 here.

            for i in range(self.vehicleInstance.ROIsize-1, -1, -1):

                if self.vehicleInstance.NS[i] == 1:

                    cur_NS[i] = 1

                elif i > 0:

                    if self.vehicleInstance.NS[i-1] == 1:

                        cur_NS[i] = 1
                        self.vehicleInstance.NS[i-1] = 0

                
                if self.vehicleInstance.SS[i] == 1:

                    cur_SS[i] = 1


                elif i > 0:

                    if self.vehicleInstance.SS[i-1] == 1:

                        cur_SS[i] = 1
                        self.vehicleInstance.SS[i-1] = 0

            self.vehicleInstance.NS = cur_NS[:]
            self.vehicleInstance.SS = cur_SS[:]

            # If the last position is 0 then call the probability function to get either 1 or 0

            if self.vehicleInstance.NS[0] == 0:

                self.vehicleInstance.NS[0] = self.vehicleProbab.GetNS_StraightProbability()

            if self.vehicleInstance.SS[0] == 0:

                self.vehicleInstance.SS[0] = self.vehicleProbab.GetNS_StraightProbability()

            # If the 1st position has vehicle (1) then start incresing the wait time

            if self.vehicleInstance.NS[-1] == 1:

                self.vehicleInstance.waitTime[1][0]+=1
            
            if self.vehicleInstance.SS[-1] == 1:

                self.vehicleInstance.waitTime[1][1]+=1

        self.vehicleInstance.vehicleCache[2][0] = self.vehicleInstance.NS
        self.vehicleInstance.vehicleCache[2][1] = self.vehicleInstance.SS





########################################################################################################################################



# Cycle 3 is the Vehicle Pattern 3 which is E and W turning traffic


class Cycle3:

    def __init__(self, vehicleInstance, vehicleProbab):

        self.vehicleInstance = vehicleInstance
        self.vehicleProbab = vehicleProbab

    def timerUpdate(self):

        # To check if the current cycle is this Vehicle Pattern

        if self.vehicleInstance.cycle == 3:

            # If yes then keep the vehicle flowing by popping out the last eement which is the first vehicle in the stack
            # Then either insert a new vehicle or dont insert a new vehicle with the probability condition provided for this vehicle pattern

            self.vehicleInstance.WT.pop()
            self.vehicleInstance.WT.insert(0, self.vehicleProbab.GetWE_TurningProbability())

            self.vehicleInstance.ET.pop()
            self.vehicleInstance.ET.insert(0, self.vehicleProbab.GetWE_TurningProbability())

        else:

            # If the current cycle is not this cycle then stack up the vehicles in the Region of Interest

            cur_WT = [0]* self.vehicleInstance.ROIsize

            cur_ET = [0]* self.vehicleInstance.ROIsize

            # Loop to check the current line progression and move the vehicle up the lane if the next position to the right is 0
            # Time complexity to do this is O(n) -> n being 8 here.

            for i in range(self.vehicleInstance.ROIsize-1, -1, -1):

                if self.vehicleInstance.WT[i] == 1:

                    cur_WT[i] = 1

                elif i > 0:

                    if self.vehicleInstance.WT[i-1] == 1:

                        cur_WT[i] = 1
                        self.vehicleInstance.WT[i-1] = 0

                
                if self.vehicleInstance.ET[i] == 1:

                    cur_ET[i] = 1


                elif i > 0:

                    if self.vehicleInstance.ET[i-1] == 1:

                        cur_ET[i] = 1
                        self.vehicleInstance.ET[i-1] = 0

            self.vehicleInstance.WT = cur_WT[:]
            self.vehicleInstance.ET = cur_ET[:]

            # If the last position is 0 then call the probability function to get either 1 or 0
            
            if self.vehicleInstance.WT[0] == 0:

                self.vehicleInstance.WT[0] = self.vehicleProbab.GetWE_TurningProbability()

            if self.vehicleInstance.ET[0] == 0:

                self.vehicleInstance.ET[0] = self.vehicleProbab.GetWE_TurningProbability()

            # If the 1st position has vehicle (1) then start incresing the wait time

            if self.vehicleInstance.WT[-1] == 1:

                self.vehicleInstance.waitTime[2][0]+=1
            
            if self.vehicleInstance.ET[-1] == 1:

                self.vehicleInstance.waitTime[2][1]+=1

        
        self.vehicleInstance.vehicleCache[3][0] = self.vehicleInstance.WT
        self.vehicleInstance.vehicleCache[3][1] = self.vehicleInstance.ET




##########################################################################################################################################



# Cycle 4 is the Vehicle Pattern 4 which is E and W through traffic


class Cycle4:

    def __init__(self, vehicleInstance, vehicleProbab):

        self.vehicleInstance = vehicleInstance
        self.vehicleProbab = vehicleProbab

    def timerUpdate(self):

        # To check if the current cycle is this Vehicle Pattern

        if self.vehicleInstance.cycle == 4:

            # If yes then keep the vehicle flowing by popping out the last eement which is the first vehicle in the stack
            # Then either insert a new vehicle or dont insert a new vehicle with the probability condition provided for this vehicle pattern

            self.vehicleInstance.WS.pop()
            self.vehicleInstance.WS.insert(0, self.vehicleProbab.GetWE_StraightProbability())

            self.vehicleInstance.ES.pop()
            self.vehicleInstance.ES.insert(0, self.vehicleProbab.GetWE_StraightProbability())
        
        else:

            # If the current cycle is not this cycle then stack up the vehicles in the Region of Interest

            cur_WS = [0]* self.vehicleInstance.ROIsize

            cur_ES = [0]* self.vehicleInstance.ROIsize

            for i in range(self.vehicleInstance.ROIsize-1, -1, -1):

                if self.vehicleInstance.WS[i] == 1:

                    cur_WS[i] = 1

                elif i > 0:

                    if self.vehicleInstance.WS[i-1] == 1:

                        cur_WS[i] = 1
                        self.vehicleInstance.WS[i-1] = 0

                
                if self.vehicleInstance.ES[i] == 1:

                    cur_ES[i] = 1


                elif i > 0:

                    if self.vehicleInstance.ES[i-1] == 1:

                        cur_ES[i] = 1
                        self.vehicleInstance.ES[i-1] = 0

            self.vehicleInstance.WS = cur_WS[:]
            self.vehicleInstance.ES = cur_ES[:]

            # If the last position is 0 then call the probability function to get either 1 or 0
            
            if self.vehicleInstance.WS[0] == 0:

                self.vehicleInstance.WS[0] = self.vehicleProbab.GetWE_StraightProbability()

            if self.vehicleInstance.ES[0] == 0:

                self.vehicleInstance.ES[0] = self.vehicleProbab.GetWE_StraightProbability()

            # If the 1st position has vehicle (1) then start incresing the wait time

            if self.vehicleInstance.WS[-1] == 1:

                    self.vehicleInstance.waitTime[3][0]+=1
                
            if self.vehicleInstance.ES[-1] == 1:

                self.vehicleInstance.waitTime[3][1]+=1

        
        self.vehicleInstance.vehicleCache[4][0] = self.vehicleInstance.WS
        self.vehicleInstance.vehicleCache[4][1] = self.vehicleInstance.ES


########################################################################################################################################

