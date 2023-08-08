import threading
import time
import random
import config
import sensorModule
import domainLogicModule
import pygame
import os

class PrintValue:
    def __init__(self, vehicleInstance):
        
        self.vehicleInstance = vehicleInstance

    def output(self):

        # Intialize the Empty Matrix

        matrix = [["" for _ in range(50)] for _ in range(50)]

        # Add all the vehicles to the matrix

        for i in range(self.vehicleInstance.ROIsize):

            matrix[i][10] = self.vehicleInstance.SS[i]

            matrix[i][11] = self.vehicleInstance.ET[i]

            matrix[12][i] = self.vehicleInstance.NT[i]

            matrix[13][i] = self.vehicleInstance.ES[i]

            matrix[24-1-i][12] = self.vehicleInstance.WT[i]

            matrix[24-1-i][13] = self.vehicleInstance.NS[i]

            matrix[10][24-1-i] = self.vehicleInstance.WS[i]

            matrix[11][24-1-i] = self.vehicleInstance.ST[i]

        screen.fill(WHITE)

        cell_size = config.CELL_SIZE
        margin = config.MARGIN




        score  =[0]*4

        num_veh = [0]*4

        for i in range(4):

            cur_score = 0

            veh_count = 0

            first = self.vehicleInstance.vehicleCache[i+1][0]
            second = self.vehicleInstance.vehicleCache[i+1][1]

            for j in range(len(first)):

                cur_score += first[j] * self.vehicleInstance.score[j]

                if first[j] == 1:

                    veh_count+=1

                cur_score += second[j] * self.vehicleInstance.score[j]

                if second[j] == 1:

                    veh_count+=1

            score[i] = cur_score

            num_veh[i] = veh_count

        
        cur_pattern_toggle = self.vehicleInstance.condition

        if cur_pattern_toggle:

            cur_pattern_cycle = "In Limits"

        
        else:
            
            cur_pattern_cycle = "Not in Limits"




        # Loop through the matrix to check the coordinates to create the cell changes through pyGame.

        for x in range(len(matrix)):

            for y in range(len(matrix[0])):

                cell_value = matrix[x][y]

                # Current Cycle is coloured in Blue to show clear visulalization

                if (x,y) in config.CURRENT_CYCLE[self.vehicleInstance.cycle]:

                    cell_color = BLUE if cell_value else WHITE

                else:

                    # Else the rest of vehicles will be in Black. 
           
                    cell_color = BLACK if cell_value else WHITE

                cell_rect = pygame.Rect(y * (cell_size + margin), x * (cell_size + margin), cell_size, cell_size)

                pygame.draw.rect(screen, cell_color, cell_rect)

                pygame.draw.rect(screen, WHITE, cell_rect, 1)  

                # Conditions to show the wait time of the vehicles.

                if x == 12 and y == 8:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[0][0]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))
                    
                elif x == 11 and y == 15:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[0][1]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))

                
                elif x == 8 and y == 10:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[1][0]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))

                elif x == 15 and y == 13:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[1][1]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))
                    
                
                elif x == 8 and y == 11:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[2][1]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))
                    
                
                elif x == 15 and y == 12:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[2][0]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))
                    
                
                if x == 13 and y == 8:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[3][1]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))
                                        
                
                elif x == 10 and y == 15:

                    font = pygame.font.Font(None, config.FONT_SIZE)
                    text_surface = font.render(str(self.vehicleInstance.waitTime[3][0]), True, BLACK)
                    screen.blit(text_surface, (cell_rect.x + cell_size // 2 - text_surface.get_width() // 2,
                                            cell_rect.y + cell_size // 2 - text_surface.get_height() // 2))
                    

                
                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(cur_pattern_cycle, True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2), (screen_size[1] // 2) - 250))
                    screen.blit(text_surface, text_rect)
                    
                
                    
                
                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("Cycle Time : "+str(round((time.time() - self.vehicleInstance.cycleTime) / config.VALIDATION,2)), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2), (screen_size[1] // 2) - 200))
                    screen.blit(text_surface, text_rect)
                    
                

                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("Pattern", True, BLACK)
                    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, (screen_size[1] // 2) + 10))
                    screen.blit(text_surface, text_rect)
                    
                if x == 19 and y == 40:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("Score", True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 85, (screen_size[1] // 2)+10))
                    screen.blit(text_surface, text_rect)


                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("NS Turning", True, BLACK)
                    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, (screen_size[1] // 2) + 30))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("NS Straight", True, BLACK)
                    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, (screen_size[1] // 2) + 50))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("EW Turning", True, BLACK)
                    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, (screen_size[1] // 2) + 70))
                    screen.blit(text_surface, text_rect)

                
                if x == 19 and y == 20:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("EW Straight", True, BLACK)
                    text_rect = text_surface.get_rect(center=(screen_size[0] // 2, (screen_size[1] // 2) + 90))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 40:

                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(round(score[0],1)), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 85, (screen_size[1] // 2)+30))
                    screen.blit(text_surface, text_rect)


                if x == 19 and y == 40:

                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(round(score[1],1)), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 85, (screen_size[1] // 2)+50))
                    screen.blit(text_surface, text_rect)


                if x == 19 and y == 40:

                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(round(score[2],1)), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 85, (screen_size[1] // 2)+70))
                    screen.blit(text_surface, text_rect)


                if x == 19 and y == 40:

                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(round(score[3],1)), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 85, (screen_size[1] // 2)+90))
                    screen.blit(text_surface, text_rect)


                if x == 19 and y == 40:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render("Vehicle count", True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 170, (screen_size[1] // 2)+10))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 40:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(num_veh[0]), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 170, (screen_size[1] // 2)+30))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 40:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(num_veh[1]), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 170, (screen_size[1] // 2)+50))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 40:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(num_veh[2]), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 170, (screen_size[1] // 2)+70))
                    screen.blit(text_surface, text_rect)

                if x == 19 and y == 40:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(num_veh[3]), True, BLACK)
                    text_rect = text_surface.get_rect(center=((screen_size[0] // 2) + 170, (screen_size[1] // 2)+90))
                    screen.blit(text_surface, text_rect)


        # Loop through to get the signals done and to toggle them with the current cycle.

        for key,value in config.SIGNAL.items():

            if key == self.vehicleInstance.cycle:

                for each in value:

                    x = each[0]
                    y = each[1]
                    cell_rect = pygame.Rect(y * (cell_size + margin), x * (cell_size + margin), cell_size, cell_size)
                    pygame.draw.circle(screen, GREEN, cell_rect.center, cell_size // 2)

            else:
                    
                for each in value:

                    x = each[0]
                    y = each[1]
                    cell_rect = pygame.Rect(y * (cell_size + margin), x * (cell_size + margin), cell_size, cell_size)
                    pygame.draw.circle(screen, RED, cell_rect.center, cell_size // 2)

        pygame.display.flip()
        clock.tick(1) 


def RunTimer(cycle1Thread, cycle2Thread, cycle3Thread, cycle4Thread, algoInstance, print_value_thread):

    
    cycle1Thread.timerUpdate()
    
    cycle2Thread.timerUpdate()
    
    cycle3Thread.timerUpdate()
    
    cycle4Thread.timerUpdate()

    algoInstance.func()

    print_value_thread.output()

    threading.Timer(config.TIME_SLEEP, RunTimer, args=(cycle1Thread, cycle2Thread, cycle3Thread, cycle4Thread, algoInstance, print_value_thread)).start()


if __name__ == "__main__":

    vehicleInstance = sensorModule.VehicleStack(config.ROI_VEHICLES)
    vehicleProbab = sensorModule.VehicleProbability()
    algoInstance = domainLogicModule.algo(vehicleInstance)
    print_value_thread = PrintValue(vehicleInstance)


    cycle1Thread = sensorModule.Cycle1(vehicleInstance,vehicleProbab)
    cycle2Thread = sensorModule.Cycle2(vehicleInstance,vehicleProbab)
    cycle3Thread = sensorModule.Cycle3(vehicleInstance,vehicleProbab)
    cycle4Thread = sensorModule.Cycle4(vehicleInstance,vehicleProbab)

    pygame.init()

    screen_size = config.SCREEN_SIZE

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    RunTimer(cycle1Thread,cycle2Thread,cycle3Thread,cycle4Thread,algoInstance,print_value_thread)
