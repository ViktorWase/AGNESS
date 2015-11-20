"""
    The functions in this file are used to
    train AGNESS using an evolutionary
    algorithm.
"""
import random

def optimize(AIs, rules, iterations):
    """
        Evolutionary optimization using roulette
        wheel selection and elitism.
    """
    for generation in range(iterations):
        winList = tournament(AIs, rules)
        newAIs = []

        #Find and keep the best one
        bestIndex = -1
        bestVal =-1
        for j in range(len(AIs)):
            if winList[j] > bestVal:
                bestVal = winList[j]
                bestIndex = j
        newAIs.append(AIs[bestIndex])

        #Use roulette wheel selection on the rest
        culmProb = list(winList)
        culmSum = 0.0
        for j in range(len(culmProb):
            culmSum += winList[j]
            culmProb[j] = culmSum
        for j in range(len(culmProb)):
            culmProb[j] = culmProb[j]/culmProb[len(culmProb)-1]
        for j in range(len(AIs)-1):
            AIindex1 = rouletteWheelChoose(culmProb)
            AIindex2 = rouletteWheelChoose(culmProb)
            newAIs[j+1] = evolutionaryReproduction(AIs[AIindex1], AIs[AIindex2])
        AIs = newAIs

def rouletteWheelChoose(culmProb):
    r = random.random()
    counter = 0
    while culmProb[counter]< r:
        counter += 1 #Check if this is correct. FIX!
    return counter
