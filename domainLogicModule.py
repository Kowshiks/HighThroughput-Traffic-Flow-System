import threading
import time
import random
import config


class algo:

    def __init__(self,dataInstance):
        self.dataInstance = dataInstance

    
    def func(self):

        toggle = True

        # Loop to check if the traffic pattern should follow the provided conditions (LIMITS)

        for key,value in self.dataInstance.vehicleCache.items():

            if key != self.dataInstance.cycle:

                first_count = sum(value[0])
                second_count = sum(value[0])

                # If the sum of vehicles in both lanes of any Cycle is lesser than a threshold then it should not follow the limit conditions  

                if first_count + second_count < config.VEHICLE_THRESHOLD:

                    toggle = False
                    break

        
        # If it should follow Active Limit Condition

        if toggle:

            print("IN CONDITION")

            self.dataInstance.condition = True

            # If the time is above the Minimum Acitve Time of any Signal in all condition

            if time.time() - self.dataInstance.cycleTime > self.dataInstance.vehicleLimits[self.dataInstance.cycle][0]:

                # If the starting posiiton of both the lanes have vehicles then just pass it

                if self.dataInstance.vehicleCache[self.dataInstance.cycle][0][-1] == 1 and self.dataInstance.vehicleCache[self.dataInstance.cycle][1][-1] == 1:

                        pass
                
                # Now check the score of other cycle patterns and also check how close the starting vechile in each cycle pattern are to the starting index

                else:

                        cur_cycle = self.dataInstance.cycle

                        nextCycle = self.dataInstance.cycleOrder[self.dataInstance.cycle]

                        val = 0

                        first  = self.dataInstance.vehicleCache[self.dataInstance.cycle][0]

                        second = self.dataInstance.vehicleCache[self.dataInstance.cycle][1]

                        cur_count = 0

                        # Vehcile count and score of the current cycle pattern

                        for each in range(len(first)):

                            val += first[each] * self.dataInstance.score[each]

                            if first[each] == 1:

                                cur_count+=1

                            val += second[each] * self.dataInstance.score[each]

                            if second[each] == 1:

                                cur_count+=1

                        # Check for other cycle scores if they are higer and also check the vehicle count

                        for j in range(4):

                            count = 0

                            if j+1 != self.dataInstance.cycle:

                                cur_val = 0

                                first  = self.dataInstance.vehicleCache[j+1][0]

                                second = self.dataInstance.vehicleCache[j+1][1]

                                for each in range(len(first)):

                                    cur_val += first[each] * self.dataInstance.score[each]

                                    if first[each] == 1:

                                        count+=1

                                    cur_val += second[each] * self.dataInstance.score[each]

                                    if second[each] == 1:

                                        count+=1

                                # If the score is higher then change the cycle pattern

                                if cur_val > val:

                                    cur_cycle = nextCycle

                                    val = cur_val

                                    break

                                # If the score is equal but the count of vehicle is higher then also change the pattern

                                if cur_val == val and count > cur_count:

                                    cur_cycle = nextCycle

                                    val = cur_val

                                    break


                        # If higher then change the cycle to the next cycle with the highest score. 

                        if cur_cycle != self.dataInstance.cycle:

                            first  = self.dataInstance.vehicleCache[self.dataInstance.cycle][0]

                            second = self.dataInstance.vehicleCache[self.dataInstance.cycle][1]

                            
                            first_index_1  = 0

                            both_lane_1 = False

                            single_lane_1 = False

                            # Check the closest vehicle index and the number of closest vehilce to the starting point of the current cycle
                            
                            for check in range(len(first)-1,-1,-1):

                                if first[check] == 1 and second[check] == 1:

                                    first_index_1  = check

                                    both_lane_1 = True

                                    break

                                elif first[check] == 1 or second[check] == 1:

                                    first_index_1  = check

                                    single_lane_1  = True

                                    break

                            first  = self.dataInstance.vehicleCache[cur_cycle][0]

                            second = self.dataInstance.vehicleCache[cur_cycle][1]
                            
                            first_index_2  = 0

                            both_lane_2 = False

                            single_lane_2 = False

                            # Check the closest vehicle index and the number of closest vehilce to the starting point of the next cycle
                            
                            for check in range(len(first)-1,-1,-1):

                                if first[check] == 1 and second[check] == 1:

                                    first_index_2  = check

                                    both_lane_2 = True

                                    break

                                elif first[check] == 1 or second[check] == 1:

                                    first_index_2  = check

                                    single_lane_2  = True

                                    break

                            # Change to the pattern which has the highest number of closest vehicle to the starting point
                            
                            if first_index_2 > first_index_1 or ((first_index_2 == first_index_1) and both_lane_2) or (((first_index_2 == first_index_1) and single_lane_1)):

                                self.dataInstance.cycle = cur_cycle

                                # Change the wait time of the next cycle to 0

                                self.dataInstance.waitTime[cur_cycle-1] = [0,0]

                                self.dataInstance.cycleTime = time.time()



            # Also to keep track if the Active iime is below the Max Active Limit, if it crosses the Max Time Limit then change to the next cycle in the sequence
            


            if time.time() - self.dataInstance.cycleTime >= self.dataInstance.vehicleLimits[self.dataInstance.cycle][1]:


                self.dataInstance.cycle = self.dataInstance.cycleOrder[self.dataInstance.cycle]

                self.dataInstance.waitTime[self.dataInstance.cycle-1] = [0,0]

                self.dataInstance.cycleTime = time.time()



        # If it can be random by not following Active Limit Condition

        else:

            print("Random")

            self.dataInstance.condition = False

            # If the time is above the Minimum Acitve Time of any Signal in all condition

            if time.time() - self.dataInstance.cycleTime > config.MIN_ACTIVE_TIME_SIGNAL:

                tmp = True

                for i in range(len(self.dataInstance.waitTime)):

                    if max(self.dataInstance.waitTime[i])+30 >= config.MAX_WAIT_TIME:

                        self.dataInstance.cycle = i+1 

                        # Change the wait time of the next cycle to 0

                        self.dataInstance.waitTime[i] = [0,0]

                        tmp = False

                        self.dataInstance.cycleTime = time.time()

                        break
        
                if tmp:

                    # If the starting positon of both the lanes have vehicles then just pass it

                    if self.dataInstance.vehicleCache[self.dataInstance.cycle][0][-1] == 1 and self.dataInstance.vehicleCache[self.dataInstance.cycle][1][-1] == 1:

                        pass

                    # Now check the score of other cycle patterns and also check how close the starting vechile in each cycle pattern are to the starting index

                    else:

                        cur_cycle = self.dataInstance.cycle

                        val = 0

                        first  = self.dataInstance.vehicleCache[self.dataInstance.cycle][0]

                        second = self.dataInstance.vehicleCache[self.dataInstance.cycle][1]

                        cur_count = 0

                        # Vehcile count and score of the current cycle pattern

                        for each in range(len(first)):

                            val += first[each] * self.dataInstance.score[each]

                            if first[each] == 1:

                                cur_count+=1

                            val += second[each] * self.dataInstance.score[each]

                            if second[each] == 1:

                                cur_count+=1

                        # Check for other cycle scores if they are higer and also check the vehicle count

                        for j in range(4):

                            count = 0

                            if j+1 != self.dataInstance.cycle:

                                cur_val = 0

                                first  = self.dataInstance.vehicleCache[j+1][0]

                                second = self.dataInstance.vehicleCache[j+1][1]

                                for each in range(len(first)):

                                    cur_val += first[each] * self.dataInstance.score[each]

                                    if first[each] == 1:

                                        count+=1

                                    cur_val += second[each] * self.dataInstance.score[each]

                                    if second[each] == 1:

                                        count+=1

                                # If the score is higher then change the cycle pattern

                                if cur_val > val:

                                    cur_cycle = j+1

                                    val = cur_val

                                # If the score is equal but the count of vehicle is higher then also change the pattern

                                if cur_val == val and count > cur_count:

                                    cur_cycle = j+1

                                    val = cur_val



                        # If higher then change the cycle to the next cycle with the highest score. 

                        if cur_cycle != self.dataInstance.cycle:

                            first  = self.dataInstance.vehicleCache[self.dataInstance.cycle][0]

                            second = self.dataInstance.vehicleCache[self.dataInstance.cycle][1]

                            
                            first_index_1  = 0

                            both_lane_1 = False

                            single_lane_1 = False

                            # Check the closest vehicle index and the number of closest vehilce to the starting point of the current cycle
                            
                            for check in range(len(first)-1,-1,-1):

                                if first[check] == 1 and second[check] == 1:

                                    first_index_1  = check

                                    both_lane_1 = True

                                    break

                                elif first[check] == 1 or second[check] == 1:

                                    first_index_1  = check

                                    single_lane_1  = True

                                    break

                            
                            first  = self.dataInstance.vehicleCache[cur_cycle][0]

                            second = self.dataInstance.vehicleCache[cur_cycle][1]

                            
                            first_index_2  = 0

                            both_lane_2 = False

                            single_lane_2 = False

                            # Check the closest vehicle index and the number of closest vehilce to the starting point of the next cycle
                            
                            for check in range(len(first)-1,-1,-1):

                                if first[check] == 1 and second[check] == 1:

                                    first_index_2  = check

                                    both_lane_2 = True

                                    break

                                elif first[check] == 1 or second[check] == 1:

                                    first_index_2  = check

                                    single_lane_2  = True

                                    break

                            # Change to the pattern which has the highest number of closest vehicle to the starting point
                            
                            if first_index_2 > first_index_1 or ((first_index_2 == first_index_1) and both_lane_2) or (((first_index_2 == first_index_1) and single_lane_1)):

                                self.dataInstance.cycle = cur_cycle

                                # Change the wait time of the next cycle to 0

                                self.dataInstance.waitTime[cur_cycle-1] = [0,0]

                                self.dataInstance.cycleTime = time.time()


        print("CYCLE : " , self.dataInstance.cycle)

        