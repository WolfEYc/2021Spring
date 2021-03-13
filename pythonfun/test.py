import csv
import numpy as np

def next_closest_efrac(data,p_efract):
    minRow = 0
    for row in range(1,len(data)):
        if(abs(float(data[row][4])-p_efract) < abs(float(data[minRow][4])-p_efract)):
            minRow = row
    return minRow

def next_closest_screat(data,p_screat):
    minRow = 0
    for row in range(1,len(data)):
        if(abs(float(data[row][7])-p_screat) < abs(float(data[minRow][7])-p_screat)):
            minRow = row
    return minRow

def prediction (data,p_efrac,p_screat,k):
    k_closest_efrac = []
    k_closest_screat = []

    efrac_data = data
    screat_data = data

    for i in range(k):
        eminRow = next_closest_efrac(efrac_data,p_efrac)
        #print(efrac_data[eminRow][4])
        k_closest_efrac.append(efrac_data[eminRow][12])
        efrac_data = np.delete(efrac_data, eminRow,0)

        sminRow = next_closest_screat(screat_data,p_screat)
        #print(screat_data[sminRow][7])
        k_closest_screat.append(screat_data[sminRow][12])
        screat_data = np.delete(screat_data, sminRow,0)

    calculation = 0
    for i in range(k):
        #print(k_closest_efrac[i])
        #print(k_closest_screat[i])
        if(k_closest_efrac[i]=='0'):
            calculation-=(1)
        else:
            calculation+=(1)
        if(k_closest_screat[i]=='0'):
            calculation-=(1)
        else:
            calculation+=(1)

    return calculation<=0



olddata = list(csv.reader(open('heart.csv'))) #imports csv to matrix

data = np.delete(olddata, 0, 0)


# Keep in mind that having a higher ejection fraction is better as more blood leaving the heart means the muscle is NOT failing
# Having high secreation of creatine is bad because that means more muscle mass is deteriorating and entering bloodflow


alive = 0
avg_screat_alive = 0
avg_efrac_alive = 0

dead = 0
avg_efrac_dead = 0
avg_screat_dead = 0


for row in range(len(data)):
    if(data[row][12]=='0'):
        avg_efrac_alive+=float(data[row][4])
        avg_screat_alive+=float(data[row][7])
        alive+=1
    else:
        avg_efrac_dead+=float(data[row][4])
        avg_screat_dead+=float(data[row][7])
        dead+=1

avg_efrac_alive/=alive
avg_screat_alive/=alive

avg_efrac_dead/=dead
avg_screat_dead/=dead

print ("average of efract of those alive: " , avg_efrac_alive)
print ("average of efract of those dead: " , avg_efrac_dead)
print ("average of screat of those alive: " , avg_screat_alive)
print ("average of screat of those dead: " , avg_screat_dead)
print ("amt alive: ",alive)
print ("amt dead: ",dead)

print ("input patient's ejection fraction: ")
p_efrac = float(input())

print ("input the patient's creatine secretion: ")
p_screat = float(input())

print("depth of search: (1-100) ")
k = int(input())

#print(prediction(data,p_efrac,p_screat,k))

if(prediction(data,p_efrac,p_screat,k)):
    print("k_closest: will survive")
else:
    print("k_closest: will not survive")



