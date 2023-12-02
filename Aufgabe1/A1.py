
import random
import time


def myPrint(x):
    for i in x:
        print(i)
    print()


failCounter = 0
sackGassenCounter = 0


def addNum(x, i):
    global sackGassenCounter
    for t in range(n*n):
        oldX = x
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if x[a][b] == 0:
            x[a][b] = i
        else:
            continue


        # search way 
        counter = 0
        countFails = 0
        d = random.randint(0, 3) # next direction
        while counter < random.randint(2, int(n*2)) and countFails < 10:
            if random.randint(0,3) == 0:
                d = random.randint(0, 3) # next direction
            try:
                if d == 0: # up
                    if x[a -1][b] == 0 and a != 0:
                        x[a - 1][b] = -i
                        counter += 1
                        a -= 1
                        countFails = 0
                    else:
                        countFails += 1
                        d = random.randint(0, 3) # next direction
                if d == 1: # right
                    if x[a][b + 1] == 0:
                        x[a][b + 1] = -i
                        counter += 1
                        b += 1
                        countFails = 0
                    else:
                        countFails += 1
                        d = random.randint(0, 3) # next direction
                if d == 2: # down
                    if x[a + 1][b] == 0:
                        x[a + 1][b] = -i
                        counter += 1
                        a += 1
                        countFails = 0
                    else:
                        countFails += 1
                        d = random.randint(0, 3) # next direction
                if d == 3: # left
                    if x[a][b - 1] == 0 and b != 0:
                        x[a][b - 1] = -i
                        counter += 1
                        b -= 1
                        countFails = 0
                    else:
                        countFails += 1
                        d = random.randint(0, 3) # next direction
            except:
                countFails += 1


        if countFails > 0: # Sackgasse
            # remove all i
            sackGassenCounter += 1
            for j in range(n):
                for k in range(n):
                    if x[j][k] == i or x[j][k] == -i:
                        x[j][k] = 0
            continue



        
        try:
            if x[a+1][b] == i:
                x[a+1][b] = 0
                x[a][b] = 0
                continue
        except IndexError:
            pass
        try:
            if x[a-1][b] == i:
                x[a-1][b] = 0
                x[a][b] = 0
                continue
        except IndexError:
            pass
        try:
            if x[a][b+1] == i:
                x[a][b+1] = 0
                x[a][b] = 0
                continue
        except IndexError:
            pass
        try:
            if x[a][b-1] == i:
                x[a][b-1] = 0
                x[a][b] = 0
                continue
        except IndexError:
            pass
        x[a][b] = i
        return True
    return False


def make(n):
    a = []
    for i in range(n):
        b = []
        for j in range(n):
            b.append(0)
        a.append(b)
    return a



def create(n, k):
    global failCounter
    a = make(n)
    for i in range(1, k+1):
        if not addNum(a, i):
            failCounter += 1
            return create(n, k)
    
    for i in range(n):
        for j in range(n):
            if a[i][j]< 0:
                a[i][j] = 0
    return a



n = int(input("Geben Sie eine Zahl ein: "))
k = random.randint(int(n/2)+1, int(2*n))


start = time.time()

a = create(n, k)

end = time.time()
print("Time: ", end - start, " seconds")

print("There were ", failCounter, "fails,")
print("And me ran in ", sackGassenCounter, " Sackgassen ⛔️,")
print("But finally we made it:")

print()
print()
print(n)
print(k)
for i in range(n):
    for j in range(n):
        print(a[i][j], end=" ")
    print()