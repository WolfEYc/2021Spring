import random

print("depth:")
n = int(input())
c = 0

for _ in range(n):
    x = random.uniform(0,1)
    y = random.uniform(0,1)
    if(x*x+y*y<1):
        c+=1
print(4*c/n)


