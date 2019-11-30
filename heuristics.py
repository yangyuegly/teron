from helper_functions import *
from constants import *
import numpy as np
from tronproblem import *
from collections import deque
import copy

def voronoi(state,initial_player):
    # calculate "I" path cost
    gov_cost,gov_trap = dijkstra(state, initial_player)
    gov_points = 0
    # calculate "OPP" path cost
    opp_cost,opp_trap = dijkstra(state, 1-initial_player)
    opp_points = 0
    board = state.board
    for r in range(1, len(board)-1):
        for c in range(1, len(board[0])-1):
            if gov_cost[r, c] < opp_cost[r, c]:
                gov_points += 1
            if opp_cost[r, c] < gov_cost[r, c]:
                opp_points += 1
   #gov_points += gov_trap
   # opp_points += opp_trap
    if have_armor(state,initial_player):
        gov_points+=10
        print('reached')
    return ((float(gov_points-opp_points))/(gov_points+opp_points))/2.0+0.5


def trap(state,player_num):
    trap_is_good = True
    gov_loc = state.player_locs[player_num]
    opp_loc = state.player_locs[1-player_num]
    if(abs(gov_loc[0]-opp_loc[0])<=2 or abs(gov_loc[1]-opp_loc[1])<=2):
        trap_is_good = False
    return trap_is_good

def have_armor(state,initial_player):
    if state.player_has_armor(initial_player):
        print("yes")
        return True
    else:
        return False

def dijkstra(state, player_num):
    trap_is_good = trap(state,player_num)
    state_copy =copy.deepcopy(state)
    curr_board = state_copy.board
    loc = state_copy.player_locs[player_num]
    trap_val = 0
    # distances to all non-starting vertices are inifinit
    dists = np.zeros((HEIGHT, WIDTH))
    dists[:, :] = np.inf

    # set the distance to 0 for the current state
    dists[loc[0], loc[1]] = 0

    visited = np.zeros((HEIGHT, WIDTH))

    # set distance for neighboring cells
    all_vertices = deque(get_next_state(curr_board, loc))
    for initial_loc in all_vertices:
        dists[initial_loc[0], initial_loc[1]] = 1

    while(all_vertices):
        curr = all_vertices.popleft()
        curr_dist = dists[curr[0], curr[1]] + 1
        for l in get_next_state(curr_board, curr):
            if curr_dist < dists[l[0], l[1]]:
                dists[l[0], l[1]] = curr_dist
                if(state.board[curr[0]][curr[1]]==CellType.TRAP) and trap_is_good:
                    trap_val += 10.0*(1/curr_dist)
            
            if visited[l[0], l[1]] == 0:
                all_vertices.append(l)
                visited[l[0], l[1]] = 1

    return dists,trap_val


def get_next_state(curr_board, loc):
    next_locs = []

    for move in TronProblem.get_safe_actions(curr_board, loc):
        next_loc = TronProblem.move(loc, move)
        next_locs.append(next_loc)

    return next_locs
