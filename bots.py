#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
from constants import *
import random
import math
from heuristics import *
import copy

# Throughout this file, ASP means adversarial search problem.
# Trap *;
# Armor @: used automatically once the player travel thru a barrier, not walls(#) or other players
# Speed ^; 4 mandatory consecutive turns
#  Bomb ! destroy all barriers in 9*9 square surrounding the bomb


class StudentBot:
    """ Write your student bot here"""

    def __init__(self, cutoff=4):
        order = ["D", "U", "R", "L"]
        self.step = 0
        self.cutoff = cutoff
        self.BOT_NAME = "Moon River"
    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        self.step +=1
            
        return self.alpha_beta(asp, self.cutoff) if self.step>=5 else self.alpha_beta(asp, 1)

    def alpha_beta(self, asp, cutoff):  # propogate backwards
        """
            alpha-beta cutoff
        """

        alpha = LOSE
        beta = WIN
        state = asp.get_start_state()
        locs = state.player_locs

        board = state.board
        player_num = state.ptm
        initial_player = state.ptm
        loc = locs[player_num]
        first_actions = list(TronProblem.get_safe_actions(board, loc))
        if asp.is_terminal_state(state):
            return None

        best_action = None
        best_score = LOSE

        for action in first_actions:
            child_state = asp.transition(state, action)
            child_num = child_state.ptm

            result = self.min_value(
                asp, child_state, alpha, beta, child_num, cutoff-1,initial_player)
            
            print("first action: "+action + " result:" +str(result))
            
            alpha = max(alpha, result)
        
            if result >= best_score:
                best_score = result
                best_action = action
        return best_action

    def max_value(self, asp, state, alpha, beta, player_num, cutoff,initial_player):
#        print("player_num="+str(player_num))
        player_num = state.ptm

#        print("state.ptm="+str(player_num))
        if asp.is_terminal_state(state):
            #print(state.board)
            print('cutoff'+str(cutoff))
            print('reached_terminal_state')
            print("initial player num: " + str(initial_player))
            return asp.evaluate_state(state)[initial_player]  # max's turn
        if cutoff <= 0:
            voronoi_val = voronoi(state)
            print("voronoi"+str(voronoi_val))
            return voronoi_val 


        locs = state.player_locs
        loc = locs[player_num]
        actions = list(TronProblem.get_safe_actions(state.board, loc))
        optimal_action = LOSE
        print("cutoff:"+ str(cutoff))
        print("max action")
        print(actions)
        if(len(actions)==0):
            actions = ["R"]
        for action in actions:
            child_state = asp.transition(state, action)
            child_num = child_state.ptm
        #    print("cutt off from max: "+str(cutoff))

            curr = self.min_value(
                asp, child_state, alpha, beta, child_num, cutoff-1,initial_player)

            print("action:"+ action)
            print("curr comparison: "+str(curr))
            if curr > optimal_action:
                optimal_action = curr

            print("optimal comparison: "+str(optimal_action))

            if optimal_action >= beta:
                return optimal_action
            alpha = max(alpha, optimal_action)
        #if cutoff==1:
            # print("optimal_action_val: "+ str(optimal_action))
        return optimal_action

    def min_value(self, asp, state, alpha, beta, player_num, cutoff,initial_player):
        player_num = state.ptm
        locs = state.player_locs
        loc = locs[player_num]

#        print("min player num: " + str(player_num))
        if asp.is_terminal_state(state):
            print('reached_terminal_state')
            print(asp.evaluate_state(state)[initial_player])
            print("initial player num: " + str(initial_player)) 
            return asp.evaluate_state(state)[initial_player]  # min's turn
        if cutoff <= 0:
            voronoi_val = voronoi(state)
            print("voronoi"+str(voronoi_val))
            return voronoi_val
        #locs = state.player_locs
        #loc = locs[player_num]
        actions = list(TronProblem.get_safe_actions(state.board, loc))
        print(actions)
        optimal_action = WIN
        if(len(actions)==0):
            actions = ["R"]
        for action in actions:
            child_state = asp.transition(state, action)
            child_num = child_state.ptm
 #           print("min child num: " + str(child_num))
#            print("cutt off from max: "+str(cutoff))

            curr = self.max_value(
                asp, child_state, alpha, beta, child_num, cutoff-1,initial_player)
            # if(cutoff==1):
            #     print("player:" + str(child_num))
            #     print("curr_action_val: "+ str(curr)) 
            if curr < optimal_action:
                optimal_action = curr
            if optimal_action <= alpha:
                return optimal_action
            beta = min(beta, optimal_action)
            # if cutoff==1:
            #     print("min optimal_action_val: "+ str(optimal_action))
        return optimal_action
    
    def simple_eval_function(self, asp, state, player_num):
        """
        return the number of available actions as the value of the state
        """
        locs = state.player_locs
        loc = locs[player_num]
        actions = list(TronProblem.get_safe_actions(state.board, loc))
        evaluation = len(actions)
        print("evaluation: " + str(evaluation))
        return evaluation/2.0

    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        self.step = 0


class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
