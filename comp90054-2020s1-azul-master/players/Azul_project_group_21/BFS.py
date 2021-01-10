# Written by Michelle Blom, 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# 1066384, Yu-Ting Liu

from advance_model import *
import utils
import copy


#This is a player implementing Blind Search algorithm "BFS"
#To avoid the timeout and memory overwhelming issue, we set some bounds to adjust it.
class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    def StartRound(self, game_state):

        return None

    def SelectMove(self, moves, game_state):



        #num_of_moves = len(moves) #因為每一小輪到後面move都剩比較少，所以可以往下多探幾層

        myqueue = []

        copyGS = copy.deepcopy(game_state)
        startState = copyGS
        path = []
        path.append(moves[0])  # root node has no execuuted moves, so put a default move
        index_of_move = []
        index_of_move.append(0) #紀錄path裡面每一個move在當初moves裡面的index
        cost = 0
        copyPS = startState.players[self.id]

        layer = len(path)

        new_startState = []
        # new_startState = state(GS) + PS + path + index_of_move + cost + layer
        new_startState.append(startState)
        new_startState.append(copyPS)
        new_startState.append(path)
        new_startState.append(index_of_move)
        new_startState.append(cost)

        new_startState.append(layer)

        myqueue.insert(0, new_startState)

        self_id = self.id
        min_cost = 0
        goal_state = new_startState

        #紀錄scan過幾個node
        count = 0

        while not len(myqueue) == 0:
            if count == 500: #限制最多只跑500個node
                break
            new_state = myqueue.pop()  # state(GS) + PS + path + index_of_move + cost + layer
            #goal_state = new_state ###
            state = new_state[0]
            #node = new_state[0]
            P_state = new_state[1]  # represents that now is whcih player's turn to move
            path = new_state[2]
            index_of_move = new_state[3]
            cost = new_state[4]

            layer = new_state[5]
            #用限制層數避免overwhelming
            if layer > 3:
                break


            # 結束條件
            if state.TilesRemaining():


                if cost < min_cost:
                    min_cost = cost
                    goal_state = new_state

                state_player_id = P_state.id
                successors, local_moves = get_copy_Successors(state_player_id, state)
                costs = get_cost(self_id, state_player_id, state, successors)

                for i in range(len(successors)):
                    succState = successors[i]
                    if state_player_id == 0:
                        succ_P_state = succState.players[1]
                    else:
                        succ_P_state = succState.players[0]
                    moveToThisSucc = local_moves[i]
                    succ_path = []
                    for x in path:
                        succ_path.append(x)
                    succ_path.append(moveToThisSucc)  # original path + the move to this succ.
                    succ_index = []
                    for index in index_of_move:
                        succ_index.append(index)
                    succ_index.append(i)
                    succCost = cost + costs[i]

                    succ_layer = len(succ_path)

                    new_succ_state = []
                    new_succ_state.append(succState)
                    new_succ_state.append(succ_P_state)
                    new_succ_state.append(succ_path)
                    new_succ_state.append(succ_index)
                    new_succ_state.append(succCost)
                    new_succ_state.append(succ_layer)
                    myqueue.insert(0, new_succ_state)

            count += 1

        index_of_moves = goal_state[3]

        if len(index_of_moves) < 2:
            index_of_best_first_move = index_of_moves[0]
        else:
            index_of_best_first_move = index_of_moves[1] #應該要1因為0是default值

        best_move = moves[index_of_best_first_move]
        return best_move



def get_copy_Successors(id, state):
    successors = []  #also is game state
    return_moves = []
    copy_GS = copy.deepcopy(state)  # make a copy of every state
    PS = copy_GS.players[id]
    moves = PS.GetAvailableMoves(copy_GS)
    for i in range(len(moves)):
        local_copyGS = copy.deepcopy(state) #make a copy of every state
        local_PS = local_copyGS.players[id]
        local_moves = local_PS.GetAvailableMoves(local_copyGS)
        local_copyGS.ExecuteMove(id, local_moves[i]) #this copyGS will be updated
        successors.append(local_copyGS)
        return_moves.append(local_moves[i])
    return successors, return_moves


#應該會影響算法好壞
def get_cost(self_id, id, state, successors):
    costs = []
    #如果當前做這個move的player是我們算法的player, 分數增加cost就是負數, 反之為正數
    #如果當前做這個move的player是對手, 則分數增加cost就是正數, 反之為負數
    if id == self_id:
        for suc in successors:
            cost = -(suc.players[id].ScoreRound()[0] - state.players[id].ScoreRound()[0])
            costs.append(cost)
    else:
        for suc in successors:
            cost = (suc.players[id].ScoreRound()[0] - state.players[id].ScoreRound()[0])
            costs.append(cost)
    return costs
