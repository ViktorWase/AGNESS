"""
    Let's see if we can find a way of
     developing a general board evaluation
     function for AGNESS.
"""
from random import random
from math import fabs
from math import exp

def tmpFunc(x):
    return x/(1.0+fabs(x))

def generalFuncANN(inp, w, dim, func):
    oldLayer = inp

    #Always add a one to avoid bias
    oldLayer.append(1.0)

    counter = 0
    for i in range(len(dim)-1):
        layer = [0.0]*dim[i]
        for j in range(len(layer)):
            for k in range(len(oldLayer)):
                layer[j] += oldLayer[k]*w[counter]
                counter += 1
            layer[j] = func(layer[j])
        oldLayer = list(layer) #Is this list-call necessary? FIX!

    #Final layer
    out = 0.0
    for i in range(dim[len(dim)-1]):
        out += layer[i]*w[counter]
        counter += 1
    return out


class boardEval:
    """

    """
    def __init__(self, vecIn, dimOfAnnIn, funcIn):

        #The weight vector for the ANN
        self.vec = list(vecIn)
        #The dimensions of the network.
        self.dimOfAnn = list(dimOfAnnIn)
        #The (hopefully) sigmoidal function used
        #in the ANN
        self.func = funcIn

    def returnCopy(self):
        return boardEval(self.vec, self.dimOfAnn, self.func)

    def eval(self, boardIn):
        """
            Evaluates the board and returns the chance
            of winning as a float between 0 (losing) and
            1 (winning)
        """
        board = list(boardIn)

        #Call the Artificial Neural Network
        out = generalFuncANN(board, self.vec, self.dimOfAnn, self.func)
        #Normalize to the interval [0, 1]
        out = exp(out) / (1.0 + exp(out))

        return out

    def errorFuncBoardEval(self, montePlayer):
        board = monteplayer.root.field
        annResult = self.eval(board)
        #Normalize the output from the exploration
        trueVal =(montePlayer.root.wins-montePlayer.root.losses)/(float(montePlayer.root.wins)+montePlayer.root.losses+montePlayer.root.draws)
        trueVal = (trueVal+1.0)/2.0
        output = (trueVal-annResult)*(trueVal-annResult)
        return output

board = [0]*9
board[2] = 1
v = [(random()-0.5)*20]*530
dim = [10]*6
B = boardEval(v, dim, tmpFunc)

chance = B.eval(board)

print board

print chance
