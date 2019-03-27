import errno, sys, os
import random, time
import math  
class Candidate:
    def __init__(self, id, score, lst=None):
        self.id = id
        self.score = score
        self.lst = list()

    def __str__(self):
        return str(self.id) + "-" + ":".join(str(x) for x in self.lst) + "-" +str(sum(self.lst))

    def getlst(self):
        return len(self.lst)
    
    def addlst(self, value):
        self.lst.append(value)
    def reset(self):
        self.lst = []

#def main(file_input, file_output):
def main(argv):
    # read input
    # generatetest(file_input)
    lst = []
    ls = []
    #n, k, lst = readFile(file_input)
    n=int(argv[0])
    k=int(argv[1])
    
    if (n*k % 2 != 0 or k >= n or k < 1 ):
        print("Can not schedule for contestants because number of battle is invalid")
        sys.exit()
    # run algorithm

    for x in range(1,n+1):
        lst.append(x)
    #print(lst)
    for x in range(1,n+1):
        ls.append(Candidate(x,x))
    
    result = schedule(lst,n,k,ls)
    #print(result)
    for item in ls:
        for x,y in result:
            if x == item.id:
                item.lst.append(y)
            if y == item.id:
                item.lst.append(x)
        
    # write output
    print("-----------------------------------")
    for x in ls:
        print(x)
    #print(result)
    print("-----------------------------------")
    print("The total number of batles: {}".format(len(result)))
    print("-----------------------------------")
    print("The number of candidates: {}".format(n))
    print("The battle of each contestant: {}".format(k))
    print("-----------------------------------")

#------------------------------------------------------------------------------------------
def schedule(lst, n, k, ls):               #lst : list of candidates
    goalstate=[]                                        # goal state
    while n > k and k > 0:
        #--------k = 1 -------------------pass----------
        if (k == 1):# best-choice
            first, second =[],[]
            i, j = 0, n-1
            while j >= i:
                first.append(lst[i])
                second.append(lst[j])
                i += 1
                j -= 1
            first = list(zip(first,second))
            for x in first:
                goalstate.append(x)
            return goalstate
        #---------k = 2----------------------pass
        elif (k == 2): 
            left, right = 0, len(lst)-1
            #print(lst)
            while left <= right:
                if right == left + 1:
                    lst[left], lst[right] = lst[right], lst[left]
                elif right != left + 2:
                    lst[left], lst[left+1] = lst[left+1], lst[left]
                    lst[right], lst[right-1] = lst[right-1], lst[right] 
                left += 2
                right -= 2
                #check2k(ls, lst)
            #create each couple of contestant
            #print(lst)
            temp=[]
            for item in lst[1:n]:
                temp.append(item)
            temp.append(lst[0])
            temp = list(zip(lst,temp))
            for x in temp:
                goalstate.append(x)
            return goalstate
        #-------k = n/2----------pass-----# [12345678]-->[1234]--[5678]
        elif (n == 2*k):
            first,second =[],[]
            temp=[]
            for i in range(0,len(lst)):
                if i < n/2:
                    first.append(lst[i])
                else:
                    second.append(lst[i])
            # optimize sum of 2 list ~~
            left, right = 0, len(second)-1
            pivot = math.ceil(((sum(second) - sum(first))/2) + 0.1)
            while right > 0:
                while left < len(first):
                    if (second[right]-first[left] <= pivot):
                        pivot -= second[right]-first[left]
                        first[left], second[right] = second[right], first[left]
                        left += 1
                        break
                    left += 1
                right -= 1
            # zip 2 list 
            temp = [(x,y) for x in first for y in second]
            for x in temp:
                goalstate.append(x)
            return goalstate
        
        #---------k = n - 1--------------------------pass
        elif (k == n-1): 
            temp, resul=[], []
            for x in lst:
                temp.append(x)
            for x in lst:
                val = temp.pop(0)
                lis = [(val,y) for y in temp]
                resul += lis
            for x in resul:
               goalstate.append(x)
            return goalstate
        #-------k > n/2 ------------------------pass----
        elif (n < 2*k and k != n - 1):
            #print(lst)
            first, second = [], []
            splitpoint = n - k
            k_2 = k - splitpoint
            for i in range(0, splitpoint):
                first.append(lst[i])
            for i in range(splitpoint, n):
                second.append(lst[i])
            
            # total list first and k2 element of second_list
            sum_first = sum(first)
            sum_second = 0 # sum of k element of second_list. Not is total of second_list
            for x in range(-k_2,0):
                sum_second += second[x]
            
            # print(first)
            # print(second)
            end_second = k - 1
            end_first = splitpoint -1
            while (sum(second) > (sum_second + sum_first)):
                #swap first[end] and second[end]
                first[end_first], second[end_second] = second[end_second], first[end_first]
                #pop end element and add to first of two list
                second = [second.pop(end_second)] + second  
                first = [first.pop(end_first)] + first
                # total list first and k2 element of second_list
                sum_first = sum(first)
                sum_second = 0 # sum of k element of second_list. Not is total of second_list
                for x in range(-k_2,0):
                    sum_second += second[x]
                
            # print(first)
            # print(second)
            temp = []
            for x in first:
                temp += [(x,y) for y in second]
            goalstate += temp

            # update lst of second and k_2
            lst = []
            for x in second:
                lst.append(x)
            k = k_2
            n = len(second)

        
        #---------k < n/2----------------------k is even-------------
        elif (n > 2*k and n%2 == 0 and k != 1 and k != 2):
            # idea : divice it into two part : k+1 | n-k-1  --> best choice
            first =[]
            for x in range(0,k+1):
                first.append(lst[0])
                lst.pop(0)
            second = lst         #change name to easily understand
            #-----cmt--------
            # print("---")
            # print("{}-{}".format(first,findmaxmin(first,k)))
            # print("{}-{}".format(second,findmaxmin(second,k)))
            # print("---")
            #-------------
            #optimize (max,min) when comparing 2 list
            i = 0
            while(sum(first[0:k]) < sum(second[0:k])):
                first[i], second[i] = second[i], first[i]
                i += 1

            i = k-1
            first.sort()
            second.sort()
            first = first[::-1]
            second = second[::-1]
            
            while((sum(first[0:k]) < sum(second[0:k])) and i >= 0):
                first[i], second[i] = second[i], first[i]
                i -= 1
            first.sort()
            second.sort()
            
            first = schedule(first,len(first),k,ls)
            goalstate += first
            second = schedule(second,len(second),k,ls)
            goalstate += second
            return goalstate

        #---------k < n/2----------------------k is odd-------------
        elif (n > 2*k and n%2 != 0 and k != 1 and k != 2):
            a = lst.pop(n/2)
            first, second = [], []
            for _ in range(0, (n-1)/2):
                first.append(lst[0])
                lst.pop(0)
            second = lst
            i = len(first) - 1
            while (sum(first) < sum(second)) and i >= 0 :
                first[i], second[i] = second[i], first[i]
                i -= 1
            
            second.sort()
            # first = [1,2,8,9]
            # second = [3,4,6,7]
            # a = 5

            # Schedule for list by role
            temp = list([(a,x) for x in first])
            goalstate += temp
            temp = list(zip(first,second))
            goalstate += temp
            
            first = schedule(first,len(first),k-2,ls)
            goalstate += first
            second = schedule(second,len(second),k-1,ls)
            goalstate += second
            return goalstate
        
    return goalstate

#------------------------------------------------------------------------------------------
def findmaxmin(lst,k):
    lst.sort()
    return sum(lst[0:k]) , sum(lst[::-1][0:k])


def check2k(ls , lst):
    print(lst)
    n = len(ls)
    temp =[]
    for item in lst[1:n]:
        temp.append(item)
    temp.append(lst[0])
    result = list(zip(lst,temp))
    for item in ls:
        for x,y in result:
            if x == item.id:
                item.lst.append(y)
            if y == item.id:
                item.lst.append(x)
    
    for x in ls:
        print(x)
        x.reset()
    print("---------------")

def readFile(file_input):
    if not os.path.isfile(file_input):
       print("File path {} does not exist. Exiting...".format(file_input))
       sys.exit()
    list =[]
    try:
        with open(file_input,"r") as f:
            line = f.readline()
            n = int(line.split(" ")[0])
            k = int(line.split(" ")[1])
            i = 1
            while i <= n:
                line = f.readline()
                list.append(Candidate(i, str(line), []))
                i += 1
        return n, k, list
    except IOError as x:
        if x.errno == errno.ENOENT:
            print('{}- does not exist'.format(file_input))
        elif x.errno == errno.EACCES:
            print('{}- cannot be read'.format(file_input))
        else:
            print('{}- some other error'.format(file_input))
        sys.exit()

def writeFile(file_output, data):
    if file_output == "":
        print("file output is not valid")
        sys.exit()
    if os.path.isfile(file_output):
        os.remove(file_output)
    
    with open(file_output,"w") as fw:
        if isinstance(data,list):
            fw.write("\n".join(str(x) for x in data))
        else:
            fw.write(str(data))
        fw.close()
    
def generatetest(file_input):
    lst=[]
    for x in range(8):
        lst.append(str(random.randrange(50)))
    writeFile(file_input,lst)


if __name__ == "__main__":
    #main('input.txt', 'output.txt')
    start_time = time.time() 
    main(sys.argv[1:])
    end_time = time.time()
    print ('total run-time: %f ms' % ((end_time - start_time) * 1000))
    '''
    # Driver code to test above 
    arr = [10, 7, 8, 9, 1, 5] 
    n = len(arr) 
    quickSort(arr,0,n-1) 
    print ("Sorted array is:") 
    for i in range(n): 
        print ("%d" %arr[i]), 
    '''
