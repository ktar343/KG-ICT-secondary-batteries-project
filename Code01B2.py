# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:22:56 2025
Filename : Code01B2
@author: 혁중
"""

import pandas as pd
import numpy as np

row = 9
column = 7

map = np.zeros( [ row, column ] )

map[1][2] = 1
map[2][3] = 1
map[4][ [1,2,3] ] = 1
map[6][4] = 1

print ( '* map * \n' , map )

snow = np.ones( [ row, column ] )
#ones써서 사람 다 지워지는 문제
print ( '* snow * \n' , snow )

for r in range( row ) :
    for c in range( column ) :
        if ( map[r][c] == 1 ) and ( snow[r][c] == 1 ) :
            map[r][c] = 0
            snow[r][c] = 0

print ( '* map * \n' , map )