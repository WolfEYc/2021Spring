def findDupes(a):
    tortoise = a[0]
    hare = a[a[0]]
    while (tortoise!=hare):
        tortoise = a[tortoise]
        hare = a[a[hare]]
    print (a[tortoise])

# code will find and print guarunteed duplicate of list of ints 1 to n-1 of size n
a = input().split()

for num in range(len(a)):
    a[num] = int(a[num])

findDupes(a)