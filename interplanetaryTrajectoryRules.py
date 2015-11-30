from lambertsProblem import lambert_problem
from positionOfPlanets import planetPosition

class Rules():
    """
        This is the rules that describe the
        interstellar trajectory planning
        problem as a board game.
        It should be noted that this board
        game is sucky as a board game for humans.
        It complicated and really hard.

        The simulation part is based on solving
        Lambert's problem. (As of now it only deals
        with max 1 revolutions and only prograde
        orbits. Might change later.)
        See the lambertsProblem.py-file for the
        implementation (which is stolen from ESA.)
    """
    def __init__(self, playerNr):
        self.playerNr = playerNr
        self.totalCost = 0.0
        #This will fill up with numbers but the
        #first element will always be a 1 or a 0.
        #A zero means it's time to choose a time,
        #and a 1 means it's time to choose a planet.
        self.manouvers = [0]
        #This shouldn't be in every cope of the rules, it's a waste of memory.
        self.orbitalPeriods = [7600530.24, 19440000.0, 31558149.504, 59360879.217024, 374279653.11744, 929703084.38784, 2651200139.83104, 5200783038.2592]
        #This sets the discretization of time. It should probably be bigger. FIX!
        self.dt = 20
        #This is the goal planet. Let's say Saturn for now.
        self.goalPlanet = 7
        #And it starts at Earth.
        self.startPlanet = 2
        #The probe will leave earth at noon of New Year's eve 1899.
        self.startTime = 0.0

    def returnAllLegalMoves(self, manouvers):
        if(manouvers[0] == 0):
            #An index for each time step.
            tmp = range(self.dt)
            tmp.pop(0) #timeOfFlight=0 ger skumma resultat. FIX!
            return tmp
        elif(manouvers[0] == 1):
            #An index for each planet. (Moons and dwarf planets
            # will be added at a later time).
            planetList = [0,1,2,3,4,5,6,7]

            #If we haven't gone anywhere we can't go to earth
            #can we? It's where we're at.
            if len(manouvers) < 3:
                planetList.pop(2)
            else:
                #Otherwise we simply remove the planet we're at.
                planetList.pop(manouvers[len(manouvers)-2])
            return planetList
        else:
            print "Huge error in returnAllLegalMoves"

    def getPlayerList(self):
        return [1,1]

    def nextPlayer(self):
        if(self.playerNr == 1):
            self.playerNr = 1
        else:
            self.playerNr = 1
    def otherPlayerNr(self):
        if(self.playerNr == 1):
            return 1
        else:
            return 1
    def getNewBoard(self):
        return [0]
    def isOver(self, manouvers):
        if (len(manouvers) % 2 == 1) and manouvers[len(manouvers)-1]==self.goalPlanet:
            return True
        else:
            return False

    def calcCost(self, manouvers):
        totalDeltaV = 0.0
        numOfMoves = (len(manouvers)-1)/2
        currentTime = self.startTime
        currentTimeIndex = 1
        nextPlanetIndex = 2
        currentPlanet = self.startPlanet
        v2_old = [0.0, 0.0, 0.0]
        #print "manouvers: ",
        #print manouvers
        for moveNr in range(numOfMoves):
            #print "MoveNr:",
            #print moveNr
            timeOfFlight = manouvers[currentTimeIndex]*self.orbitalPeriods[currentPlanet]/self.dt
            r1 = planetPosition(currentPlanet, currentTime)
            r2 = planetPosition(manouvers[nextPlanetIndex], currentTime+timeOfFlight)

            if(r1[0]==r2[0] and r1[1]==r2[1] and r1[2]==r2[2]):
                print "Wrong."
                return False
            #print "r",
            #print r1,
            #print r2
            #print "timeOfFlight:",
            #print timeOfFlight
            mu = 1.32712440018*pow(10,20)/(pow(149597870700.0,3))
            #print mu
            (v1, v2) = self.lambertSolver(r1,r2,timeOfFlight,mu) #The last one isn't right. FIX!
            totalDeltaV += self.calcDeltaV(v2_old, v1)
            v2_old = v2
            currentTime += timeOfFlight
            currentPlanet = manouvers[nextPlanetIndex]
            nextPlanetIndex += 2
            currentTimeIndex += 2
        #print "val:",
        #print 1.0/(1.0+100000*totalDeltaV)
        return 1.0/(1.0+100000*totalDeltaV)


    def calcDeltaV(self, v1, v2):
        out = 0.0
        for it in range(3):
            out += abs(v1[it]+v2[it])
        return out

    def lambertSolver(self, r1, r2, t, mu):
        (v1, v2) = lambert_problem(r1, r2, t, mu, False, 1) #This might be False or True. FIX!
        #deltaVs = []
        #for it in range(len(v1)):
        #    deltaVs.append(self.calcDeltaV(v1[it],v2[it]))
        #return min(deltaVs)
        return (v1[0], v2[0]) #There might be better ways of doing this.

    def returnValue(self, manouvers):
        if self.isOver(manouvers):
            return self.calcCost(manouvers)
        else:
            return 0.0

    def makeMove(self, manouvers, n, player):
        self.manouvers = list(manouvers)
        self.manouvers.append(n)
        if self.manouvers[0]==0:
            self.manouvers[0]=1
        elif self.manouvers[0]==1:
            self.manouvers[0]=0
        else:
            print "Error in make move!"
        return list(self.manouvers)
