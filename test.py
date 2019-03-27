import sys,random

class Candidate:
    def __init__(self, id, score, lst=[]):
        self.id = id
        self.score = score
        self.lst = lst

    def __str__(self):
        #return "\n".join(x for x in self.lst) + str(self.id) + "-" + str(self.score)
        return str(self.id) + "-" + str(self.score)

    def getlst(self):
        return len(self.lst)

def sortScore(val):
    return val.score

def main(argv):
    lst=[]
    i = 1
    n=int(argv[0])
    k=int(argv[1])
    # for _ in range(n):
    #     score = random.randrange(1,50)
    #     lst.append(Candidate(i,score))
    #     i = i + 1
    
    # for x in lst:
    #     print(x)
    # print("_-----------------------------------")
    # lst.sort(key = sortScore)
    # for x in lst:
    #     print(x.id)

    for i in range(1,n+1):
        lst.append(i)
    maxmin(lst,k)
    lst = process(lst,k)
    print(lst)

def process(lst,k):
    goalstate = []
    n = len(lst)
    if n > 3:
        if n%3 == 0:
            pass
        else:
            pass
    else:
        first,second=[],[] # first is list of even number - second -> odd number
        for x in range(0,len(lst)):#[0-8] example of n = 8
            if x%2 !=0:
                first.append(lst[x])     #even number
            else:
                second.append(lst[x])    #odd number
        first = second + first[::-1]
        second =[]
        for x in first:
            second.append(x)
        second.append(first[0])
        del second[0]
        goal1 = list(zip(first,second))
        goal2 = list(zip(second,first))
        for x,y in list(zip(goal1,goal2)):
            goalstate.append(x)
            goalstate.append(y)
        goalstate.insert(0,goalstate[-1])
        del goalstate[-1]
        return goalstate

    


def maxmin(lst,k):
    n = len(lst)
    nol = n / k
    

main(sys.argv[1:])