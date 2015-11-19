from parameters import *

from monteCarloPlayer import *
from pageRank import *
from random import *
import random


def morphAnnList2(AIs,surviving):
    """
        Takes the top half of the ANNs and gives
        them 2 children each.
    """
    #surviving = findTheMostFit(AIs,winCounterList)
    new_generation_ann = []
    ann_nr = 0
    for ann_nr in surviving:
        child = AIs[ann_nr].spawnChild()
        new_generation_ann.append(child)
        new_generation_ann.append(AIs[ann_nr])
    random.shuffle(new_generation_ann)
    return new_generation_ann

def writeToFile(fileName, AIs):
    text_file = open(fileName, "w")
    string =""
    for ai in AIs:
        string=string+str(ai.w)+"\n"
    string=string+"\n"
    for ai in AIs:
        string=string+str(ai.c)+"\n"
    string=string+"\n"
    for ai in AIs:
        string=string+str(ai.sigma)+"\n"
    text_file.write(string)
    text_file.close()

def morphAnnList(AIs,winCounterList):
    """
        Takes the top half of the ANNs and gives
        them 2 children each.
    """
    surviving = findTheMostFit(AIs,winCounterList)
    new_generation_ann = []
    for ann_nr in surviving:
        for child_nr in range(2):
            child = AIs[ann_nr].spawnChild()
            new_generation_ann.append(child)
    #FUCK YO SHUFFLE!
    #random.shuffle(new_generation_ann)
    return new_generation_ann

def ADHOC(ais):
    error = 0.0
    for ai in ais:
        error = error + (ai.c-1.4142135623730951)*(ai.c-1.4142135623730951)
    return error/len(ais)

def ADHOC2(ais):
    bestVal = 10000000.0
    for ai in ais:
        if abs(ai.c-1.414213)<bestVal:
            bestVal = abs(ai.c-1.4142135623730951)
    return bestVal

def EVOLUTION_BITCH(AIs, rules, numberOfGenerations):
    for gen in range(numberOfGenerations):
        error = ADHOC(AIs)
        print('\nGeneration: '),
        print gen
        print "Variance: ",
        print AIdist(AIs)
        print "Mean error in 2-norm: ",
        print error
        print "Smallest error in 1-norm: ",
        smallestError = ADHOC2(AIs)
        print smallestError
        winList = tournament(AIs, rules)

        if(gen != numberOfGenerations -1):
            nextGenAI = morphAnnList2(AIs,winList)
            AIs = nextGenAI
    return AIs

def AIdist(AIs):
    n = float(len(AIs[0].w))

    meanVar = 0.0
    for i in range(int(n)):
        tmp = 0.0
        mean = 0.0
        for j in range(len(AIs)):
            mean += AIs[j].w[i]
        mean = mean /float(n)
        for j in range(len(AIs)):
            tmp += (AIs[j].w[i]-mean)*(AIs[j].w[i]-mean)
        tmp = tmp / n
        meanVar += tmp
    meanVar = meanVar/float(len(AIs))
    return meanVar

r1 = Rules(1)

"""
NN = 90

w1 = [random.random() for col in range(NN)]
w2 = [random.random() for col in range(NN)]
w3 = [random.random() for col in range(NN)]
w4 = [random.random() for col in range(NN)]
w5 = [random.random() for col in range(NN)]
w6 = [random.random() for col in range(NN)]
w7 = [random.random() for col in range(NN)]
w8 = [random.random() for col in range(NN)]
w9 = [random.random() for col in range(NN)]
w10 = [random.random() for col in range(NN)]

c1 = random.random()*5
c2 = random.random()*5
c3 = random.random()*5
c4 = random.random()*5
c5 = random.random()*5
c6 = random.random()*5
c10 = random.random()*5
c9 = random.random()*5
c7 = random.random()*5
c8 = random.random()*5

p1 = montePlayer(w1,c1,random.random(), 1, r1)
p2 = montePlayer(w2,c2,random.random(), 1, r1)
p3 = montePlayer(w3,c3,random.random(), 1, r1)
p4 = montePlayer(w4,c4,random.random(), 1, r1)
p5 = montePlayer(w5,c5,random.random(), 1, r1)
p6 = montePlayer(w6,c6,random.random(), 1, r1)
p7 = montePlayer(w7,c7,random.random(), 1, r1)
p8 = montePlayer(w8,c8,random.random(), 1, r1)
p9 = montePlayer(w9,c9,random.random(), 1, r1)
p10 = montePlayer(w10,c10,random.random(), 1, r1)

AIs = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]

output = EVOLUTION_BITCH(AIs,r1,30)

print output[0].w
print output[0].c
print output[0].sigma
"""
NN = 90

w1 = [random.random() for col in range(NN)]
c1 = random.random()*5
coopPlayer = montePlayerCoop(w1,c1,random.random(), 1, r1)
store = -0.21342
for itt in range(1000):
    coopPlayer.root.explore(1)

    if store != coopPlayer.root.bestCulmValOfTerminalChild:
        store = coopPlayer.root.bestCulmValOfTerminalChild
        print store

"""
for ai in output:
    print ai.w
print "\n"
for ai in output:
    print ai.c
for ai in output:
    print ai.sigma
"""

print "Press the Enter key to quit."
raw_input()
