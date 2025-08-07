# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 15:37:07 2025

@author: ktar343
"""

import numpy as np
c = np.array( [ 1, 2, 3, 4, 5 ] )
 # np.where
find_c1 = np.where( c > 3 )
find_c2 = np.where( c > 3, 10, -10 )
find_c3 = np.where( c > 3, True, False )
find_c4 = np.where( c > 3, 1, 0 )
 # np.extract 
ext_c1 = np.extract( c > 3, c )
print( f'find_c1={find_c1}' )
print( f'find_c2={find_c2}' )
print( f'find_c3={find_c3}' )
print( f'find_c4={find_c4}' )

print( ext_c1 )

import numpy as np
import matplotlib.pyplot as plt
c = np.array( [ 1, 2, 3, 4, 5 ] )
 # np.where
find_c4 = np.where( c > 3, 1, 0 )
plt.plot( c, '*' )
plt.plot( find_c4, '*' )
#plt.show()


plt.xlabel( xlabel='Xlabel' )
plt.ylabel( ylabel='Ylabel' )
plt.title( label='TITLE')
plt.show()