#from keplerian_elements_jpl import KEPLERIAN_PARAMETERS
import ephem
from math import *

planetGravitationalParameterList = [2.20329*10**13,3.248599*10**14,3.9860044189*10**14,4.28289*10**13,6.26325*10**10,1.266865349*10**17,3.79311879*10**16,5.7939399*10**15,6.8365299*10**15]

def planetGravitationalParameter(planetNr):
    """
        Returns the standard gravitational parameter
        of the planet. IT is measured in m^3/s^2
    """
    return planetGravitationalParameterList[planetNr]

def planetVelocity(planetNr, time):
    """
        Finds the velocity of a planet.

        The planetNr is 0-index and time
        is measured in seconds from noon
        Universal Time on the last day of
        1899. Because why not.

        The output is a 3D-vector measured in
        meters per second.
    """
    if(planetNr == 0):
        planet = ephem.Mercury()
    elif(planetNr == 1):
        planet = ephem.Venus()
    elif(planetNr == 2):
        return [0.0, 0.0, 0.0]
        #return [149597870700.0,0.0,0.0]
    elif(planetNr == 3):
        planet = ephem.Mars()
    elif(planetNr == 4):
        planet = ephem.Jupiter()
    elif(planetNr == 5):
        planet = ephem.Saturn()
    elif(planetNr == 6):
        planet = ephem.Uranus()
    elif(planetNr == 7):
        planet = ephem.Neptune()
    else:
        print "Fuck"
        return False
    planet.compute(time/(3600.0*24.0))
    r = planet.sun_distance#*149597870700.0
    b = float(planet.hlat)
    l = float(planet.hlon)

    x1 = r*cos(b)*cos(l)
    y1 = r*cos(b)*sin(l)
    z1 = r*sin(b)
    planet.compute((time-3600)/(3600.0*24.0))
    r = planet.sun_distance#*149597870700.0
    b = float(planet.hlat)
    l = float(planet.hlon)

    x2 = r*cos(b)*cos(l)
    y2 = r*cos(b)*sin(l)
    z2 = r*sin(b)
    return [(x1-x2)/3600.0, (y1-y2)/3600.0, (z1-z2)/3600.0]

def planetPosition(planetNr, time):
    """
        Finds the position of a planet.

        The planetNr is 0-index and time
        is measured in seconds from noon
        Universal Time on the last day of
        1899. Because why not.

        The output is a 3D-vector measured in
        meters where the earth is always in the
        [149597870700, 0, 0] posistion. (I think).
    """
    if(planetNr == 0):
        planet = ephem.Mercury()
    elif(planetNr == 1):
        planet = ephem.Venus()
    elif(planetNr == 2):
        return [1.0, 0.0, 0.0]
        #return [149597870700.0,0.0,0.0]
    elif(planetNr == 3):
        planet = ephem.Mars()
    elif(planetNr == 4):
        planet = ephem.Jupiter()
    elif(planetNr == 5):
        planet = ephem.Saturn()
    elif(planetNr == 6):
        planet = ephem.Uranus()
    elif(planetNr == 7):
        planet = ephem.Neptune()
    else:
        print "Fuck"
        return False
    planet.compute(time/(3600.0*24.0))
    r = planet.sun_distance#*149597870700.0
    b = float(planet.hlat)
    l = float(planet.hlon)

    x = r*cos(b)*cos(l)
    y = r*cos(b)*sin(l)
    z = r*sin(b)
    return [x,y,z]
    #para = KEPLERIAN_PARAMETERS[2*planetNr]
    #paraChange = KEPLERIAN_PARAMETERS[2*planetNr+1]
