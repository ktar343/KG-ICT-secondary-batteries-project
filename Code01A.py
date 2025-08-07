# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:23:56 2025
Filename : Code01A
@author: 혁중
"""

import pandas as pd
import numpy as np

row = 7
column = 5

map = np.zeros( [ row, column ] )

map[1][2] = 1
map[2][3] = 1
map[4][ [1,2,3] ] = 1
map[6][4] = 1

print ( '* map * \n' , map )

df = pd.DataFrame( map ) #이렇게하면 맵을 직접입력하지 않고 받아올수도
df.to_csv( 'map.csv' )
print( df, type(df) )
print ( '* df *\n', df,'\n', '* type(df) *\n', type(df) )

df = pd.DataFrame( map ) #여기 넣으면 실수로 바뀌는구나
df.to_csv( 'code01A.csv' ) #뭔가를 파일로 저장했겠구나
print( df, type(df) )
print ( '* df *\n', df,'\n', '* type(df) *\n', type(df) )

df = df.astype(int)
df.to_csv( 'code01Aint.csv' )
print ( '* df *\n', df,'\n', '* type(df) *\n', type(df) )

snow = np.ones( [ row, column ] ) #ones써서 사람 다 지워지는 문제
print ( '* snow * \n' , snow )

for r in range( row ) :
    for c in range( column ) :
        if ( map[r][c] == 1 ) and ( snow[r][c] == 1 ) :
            map[r][c] = 0
            snow[r][c] = 0

print ( '* map * \n' , map )