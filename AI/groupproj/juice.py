import numpy as np
import pygame

def is_terminal_state(): #checks if state is terminal or not
    for i in D:
        if(i != max_blocks):
            return False
    return True

def fetch_rewards(row,col): #will return 13 if picking up or dropping off, otherwise just -1
    if(X==1):
        for zone in range(len(Dzones)):
            if([row,col] == Dzones[zone] and D[zone] < max_blocks):
                return 13
    if(X==0):
        for zone in range(len(Pzones)):
            if([row,col] == Pzones[zone] and P[zone] > 0):
                return 13
    return -1

def toggle_block(row,col): #will pickup or dropoff if available
    global P,D,X
    if(X==1):
        for zone in range(len(Dzones)):
            if([row,col] == Dzones[zone] and D[zone] < max_blocks):
                X = 0
                D[zone]+=1
    if(X==0):
        for zone in range(len(Pzones)):
            if([row,col]== Pzones[zone] and P[zone] > 0):
                X = 1
                P[zone]-=1                

def biDec(bi): #not accurate btw but it works lol
    dec = 0
    for i in range(len(S)):
        if S[i] == 1:
            dec += i+1
    return dec

def stuv(): #sets STUV to correct values (read slide 10 in pptx)
    global S
    if(X==1):
        for zone in range(len(S)):
            if zone < len(D) and D[zone] < max_blocks:
                S[zone] = 1
            else:
                S[zone] = 0        
    if(X==0):
        for zone in range(len(S)):
            if zone < len(P) and P[zone] > 0:
                S[zone] = 1
            else:
                S[zone] = 0    
    return biDec(S)

def get_next_action(policy,s): #gets next action based on policy
    if(policy == 'PGreedy'):
        return np.argmax(q_values[current_row_index,current_column_index,X,s])
    if(policy == 'PRandom'):
        return np.random.randint(4)
    if(policy == 'PExploit'):
        if(np.random.random() < 0.8):
            return np.argmax(q_values[current_row_index,current_column_index,X,s])
        else:
            return np.random.randint(4)

def get_next_location(action_index): #gets next location based on action index
    new_row_index = current_row_index
    new_column_index = current_column_index
    if actions[action_index] == 'up' and current_row_index > 0:
        new_row_index -= 1
    elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
        new_column_index += 1
    elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
        new_row_index += 1
    elif actions[action_index] == 'left' and current_column_index > 0:
        new_column_index -= 1
    return new_row_index, new_column_index

def init(): #reinitializes values
    global P, D, X, current_row_index, current_column_index
    P = np.full(len(Pzones),start_blocks) #pickup locations block counts
    D = np.full(len(Dzones),0) #dropoff locations block counts
    X = 0
    current_row_index = start_row
    current_column_index = start_col

def run(steps=6000,terminals_allowed=-1,learning_rate=0.3,discount_factor=0.5,policy='PExploit',sarsa=False,visual=False): #runs for each expirement
    global P,D,X,current_row_index,current_column_index,q_values,reward_avg,move_avg
    step = 0
    terminals = 0
    while step < steps and (terminals_allowed==-1 or terminals < terminals_allowed):
        rewards = 0
        moves = 0
        while not is_terminal_state() and step < steps:        
            s = stuv()
            action_index = get_next_action(policy,s)            
            old_row_index, old_column_index = current_row_index, current_column_index
            current_row_index, current_column_index = get_next_location(action_index)
            reward = fetch_rewards(current_row_index,current_column_index)
            rewards+=reward          
            old_q_value = q_values[old_row_index,old_column_index,X,s,action_index]

            if sarsa:
                temporal_difference = reward + (discount_factor * q_values[current_row_index,current_column_index,X,s,get_next_action(policy,s)]) - old_q_value
            else:
                temporal_difference = reward + (discount_factor * np.max(q_values[current_row_index,current_column_index,X,s])) - old_q_value

            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[old_row_index, old_column_index, X, s, action_index] = new_q_value
            
            if(reward == 13):
                toggle_block(current_row_index,current_column_index)
            
            if([current_row_index,current_column_index] != [old_row_index,old_column_index]):
                moves+=1
                step+=1

                if visual:
                    gameDisplay.fill(black)

                    if(X == 1):
                        pygame.draw.rect(gameDisplay,red,(current_column_index*50,current_row_index*50,50,50))
                    else:
                        pygame.draw.rect(gameDisplay,darkred,(current_column_index*50,current_row_index*50,50,50))

                    for zone in range(len(Dzones)):
                        num = font.render(str(D[zone]),True,white)
                        gameDisplay.blit(num,(Dzones[zone][1]*50+17,Dzones[zone][0]*50+12))
                        pygame.draw.rect(gameDisplay,green,(Dzones[zone][1]*50,Dzones[zone][0]*50,50,50),3)

                    for zone in range(len(Pzones)):
                        num = font.render(str(P[zone]),True,white)
                        gameDisplay.blit(num,(Pzones[zone][1]*50+17,Pzones[zone][0]*50+12))
                        pygame.draw.rect(gameDisplay,blue,(Pzones[zone][1]*50,Pzones[zone][0]*50,50,50),3)
                    
                    pygame.display.update()
                    clock.tick(15)

                    for event in pygame.event.get(): #closes window for that run
                        if event.type == pygame.QUIT:
                            visual = False
        
        reward_avg[len(reward_avg)-1] += rewards #adds ending rewards and moves to rewards and moves list
        move_avg[len(move_avg)-1] += moves

        if is_terminal_state(): #starts adding to next rewards and moves list, also resets world
            init()
            terminals+=1
            reward_avg.append(0)
            move_avg.append(0)        

def avgs(): #prints the report of each expirement and reinits report for next expirement
    global move_avg, reward_avg

    if not is_terminal_state(): #removes last dataset if terminal state not reached
        move_avg.pop()
        reward_avg.pop()

    avg_rewards = int(sum(reward_avg)/len(reward_avg))
    avg_moves = int(sum(move_avg)/len(move_avg))
    
    print('\nTerminal States Reached:',len(move_avg))
    print('Average Rewards:',avg_rewards)
    print('Average Moves:',avg_moves)
    print('Smartness:',"{:.2f}".format(reward_avg[len(reward_avg)-1]/move_avg[len(move_avg)-1]),'\n')

    for i in range(len(move_avg)):
        print(i+1,'Rewards:',reward_avg[i],'Moves:',move_avg[i])
        
    move_avg = [0]
    reward_avg = [0]
    Q_reset()

def Q_reset(): #resets the Q-table and World
    global q_values,S,gameDisplay

    init()
    S = np.zeros((np.max([len(D),len(P)])))
    gameDisplay = pygame.display.set_mode((environment_columns*50,environment_rows*50))
    q_values = np.zeros((environment_rows, environment_columns,2, pow(len(S),2), 4))
    

pygame.init()
sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 40)

white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,0,255)
darkred = (100,0,0)
red = (255,0,0)

environment_rows = 5 #grid init
environment_columns = 5

max_blocks = 4 #dropoff allowed
start_blocks = 8 #starting blocks in p zones

reward_avg = [0] #list of rewards fetched from each terminal state in a run
move_avg = [0] #same for moves

actions = ['up', 'right', 'down', 'left']

Pzones = [[2,4],[3,1]] # Changing these values will allow you to change pickup and dropoff locations
Dzones = [[0,0],[0,4],[2,2],[4,4]]

P = np.full(len(Pzones),start_blocks) #pickup locations block counts
D = np.full(len(Dzones),0) #dropoff locations block counts
X = 0 #agent carrying block or not
S = np.zeros((np.max([len(D),len(P)]))) #read pptx slide 10

start_row = 4 #set this anywhere in the code if you want to change the start pos
start_col = 0
current_row_index = start_row #sets current pos to start pos initially
current_column_index = start_col

q_values = np.zeros((environment_rows, environment_columns,2, pow(len(S),2), 4)) #read slide 10 in pptx

gameDisplay = pygame.display.set_mode((environment_columns*50,environment_rows*50))
pygame.display.set_caption('PD World')
clock = pygame.time.Clock()

print('\nExpirement 1')

print('\na.')
run(steps=6000,policy='PRandom')
avgs()

print('\nb.')
run(steps=500,policy='PRandom')
run(steps=5500,policy='PGreedy',visual=True)
avgs()

print('\nc.')
run(steps=500,policy='PRandom')
run(steps=5500,visual=True)
avgs()

print('\nExpirement 2')
run(steps=500,policy='PRandom',sarsa=True)
run(steps=5500,sarsa=True,visual=True)
avgs()

print('\nExpirement 3')
run(steps=500,learning_rate=0.15,discount_factor=0.45,policy='PRandom')
run(steps=5500,learning_rate=0.15,discount_factor=0.45,visual=True)
avgs()

print('\nExpirement 4')
run(steps=500,policy='PRandom')
run(steps=5500,terminals_allowed=3,visual=True)
Pzones = [[1,3],[3,1]]
run(steps=5500,terminals_allowed=3,visual=True)

print('\nExpirement 5')
environment_rows = 10
environment_columns = 10
start_row = 4
start_col = 4
Dzones = [[0,0],[9,0],[0,9],[9,9],[4,4]]
Pzones = [[2,2],[6,6],[7,3]]
avgs()
run(steps=6000,policy='PRandom')
run(steps=600000)
run(steps=6000,policy='PGreedy',visual=True)
avgs()
