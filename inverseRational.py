# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:52:00 2016

implements rational camera inverse mapping

@author: sebalander
"""
# %%
import numpy as np


# %%
def inverseRational(u, v, cameraMatrix, distCoeffs):
    '''
    inverseRational(u, v, cameraMatrix, distCoeffs) -> X,Y
    takes position (u,v) in image and returns (X,Y,0) in scene
    '''
    xpp = (u-cameraMatrix[0,2]) / cameraMatrix[0,0]
    ypp = (v-cameraMatrix[1,2]) / cameraMatrix[1,1]
    rpp = np.sqrt(xpp**2 + ypp**2)
    
    # polynomial coeffs
    # # (k1,k2,p1,p2[,k3[,k4,k5,k6[,s1,s2,s3,s4[,τx,τy]]]])
    p = [distCoeffs[4,0],
         -rpp*distCoeffs[7,0],
         distCoeffs[1,0],
         -rpp*distCoeffs[6,0],
         distCoeffs[0,0],
         -rpp*distCoeffs[5,0],
         1,
         -rpp]
    
    roots = np.roots(p)
    
#    # max radious possible
#    rppMax = np.sqrt((cameraMatrix[0,2] / cameraMatrix[0,0])**2 +
#                     (cameraMatrix[1,2] / cameraMatrix[1,1])**2)
    
    rp_rpp = roots[np.isreal(roots)]/rpp # asume real positive root, in interval
    
    xp = xpp*rp_rpp
    yp = ypp*rp_rpp
    
    # auxiliar calculations
    a = cameraMatrix[0,0] - cameraMatrix[2,0] * xp
    b = cameraMatrix[0,1] - cameraMatrix[2,1] * xp
    c = cameraMatrix[0,2] - cameraMatrix[2,2] * xp
    d = cameraMatrix[1,0] - cameraMatrix[2,0] * yp
    e = cameraMatrix[1,1] - cameraMatrix[2,1] * yp
    f = cameraMatrix[1,2] - cameraMatrix[2,2] * yp
    q = a*e-d*b
    
    X = (c*e - f*b)/q
    Y = (f*a - c*d)/q
    
    return X,Y