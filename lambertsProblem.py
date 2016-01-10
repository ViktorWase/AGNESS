"""
This file solves Lambert's problem using the algorithm developed by ESA for
their PyKEP library, but using Python instead of C++.

/*****************************************************************************
 *   Copyright (C) 2004-2015 The PyKEP development team,                     *
 *   Advanced Concepts Team (ACT), European Space Agency (ESA)               *
 *                                                                           *
 *   https://gitter.im/esa/pykep                                             *
 *   https://github.com/esa/pykep                                            *
 *                                                                           *
 *   act@esa.int                                                             *
 *                                                                           *
 *   This program is free software; you can redistribute it and/or modify    *
 *   it under the terms of the GNU General Public License as published by    *
 *   the Free Software Foundation; either version 2 of the License, or       *
 *   (at your option) any later version.                                     *
 *                                                                           *
 *   This program is distributed in the hope that it will be useful,         *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of          *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           *
 *   GNU General Public License for more details.                            *
 *                                                                           *
 *   You should have received a copy of the GNU General Public License       *
 *   along with this program; if not, write to the                           *
 *   Free Software Foundation, Inc.,                                         *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.               *
 *****************************************************************************/
 """

from math import acos
from math import asin
from math import sinh
from math import asinh
from math import acosh
from math import log
from math import sqrt
from math import sin

def norm(vec):
    norm = 0.0
    out = list(vec)
    for it in xrange(3):
        norm += vec[it]*vec[it]
    return sqrt(norm)

def normalizedCopy(vec):
    l = norm(vec)
    out = list(vec)
    for it in range(3):
        out[it] = vec[it]/l
    return out

def crossProd(a, b):
    out = [0.0, 0.0, 0.0]
    out[0] = -a[2]*b[1]+a[1]*b[2]
    out[1] = a[2]*b[0]-a[0]*b[2]
    out[2] = -a[1]*b[0]+a[0]*b[1]
    return out

# Constructor
"""
Constructs and solves a Lambert problem.

 \param[in] R1 first cartesian position
 \param[in] R2 second cartesian position
 \param[in] tof time of flight
 \param[in] mu gravity parameter
 \param[in] cw when 1 a retrograde orbit is assumed
 \param[in] multi_revs maximum number of multirevolutions to compute
"""
def lambert_problem(r1, r2, tof, mu, cw, multi_revs):
    M_PI = 3.14159265359
    m_r1=list(r1)
    m_r2=list(r2)
    if tof<=0.0:
        print "Faulty time input in Lambert"
        return False
    m_tof=tof
    m_mu=mu
    m_has_converged=True
    m_multi_revs=multi_revs
    # 0 - Sanity checks
    if(tof <= 0):
	       print "Time of flight is negative!"
    if (mu <= 0):
	       print "Gravity parameter is zero or negative!"
	# 1 - Getting lambda and T
    m_c = sqrt( (r2[0]-r1[0])*(r2[0]-r1[0]) + (r2[1]-r1[1])*(r2[1]-r1[1]) + (r2[2]-r1[2])*(r2[2]-r1[2]))
    R1 = norm(m_r1)
    R2 = norm(m_r2)
    m_s = (m_c+R1+R2) / 2.0
    #array3D ir1,ir2,ih,it1,it2;
    ir1 = normalizedCopy(r1)
    ir2 = normalizedCopy(r2)
    #print "ir",
    #print ir1,
    #print ir2
    ih = crossProd(ir1,ir2)
    ih = normalizedCopy(ih)
    if (ih[2] == 0):
        print "The angular momentum vector has no z component, impossible to define automatically clock or counterclockwise"
    lambda2 = 1.0 - m_c/m_s
    m_lambda = sqrt(lambda2);
    if (ih[2] < 0.0): # Transfer angle is larger than 180 degrees as seen from above the z axis
        m_lambda = -m_lambda
        it1 = crossProd(ir1,ih)
        it2 = crossProd(ir2,ih)
    else:
        it1 = crossProd(ih,ir1)
        it2 = crossProd(ih,ir2)
    it1 = normalizedCopy(it1)
    it2 = normalizedCopy(it2)

    if (cw): # Retrograde motion
        m_lambda = -m_lambda
        it1[0] = -it1[0]
        it1[1] = -it1[1]
        it1[2] = -it1[2]
    	it2[0] = -it2[0]
        it2[1] = -it2[1]
        it2[2] = -it2[2]
    lambda3 = m_lambda*lambda2

    T = sqrt(2.0*m_mu/m_s/m_s/m_s) * m_tof
    #print "hej2",
    #print T,
    #print m_mu,
    #print m_tof
    #print lambda3
    # 2 - We now have lambda, T and we will find all x
    # 2.1 - Let us first detect the maximum number of revolutions for which there exists a solution
    m_Nmax = int((T/M_PI)) #Removed round(). FIX!
    #print "m_Nmax:",
    #print m_Nmax
    #print lambda3
    T00 = acos(m_lambda) + m_lambda*sqrt(1.0-lambda2)
    #print lambda3
    T0 = (T00 + m_Nmax*M_PI)
    #print lambda3
    T1 = 2.0/3.0 * (1.0 - lambda3)
    DT = 0.0
    DDT = 0.0
    DDDT = 0.0
    if (m_Nmax > 0):
        if (T < T0): # We use Halley iterations to find xM and TM
            it=0
            err = 1.0
            T_min=T0
            x_old=0.0
            x_new = 0.0
            while (True):
                (DT,DDT,DDDT) = dTdx(x_old,T_min, m_lambda)
                if (DT != 0.0):
                    x_new = x_old - DT * DDT / (DDT * DDT - DT * DDDT / 2.0)
                err=abs(x_old-x_new)
                if ( (err<1e-13) or (it>12) ):
                    break
                T_min = x2tof(T_min,x_new,m_Nmax, m_lambda)
                x_old=x_new
                it+=1
            if (T_min > T):
                m_Nmax -= 1
	# We exit this if clause with Mmax being the maximum number of revolutions
	# for which there exists a solution. We crop it to m_multi_revs
    m_Nmax = min(m_multi_revs,m_Nmax)

	# 2.2 We now allocate the memory for the output variables
    m_v1 = [[0.0 for x in range(3)] for y in range(int(round(m_Nmax*2+1)))] # m_v1.resize(m_Nmax * 2 +1)
    m_v2 = [[0.0 for x in range(3)] for y in range(int(round(m_Nmax*2+1)))] # m_v2.resize(m_Nmax * 2 +1)
    m_iters = [[0.0 for x in range(3)] for y in range(int(round(m_Nmax*2+1)))] # m_iters.resize(m_Nmax * 2 +1)
    m_x = [[0.0 for x in range(3)] for y in range(int(round(m_Nmax*2+1)))] # m_x.resize(m_Nmax * 2 +1)

	# 3 - We may now find all solutions in x,y
	# 3.1 0 rev solution
	# 3.1.1 initial guess
    if (T>=T00):
        m_x[0] = -(T-T00)/(T-T00+4)
    elif (T<=T1):
        #print "is zero? :",
        #print (1-lambda2*lambda3)
        #print lambda2
        #print lambda3
        #print T
        m_x[0] = T1*(T1-T) / ( 2.0/5.0*(1-lambda2*lambda3) * T ) + 1
    else:
        m_x[0] = pow((T/T00),0.69314718055994529 / log(T1/T00)) - 1.0
	# 3.1.2 Householder iterations
    (m_iters[0], m_x[0]) = householder(T, m_x[0], 0.0, 1e-5, 15, m_lambda)
	# 3.2 multi rev solutions
    tmp=0.0

    for i in range(m_Nmax+1):
        if(i!=0):
            #3.2.1 left Householder iterations
            tmp = pow((i*M_PI+M_PI) / (8.0*T), 2.0/3.0)
            m_x[2*i-1] = (tmp-1)/(tmp+1)
            (m_iters[2*i-1], m_x[2*i-1]) = householder(T, m_x[2*i-1], i, 1e-8, 15, m_lambda)
            #3.2.1 right Householder iterations
            tmp = pow((8.0*T)/(i*M_PI), 2.0/3.0)
            m_x[2*i] = (tmp-1)/(tmp+1)
            (m_iters[2*i], m_x[2*i]) = householder(T, m_x[2*i], i, 1e-8, 15, m_lambda)

	# 4 - For each found x value we reconstruct the terminal velocities
    gamma = sqrt(m_mu*m_s/2.0)
    rho = (R1-R2) / m_c
    sigma = sqrt(1.0-rho*rho)
	#vr1,vt1,vr2,vt2,y;
    for i in range(len(m_x)):
        y = sqrt(1.0-lambda2+lambda2*m_x[i]*m_x[i])
        vr1 = gamma *((m_lambda*y-m_x[i])-rho*(m_lambda*y+m_x[i]))/R1
        vr2 = -gamma*((m_lambda*y-m_x[i])+rho*(m_lambda*y+m_x[i]))/R2
        vt = gamma*sigma*(y+m_lambda*m_x[i])
        vt1 = vt/R1
        vt2 = vt/R2
        for j in range(3):
            m_v1[i][j] = vr1 * ir1[j] + vt1 * it1[j]
        for j in range(3):
            m_v2[i][j] = vr2 * ir2[j] + vt2 * it2[j]
    return (m_v1, m_v2);

def x2tof2(tof, x, N, m_lambda):
    a = 1.0/(1.0-x*x)
    M_PI = 3.14159265359
    if(a>0):
        alfa = 2.0 * acos(x)
        beta = 2.0 * asin(sqrt(m_lambda*m_lambda/a))
        if(m_lambda < 0.0):
            beta = -beta
        tof = ((a*sqrt(a)*((alfa - sin(alfa))-(beta-sin(beta)) + 2.0*M_PI*N))/2.0)
    else:
        alfa = 2.0*acosh(x)
        beta = 2.0*asinh(sqrt(-m_lambda*m_lambda/a))
        if(m_lambda <0.0):
            beta = -beta
        tof = ( -a * sqrt (-a)* ( (beta - sinh(beta)) - (alfa - sinh(alfa)) ) / 2.0)
    return tof

def householder(T, x0,  N, eps, iter_max, m_lambda):
    it=0
    err = 1.0
    xnew=0.0
    tof=0.0
    delta=0.0
    DT=0.0
    DDT=0.0
    DDDT=0.0
    while ( (err>eps) and (it < iter_max) ):
        tof = x2tof(tof,x0,N, m_lambda)
        (DT, DDT, DDDT) = dTdx(x0,tof, m_lambda)
        delta = tof-T
        DT2 = DT*DT
        xnew = x0 - delta * (DT2-delta*DDT/2.0) / (DT*(DT2-delta*DDT) + DDDT*delta*delta/6.0)
        err=abs(x0-xnew)
        x0=xnew
        it+=1;
    return (it, x0);

def dTdx(x,T, m_lambda):
    l2 = m_lambda*m_lambda
    l3 = l2*m_lambda
    umx2 = 1.0-x*x
    y = sqrt(1.0-l2*umx2)
    y2 = y*y
    y3 = y2*y
    DT = 1.0/umx2 * (3.0*T*x-2.0+2.0*l3*x/y)
    DDT = 1.0 / umx2 * (3.0*T+5.0*x*DT+2.0*(1.0-l2)*l3/y3)
    DDDT = 1.0 / umx2 * (7.0*x*DDT+8.0*DT-6.0*(1.0-l2)*l2*l3*x/y3/y2)
    out = (DT, DDT, DDDT);
    return out

def hypergeometricF(z, tol):
    Sj=1.0
    Cj=1.0
    err=1.0
    Cj1=0.0
    Sj1=0.0
    j=0
    while (err > tol):
        Cj1 = Cj*(3.0+j)*(1.0+j)/(2.5+j)*z/(j+1)
        Sj1 = Sj + Cj1
        err=abs(Cj1)
        Sj = Sj1
        Cj=Cj1
        j=j+1
    return Sj

def x2tof(tof, x, N, m_lambda):
    M_PI = 3.14159265359
    battin = 0.01
    lagrange = 0.2
    dist = abs(x-1)
    if (dist < lagrange and dist > battin): # We use Lagrange tof expression
        #print "FUCKELINI!!!!!!"
        tof = x2tof2(tof,x,N, m_lambda)
        return tof
    K = m_lambda*m_lambda
    E = x*x-1.0
    rho = abs(E)
    z = sqrt(1.0+K*E)
    if (dist < battin): # We use Battin series tof expression
        eta = z-m_lambda*x
        S1 = 0.5*(1.0-m_lambda-x*eta)
        Q = hypergeometricF(S1,1e-11)
        Q = 4.0/3.0*Q
        tof = (eta*eta*eta*Q+4.0*m_lambda*eta)/2.0 + N*M_PI / pow(rho,1.5)
        return tof
    else: # We use Lancaster tof expresion
        y = sqrt(rho)
        g = x*z - m_lambda*E
        d = 0.0
        #print E
        if (E<0):
            l = acos(g)
            d=N*M_PI+l
        else:
            f = y*(z-m_lambda*x)
            #print "-----1"
            #print y
            #print z
            #print m_lambda
            #print x
            #print "-------"
            #print E
            #print f
            #print g
            d=log(f+g)

    	tof = (x-m_lambda*z-d/y)/E
    	return tof
"""
(v1, v2) = lambert_problem([100.0, 0.0, 0.0], [0.0, 10000.0, 0.0], 100.0, 0.00001, 1, 1)
print v1
print v2
print findDeltaV(v1[0], v2[0])
print len(v1)
"""
