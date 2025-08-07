# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:37:42 2025
Filename : Code02
@author: 혁중
"""

import numpy as np

n1 = np.linspace( 0, 20, num=20 )
print( n1 )

n2 = np.linspace( 0, 20+1, num=20+1, endpoint=False )
print( n2 ) #헷갈리면 +1로 표기하면 좋음

n2[ [ range( 1, 10, 2 ) ] ]
print( n2[ [ range( 1, 10, 2 ) ] ] )

row, col = 5, 5
map = np.zeros( [ row, col ] )
# map
print( map )

map = np.zeros( [ row, col ], dtype=int )
print( map )

snow = np.ones( [ row, col ] )

for r in range( row ) :
     for c in range( col ) :
         if ( map[r][c] == 1 ) and ( snow[r][c] == 1 ) :
             map[r][c] = 0
             snow[r][c] = 0
print( map )
