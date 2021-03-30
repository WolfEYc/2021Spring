#import libraries
import numpy as np

def is_terminal_state(): #checks if state is terminal or not
    for i in D:
        if(i != 4):
            return False
    return True

def fetch_rewards(row,col): #will return 13 if picking up or dropping off, otherwise just -1
    if(X==1):
        for zone in range(len(Dzones)):
            if([row,col] == Dzones[zone] and D[zone] < 4):
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
            if([row,col] == Dzones[zone] and D[zone] < 4):
                X = 0
                D[zone]+=1
    if(X==0):
        for zone in range(len(Pzones)):
            if([row,col]== Pzones[zone] and P[zone] > 0):
                X = 1
                P[zone]-=1                

def stuv(): #sets STUV to correct values (read slide 10 in pptx)
    global S, T, U, V
    if(X==1):
        if(D[0] == 4):
            S = 0
        else:
            S = 1
        if(D[1] == 4):
            T = 0
        else:
            T = 1
        if(D[2] == 4):
            U = 0
        else:
            U = 1
        if(D[3] == 4):
            V = 0
        else:
            V = 1
    if(X==0):
        if(P[0] == 0):
            S = 0
        else:
            S = 1
        if(P[1] == 0):
            T = 0
        else:
            T = 1
        U = 0
        V = 0

def get_next_action(policy): #gets next action based on policy
    if(policy == 'PGreedy'):
        return np.argmax(q_values[current_row_index,current_column_index,X,S,T,U,V])
    if(policy == 'PRandom'):
        return np.random.randint(4)
    if(policy == 'PExploit'):
        if(np.random.random() < 0.8):
            return np.argmax(q_values[current_row_index,current_column_index,X,S,T,U,V])
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
    P = [8,8]
    D = [0,0,0,0]
    X = 0
    S = 1
    T = 1
    U = 0
    V = 0

    current_row_index = start_row
    current_column_index = start_col

def run(steps,terminals_allowed,learning_rate,discount_factor,policy,sarsa,visual): #runs for each expirement
    global P,D,X,current_row_index,current_column_index,q_values,reward_avg,move_avg
    step = 0
    terminals = 0
    while step < steps and (terminals_allowed==-1 or terminals < terminals_allowed):
        rewards = 0
        moves = 0
        while not is_terminal_state() and step < steps:        
            stuv()
            action_index = get_next_action(policy)            
            old_row_index, old_column_index = current_row_index, current_column_index
            current_row_index, current_column_index = get_next_location(action_index)
            reward = fetch_rewards(current_row_index,current_column_index)
            rewards+=reward          
            old_q_value = q_values[old_row_index,old_column_index,X,S,T,U,V,action_index]

            if sarsa:
                temporal_difference = reward + (discount_factor * q_values[current_row_index,current_column_index,X,S,T,U,V][get_next_action(policy)]) - old_q_value
            else:
                temporal_difference = reward + (discount_factor * np.max(q_values[current_row_index,current_column_index,X,S,T,U,V])) - old_q_value

            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[old_row_index, old_column_index, X, S,T,U,V, action_index] = new_q_value
            
            if(reward == 13):
                toggle_block(current_row_index,current_column_index)
            
            if([current_row_index,current_column_index] != [old_row_index,old_column_index]):
                moves+=1
                step+=1
                if visual:
                    grid = [[D[0],0,0,0,D[1]],
                    [0,0,0,0,0],
                    [0,0,D[2],0,P[0]],
                    [0,P[1],0,0,0],
                    [0,0,0,0,D[3]]]
                    
                    if(X == 1):
                        grid[current_row_index][current_column_index] = -2
                    else:
                        grid[current_row_index][current_column_index] = -1

                    for row in grid:
                        print(row)
                    print()
        
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
    print('Smartness:',"{:.2f}".format(avg_rewards/avg_moves),'\n')

    for i in range(len(move_avg)):
        print(i+1,'Rewards:',reward_avg[i],'Moves:',move_avg[i])
        
    move_avg = [0]
    reward_avg = [0]
    Q_reset()

def Q_reset(): #resets the Q-table and World
    global q_values
    q_values = np.zeros((environment_rows, environment_columns,2, 2,2,2,2, 4))
    init()

environment_rows = 5 #grid init
environment_columns = 5

reward_avg = [0] #list of rewards fetched from each terminal state in a run
move_avg = [0] #same for moves

actions = ['up', 'right', 'down', 'left']

P = [8,8] #pickup locations block counts
D = [0,0,0,0] #dropoff locations block counts
X = 0 #agent carrying block or not
S = 1 #read pptx slide 10
T = 1
U = 0
V = 0

Pzones = [[2,4],[3,1]] # Changing these values will allow you to change pickup and dropoff locations
Dzones = [[0,0],[0,4],[2,2],[4,4]]

start_row = 4 #set this anywhere in the code if you want to change the start pos
start_col = 0

current_row_index = start_row #sets current pos to start pos initially
current_column_index = start_col

q_values = np.zeros((environment_rows, environment_columns,2, 2,2,2,2, 4)) #read slide 10 in pptx

print('\nExpirement 1')

print('\na.')
run(6000,-1,0.3,0.5,'PRandom',False,False)
avgs()

print('\nb.')
run(500,-1,0.3,0.5,'PRandom',False,False)
run(5500,-1,0.3,0.5,'PGreedy',False,False)
avgs()

print('\nc.')
run(500,-1,0.3,0.5,'PRandom',False,False)
run(5500,-1,0.3,0.5,'PExploit',False,False)
avgs()

print('\nExpirement 2')
run(500,-1,0.3,0.5,'PRandom',True,False)
run(5500,-1,0.3,0.5,'PExploit',True,False)
avgs()

print('\nExpirement 3')
run(500,-1,0.15,0.45,'PRandom',False,False)
run(5500,-1,0.15,0.45,'PExploit',False,False)
avgs()

print('\nExpirement 4')
run(500,-1,0.3,0.5,'PRandom',False,False)
run(5500,3,0.3,0.5,'PExploit',False,False)
Pzones = [[1,3],[3,1]]
run(5500,3,0.3,0.5,'PExploit',False,False)
avgs()
