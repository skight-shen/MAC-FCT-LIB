import os
import sys

def test(t):
    if not t:
        print "can't be none"
        return 0
    list_1=[]
    for i in t:
        if i%2 != 0:
            list_1.append(i)
    return list_1

if __name__=='__main__':
    #assert test(None)
    t1 = [0,2,4,6,8]
    t2 = [-5,-3,-1,0]
    t3 = [0,0,0,0]
    t4 = [1.2,3.4,5.5]
    t5 = [-1.2,-3.4,-5.5]

    print test(t1)
    print test(t2)
    print test(t3)
    print test(t4)
    print test(t5)
    print test(t1+t2)
    print test(t1+t3)
    print test(t1+t4)
    print test(t1+t5)
    print test(t2+t3)
    print test(t2+t4)
    print test(t2+t5)
    print test(t3+t4)
    print test(t3+t5)
    print test(t4+t5)