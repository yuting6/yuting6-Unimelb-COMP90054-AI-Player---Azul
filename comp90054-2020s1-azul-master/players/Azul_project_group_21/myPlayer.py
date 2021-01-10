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

# This file will be used in the competition
# Please make sure the following functions are well defined
# MCTS Version 7
# Chen-An Fan

from advance_model import *
from utils import *

class myPlayer(AdvancePlayer):
    counter = 0 
    
    # initialize
    # The following function should not be changed at all
    def __init__(self,_id):
        super().__init__(_id)
        
        
    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and 
    # you will receive a timeout warning
    def StartRound(self,game_state):
        
        return None

    # Each player is given 1 second to select next best move
    # If exceeds 5 seconds, all your code will be terminated, 
    # a random action will be selected, and you will receive 
    # a timeout warning
    def SelectMove(self, moves, game_state):
        #a copy of the current game state
        
        startTime = time.time()
        player_state = game_state.players[self.id]
        #copyGS = copy.deepcopy(game_state)
        #copyPS = copyGS.players[self.id]
        #copyPS = copy.deepcopy(player_state)
        
        opponentId = abs(self.id - 1)
        maxReward = 0
        best_move = random.choice(moves) #Randon initial the move

        for mid,fid,tgrab in moves:
            inTime = time.time()
            move = (mid,fid,tgrab)
            
            # Reset the player_state and grid_state to original one before any move
            copyGS = copy.deepcopy(game_state) # A new address
            copyPS = copyGS.players[self.id]   # A new address

            # Try to execute the move outside the main
            copyGS.ExecuteMove(self.id, move) #This will change and update the game state
            score = copyPS.ScoreRound()[0] #this will change the grid_state and the player_state
            bonus = copyPS.EndOfGameScore()
            reward = score + bonus

            futureReward = 0
            counter = 0
            discountFactor = 0
            i = abs(self.id - 1)

            while True:
                currentTime = time.time()
                #print(currentTime - inTime)
                if (currentTime - inTime) > (0.5 / len(moves)):
                    #print(currentTime - inTime)
                    #print("my time out")
                    break

                
                if not copyGS.TilesRemaining():
                    #print("end of the round")
                    break
                #result = self.simulatorAlwaysBest(copyGS, i)
                result = self.simulatorRandomMove(copyGS, i)
                i = abs(i-1)
                if (i == self.id):
                    counter = counter + 1
                    futureReward = result[1]
                    reward = reward + futureReward * (discountFactor**counter)
                else:
                    counter = counter + 1
                    futureReward = result[1]
                    reward = reward - futureReward * (discountFactor**counter)
                copyGS = result[0]
         
            if reward > maxReward:
                best_move = (mid,fid,tgrab)
                maxReward = reward
        
        return best_move
    

    # this is usd to execute the bestmove for one player
    def simulatorAlwaysBest(self, GS, opponentId):
        #should not modify the input game state
        #copyGS = copy.deepcopy(GS)
        #print("simulatro is running")
        copyGS  = GS
        # opponent turn
        opponnentPS = copyGS.players[opponentId]
        opponentMoves = opponnentPS.GetAvailableMoves(copyGS)
        oppMaxReward = 0
        oppBestMove = None
        for mid,fid,tgrab in opponentMoves:
            
            oppReward = 0
            oppMove = (mid,fid,tgrab)
            
            copyOppGS = copy.deepcopy(copyGS)#this should update and reset for every avaliable move
            
            copyOppPS = copyOppGS.players[opponentId]
            copyOppGS.ExecuteMove(opponentId, oppMove)
            oppScore = copyOppPS.ScoreRound()[0] #this will change the grid_state and the player_state
            oppBonus = copyOppPS.EndOfGameScore()
            oppReward = oppScore + oppBonus
            
            if oppReward >= oppMaxReward:
                oppBestMove = oppMove
                oppMaxReward = oppReward

        copyGS.ExecuteMove(opponentId, oppBestMove)

        return (copyGS, oppMaxReward)


        # this is usd to execute the bestmove for one player
    def simulatorRandomMove(self, GS, opponentId):
        #should not modify the input game state
        #copyGS = copy.deepcopy(GS)
        #print("simulatro is running")
        copyGS  = GS
        # opponent turn
        opponnentPS = copyGS.players[opponentId]
        opponentMoves = opponnentPS.GetAvailableMoves(copyGS)
        opponrntMove = random.choice(opponentMoves)

        copyGS.ExecuteMove(opponentId, opponrntMove)
        oppScore = opponnentPS.ScoreRound()[0] #this will change the grid_state and the player_state
        oppBonus = opponnentPS.EndOfGameScore()
        oppReward = oppScore + oppBonus
        return (copyGS, oppReward)