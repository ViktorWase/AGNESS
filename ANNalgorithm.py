from random import random
from math import fabs

def sigmoidFunc(x):
        return x/(1.0+fabs(x))

def errorCheck(inp, h, li,w, isRandom):
    n = len(inp)
    if(isRandom == True):
        x = (n+2)*li[0]
    else:
        x = (n+1)*li[0]
    for i in range(h-1):
        x += li[i]*li[i]
    x += li[h-1]*1
    
    if(len(w)==x):
        return True
    else:
        print "EEEEEEEEEEEEEEEEEERROR IN ANN DIMENSIONS!"
        return False
    
def ANN(inp, hiddenLayers, nodesInHiddenLayers, weights,isRandom):
    #errorCheck(inp, hiddenLayers, nodesInHiddenLayers, weights, isRandom)
    
    oldLayer = inp
    
    #Always add a one to avoid bias
    oldLayer.append(1.0)

    #Sometimes add a random to instil fear in the hearts of your enemies
    if(isRandom):
        oldLayer.append(2.0*random()-1.0)

    counter = 0
    for i in range(hiddenLayers):
        layer = [0.0]*nodesInHiddenLayers[i]
        for j in range(len(layer)):
            for k in range(len(oldLayer)):
                layer[j] += oldLayer[k]*weights[counter]
                counter += 1
            layer[j] = sigmoidFunc(layer[j])
        oldLayer = list(layer)

    #Final layer
    out = 0.0
    for i in range(nodesInHiddenLayers[hiddenLayers-1]):
        out += layer[i]*weights[counter]
        counter += 1

    return sigmoidFunc(out)
        

#print ANN([0.1, 0.2], 1, [2], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], True)
    
