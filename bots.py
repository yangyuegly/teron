#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
from constants import *
import random
import math
from heuristics import *

# Throughout this file, ASP means adversarial search problem.
# Trap *;
# Armor @: used automatically once the player travel thru a barrier, not walls(#) or other players
# Speed ^; 4 mandatory consecutive turns
#  Bomb ! destroy all barriers in 9*9 square surrounding the bomb


class StudentBot:
    """ Write your student bot here"""

    def __init__(self, cutoff=6):
        order = ["D", "U", "R", "L"]
        self.cutoff = cutoff

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        return self.alpha_beta(asp, self.cutoff)

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
        loc = locs[player_num]
        first_actions = list(TronProblem.get_safe_actions(board, loc))
        if asp.is_terminal_state(state):
            return None

        best_action = None
        best_score = LOSE

        for action in first_actions:
            child_state = asp.transition(state, action)
            result = self.min_value(
                asp, child_state, alpha, beta, player_num, cutoff-1)
            alpha = max(alpha, result)
            if result >= best_score:
                best_score = result
                best_action = action
        return best_action

    def max_value(self, asp, state, alpha, beta, player_num, cutoff):
        # print(dijkstra(state, 0))
        if cutoff <= 0:
            voronoi_val = voronoi(state)
            print("voronoi"+str(voronoi_val))
            return voronoi_val if (voronoi_val != 0) else simple_eval_function(asp, state, player_num)
        if asp.is_terminal_state(state):
            print('reached_terminal_state')
            print(state)
            return asp.evaluate_state(state)[player_num]  # max's turn

        locs = state.player_locs
        loc = locs[player_num]
        actions = list(TronProblem.get_safe_actions(state.board, loc))
        optimal_action = LOSE

        for action in actions:
            child_state = asp.transition(state, action)
            curr = self.min_value(
                asp, child_state, alpha, beta, player_num, cutoff-1)
            if curr > optimal_action:
                optimal_action = curr
            if optimal_action >= beta:
                return optimal_action
            alpha = max(alpha, optimal_action)

        return optimal_action

    def min_value(self, asp, state, alpha, beta, player_num, cutoff):
        if cutoff <= 0:
            voronoi_val = voronoi(state)
            print("voronoi"+str(voronoi_val))
            return voronoi_val if (voronoi_val != 0) else simple_eval_function(asp, state, player_num)
        if asp.is_terminal_state(state):
            print('reached_terminal_state')
            print(state)
            return asp.evaluate_state(state)[player_num]  # min's turn

        locs = state.player_locs
        loc = locs[player_num]
        actions = list(TronProblem.get_safe_actions(state.board, loc))
        optimal_action = LOSE

        for action in actions:
            child_state = asp.transition(state, action)
            curr = self.max_value(
                asp, child_state, alpha, beta, player_num, cutoff-1)
            if curr < optimal_action:
                optimal_action = curr
            if optimal_action <= alpha:
                return optimal_action
            beta = min(beta, optimal_action)
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
        pass


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
