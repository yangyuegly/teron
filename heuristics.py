from helper_functions import *
from constants import *
import numpy as np
from tronproblem import *
from collections import deque
import copy

def voronoi(state):
    # calculate "I" path cost
    gov_cost = dijkstra(state, 0)
    gov_points = 0
    # calculate "OPP" path cost
    opp_cost = dijkstra(state, 1)
    opp_points = 0
    board = state.board
    for r in range(1, len(board)-1):
        for c in range(1, len(board[0])-1):
            if gov_cost[r, c] < opp_cost[r, c]:
                gov_points += 1
            if opp_cost[r, c] < gov_cost[r, c]:
                opp_points += 1
    print(gov_points)
    print(opp_points)
    return (float(gov_points-opp_points))/(gov_points+opp_points)


def dijkstra(state, player_num):
    state_copy =copy.deepcopy(state)
    curr_board = state_copy.board
    loc = state_copy.player_locs[player_num]

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
            if visited[l[0], l[1]] == 0:
                all_vertices.append(l)
                visited[l[0], l[1]] = 1

    return dists


def get_next_state(curr_board, loc):
    # print('curr loc:'+str)
    next_locs = []
    for move in TronProblem.get_safe_actions(curr_board, loc):
        next_loc = TronProblem.move(loc, move)
        #print('move: '+move+' loc: '+str(next_loc))
        next_locs.append(next_loc)

    # print("next_locs:")
    # print(next_locs)
    return next_locs
