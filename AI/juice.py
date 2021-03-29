#import libraries
import numpy as np

def is_terminal_state():
    for i in D:
        if(i != 4):
            return False
    return True

def fetch_rewards(row,col): #will return 13 if picking up or dropping off, otherwise just -1
    global P, D, X
    cmp = [row,col]

    if(X==1):
        for zone in range(len(Dzones)):
            if(cmp == Dzones[zone] and D[zone] < 4):
                return 13

    if(X==0):
        for zone in range(len(Pzones)):
            if(cmp == Pzones[zone] and P[zone] > 0):
                return 13

    return -1

def toggle_block(row,col):
    global P, D, X
    cmp = [row,col]

    if(X==1):
        for zone in range(len(Dzones)):
            if(cmp == Dzones[zone] and D[zone] < 4):
                X = 0
                D[zone]+=1

    if(X==0):
        for zone in range(len(Pzones)):
            if(cmp == Pzones[zone] and P[zone] > 0):
                X = 1
                P[zone]-=1                

def stuv():
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

def get_next_action(policy):
    if(fetch_rewards(current_row_index-1,current_column_index)==13):
        return 0
    if(fetch_rewards(current_row_index,current_column_index+1)==13):
        return 1
    if(fetch_rewards(current_row_index+1,current_column_index)==13):
        return 2
    if(fetch_rewards(current_row_index,current_column_index-1)==13):
        return 3
    if(policy == 'PGreedy'):
        return np.argmax(q_values[current_row_index,current_column_index,X,S,T,U,V])
    if(policy == 'PRandom'):
        return np.random.randint(4)
    if(policy == 'PExploit'):
        if(np.random.random() < 0.8):
            return np.argmax(q_values[current_row_index,current_column_index,X,S,T,U,V])
        else:
            return np.random.randint(4)

def get_next_location(action_index):
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


def run(learning_rate,discount_factor,policy,sarsa,visual): #runs for each expirement
    init()
    global P,D,X,current_row_index,current_column_index,q_values,reward_avg,move_avg
    rewards = 0
    moves = 0
    while not is_terminal_state():
        moves+=1
        if visual:
            global P,D,X
            grid = [[D[0],0,0,0,D[1]],
            [0,0,0,0,0],
            [0,0,D[2],0,P[0]],
            [0,P[1],0,0,0],
            [0,0,0,0,D[3]]]

            grid[current_row_index][current_column_index] = -1

            for row in grid:
                print(row)
            print()           
        
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
        q_values[old_row_index, old_column_index, X,S,T,U,V, action_index] = new_q_value

        toggle_block(current_row_index,current_column_index)

    
    reward_avg.append(rewards)
    move_avg.append(moves)

def avgs():
    global move_avg, reward_avg
    avg_rewards = sum(reward_avg)/len(reward_avg)
    avg_moves = sum(move_avg)/len(move_avg)
    print('Average Reward: ',avg_rewards)
    print('Average Moves: ',avg_moves)
    move_avg = []
    reward_avg = []

def Q_reset():
    global q_values
    q_values = np.zeros((environment_rows, environment_columns,2, 2,2,2,2, 4))

def expirement(runs,learning_rate,discount_factor,policy,sarsa):
    for r in range(runs):
        run(learning_rate,discount_factor,policy,sarsa,False)

    

# variable init------------------------

environment_rows = 5
environment_columns = 5

reward_avg = []
move_avg = []

actions = ['up', 'right', 'down', 'left']

P = [8,8] #pickup locations block counts
D = [0,0,0,0] #dropoff locations block counts
X = 0 #agent carrying block or not

Pzones = [[2,4],[3,1]]
Dzones = [[0,0],[0,4],[2,2],[4,4]]

#designate pickup possibilities
S = 1
T = 1
U = 1
V = 1

start_row = 4
start_col = 0

q_values = np.zeros((environment_rows, environment_columns,2, 2,2,2,2, 4))

#finish variable init-----------------

#running expirements-------------

print('Expirement 1')

print('a.')
expirement(6000,0.3,0.5,'PRandom',False)
avgs()
Q_reset()

print('b.')
expirement(500,0.3,0.5,'PRandom',False)
expirement(5500,0.3,0.5,'PGreedy',False)
avgs()
Q_reset()

print('c.')
expirement(500,0.3,0.5,'PRandom',False)
expirement(5500,0.3,0.5,'PExploit',False)
avgs()
Q_reset()

print('Expirement 2')
expirement(500,0.3,0.5,'PRandom',True)
expirement(5500,0.3,0.5,'PExploit',True)
avgs()
Q_reset()

print('Expirement 3')
expirement(500,0.15,0.45,'PRandom',False)
expirement(5500,0.15,0.45,'PExploit',False)
avgs()
Q_reset()


