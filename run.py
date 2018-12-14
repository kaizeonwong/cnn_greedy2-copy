# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 17:26:44 2018

@author: 01379055
"""

import numpy as np
from a_star import Array2D, AStar, Point
from env import Env
import random

CONF = {
    'world_size': 12,
    'capacity': 10,
    'player1_home': (5, 5),
    'player2_home': (6, 6),
    'num_walls': 24,
    'num_jobs': 24,
    'value_range': (6, 12),
    'max_steps': 200
    }

                    
    
def get_distance(x,y,x_target,y_target,big_list):
    path= big_list[(x,y,x_target,y_target)]
    steps = len(path)
    return steps
   
    
def get_all_package(map_0):
    
    positions = []
    for x in range(0,12):
        for y in range(0,12):
            if map_0[x,y]>0:
                positions.append((x,y))
    return positions


def find_nearest_package(x,y,map_0,big_list):
    package_positions = get_all_package(map_0)
    min_step = get_distance(x,y,package_positions[0][0],package_positions[0][1],big_list)
    for p in package_positions:
        min_step = min(min_step,get_distance(x,y,p[0],p[1],big_list))  
    return min_step

def get_map2d(map_0):
    print('oooooooooooooooooooooo')
    map2d = Array2D(12, 12)
    for x in range(0,12):
        for y in range(0,12):
            if map_0[x][y]==-1:
                map2d[y][x] = 1
                
    return map2d


def get_all_paths(map2d):

    big_list=dict()
    for x_start in range(0,12):   
        for y_start in range(0,12): 
            for x_end in range(0,12): 
                for y_end in range(0,12):
                    if x_start == x_end and y_start == y_end:
                        continue
                    elif map2d[x_start][y_start] == 1 or map2d[x_end][y_end] == 1:
                        continue
                    astar = AStar(map2d, Point(x_start, y_start), Point(x_end, y_end))
                    try:
                        path_list = [(p.y, p.x) for p in astar.start()]
                    except:
                        continue
                    big_list[(y_start, x_start, y_end, x_end)] = path_list
#    print(list(big_list.keys())[10], big_list[list(big_list.keys())[10]])
    return big_list  
        

def go_home(map2d, x,y,home_x,home_y):
    
    print(x, y)
    astar = AStar(map2d, Point(y, x), Point(home_y, home_x))
    path_list = [(p.y, p.x) for p in astar.start()]
    
    print(path_list)
#    action = "S"
    if path_list[0][0]==x:
        if path_list[0][1] > y:
            action='R'
        else:
            action='L'
    else:
        if path_list[0][0] > x:
            action='D'
        else:
            action='U'
    
    return action
    
    
    
def CNN_path (map_info,x1,y1,n,player,big_list,map2d,step):
    map_0=map_info
    
    
    if player == 'player1':
        if n>5 :
            map_0[5,5]=150
    else :
        if n>5 :
            map_0[6,6]=150
 
    
    if n>=10:
        if player == 'player1':
            action=go_home(map2d,x1,y1,5,5)
        else :
            action=go_home(map2d, x1,y1,6,6)    
    else:
        map_x=np.zeros(shape=(24,24))
        for x in range(6,18):
            for y in range(6,18):
                map_x[x,y]=map_0[x-6,y-6]
        map_true=np.zeros(shape=(11,11))
        for x in range(0,11):
            for y in range(0,11):
                map_true[x,y]=map_x[x1+1+x,y1+1+y]
            
        x=x1
        y=y1    
        
        map_1=CNN_cal(map_true,map_x,0,x,y)
        map_2=CNN_cal(map_1,map_x,1,x,y)
        map_3=CNN_cal(map_2,map_x,2,x,y)
        map_4=CNN_cal(map_3,map_x,3,x,y)
        

        print(map_true)
        print(map_1)
        print(map_2)
        print(map_3)
        print(map_4)
        
        min_step = find_nearest_package(x,y,map_0,big_list)
        if min_step==1:
            action=get_action(map_0,x,y)
            
        else:
            action=get_action(map_4,5,5) 
    
    if (200-step)<50:      
        if player == 'player1':
            if (x1, y1) != (5, 5):
                print("#######cal home_step")
                home_steps = get_distance(x1,y1,5,5,big_list)
                print("home_steps: ", home_steps)
                print("left step: ", 200 - step)
                if 200-step-2 <= home_steps <= 200-step:
                    action=go_home(map2d,x1,y1,5,5)
        else :
            if (x1, y1) != (6, 6):
                home_steps = get_distance(x1,y1,6,6,big_list)
                if 200-step-2 <= home_steps <= 200-step:   
                    action=go_home(map2d, x1,y1,6,6) 
            
    
    return action


def CNN_cal(map_x,map_org,v,x1,y1):
    new_map=np.zeros(shape=(11,11))
    for x in range(v,9-v):
        for y in range(v,9-v):
            new_map[x+1,y+1]=(map_x[x,y]+map_x[x+1,y]+map_x[x+2,y]+map_x[x,y+1]+map_x[x+1,y+1]+map_x[x+2,y+1]+map_x[x,y+2]+map_x[x+1,y+2]+map_x[x+2,y+2])
            
            if map_org[x+2+x1,y+2+y1]==-1:
                new_map[x+1,y+1]=-1
    return new_map


def get_action(use_map0,x,y):
    
    print('jiaoluo')
    print(use_map0)
#    if x == 0:
#        U0=-1
#        D0=use_map0[x+1,y]
#        L0=use_map0[x,y-1]
#        R0=use_map0[x,y+1]
#    elif x == 11:
#        U0=use_map0[x-1,y]
#        D0=-1
#        L0=use_map0[x,y-1]
#        R0=use_map0[x,y+1]
#    elif y==0:
#        U0=use_map0[x-1,y]
#        D0=use_map0[x+1,y]
#        L0=-1
#        R0=use_map0[x,y+1]
#    elif y==11:
#        U0=use_map0[x-1,y]
#        D0=use_map0[x+1,y]
#        L0=use_map0[x,y-1]
#        R0=-1
#    else:
#        U0=use_map0[x-1,y]
#        D0=use_map0[x+1,y]
#        L0=use_map0[x,y-1]
#        R0=use_map0[x,y+1]
        
    U0, D0, L0, R0 = -1, -1, -1, -1
    if 0 < x:
        U0 = use_map0[x-1,y]
    if x < 11:
        D0 = use_map0[x+1,y]
    if 0 < y:
        L0 = use_map0[x,y-1]
    if y < 11:
        R0 = use_map0[x,y+1]
   
    a01=int(max(U0,D0,L0,R0)==U0)
    a02=int(max(U0,D0,L0,R0)==D0)
    a03=int(max(U0,D0,L0,R0)==L0)
    a04=int(max(U0,D0,L0,R0)==R0)
    
    if a01+a02+a03+a04 == 1:
        if a01==1:
            Move='U'
        elif a02==1:
            Move='D'
        elif a03==1:
            Move='L'
        elif a04==1:
            Move='R'

    else :
        
        list1=[]
        if a01==1:
            list1.append('U')
        if a02==1:
            list1.append('D')
        if a03==1:
            list1.append('L')
        if a04==1:
            list1.append('R')
        Move=np.random.choice(list1)
    
    return Move



