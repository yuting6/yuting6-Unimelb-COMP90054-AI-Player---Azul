# This file will be used in the competition
# Please make sure the following functions are well defined
# MCTS Version 6
# Chen-An Fan 1087032

from advance_model import *
from utils import *


class myPlayer(AdvancePlayer):
    counter = 0 #count how many action has this player done
    #grid_color = -1
    #reward = 0
    
    # initialize
    # The following function should not be changed at all
    def __init__(self,_id):
        super().__init__(_id)
        
        #self.grid_color = -1
        #self.reward = 0
        #self.pt = PlayerTrace(self.id)
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
        #move傳進來已經是avaliable move了
        #a copy of the current game state
        
        startTime = time.time()
        player_state = game_state.players[self.id]
        #copyGS = copy.deepcopy(game_state)
        #copyPS = copyGS.players[self.id]
        #copyPS = copy.deepcopy(player_state)
        
        opponentId = abs(self.id - 1)
        
        
        myGridState = player_state.grid_state #這是做動作之前的State看此有沒有東西
        #copyGrid = copyPS.grid_state
        myGridScheme = player_state.grid_scheme
        maxReward = 0
        best_move = random.choice(moves) #Randon initial the move
        #print("==================new action====================")
        #beforeForTime = time.time()
        #print(beforeForTime - startTime)
        for mid,fid,tgrab in moves:
            inTime = time.time()
            move = (mid,fid,tgrab)
            
            # Reset the player_state and grid_state to original one before any move
            copyGS = copy.deepcopy(game_state) # A new address
            copyPS = copyGS.players[self.id]   # A new address
           
            ##preGridState = copy.deepcopy(copyPS.grid_state) #for debug
            #print(preGridState)
            # Try to execute the move outside the main
            copyGS.ExecuteMove(self.id, move) #This will change and update the game state
            score = copyPS.ScoreRound()[0] #this will change the grid_state and the player_state
            bonus = copyPS.EndOfGameScore()
            reward = score + bonus

            #print("score = " + str(score))
            #print("bonus = " + str(bonus))
            #print("reward = " + str(reward))
            #afeGridState = copyPS.grid_state
            #print(preGridState)
            #print("---")
            #print(afeGridState)
            #print(preGridState == afeGridState)
            #print("==============between move========================")
            ##print("number of moves: ")
            ##print(len(moves))
            futureReward = 0
            counter = 0
            discountFactor = 0.1
            i = abs(self.id - 1)
            #beforewhileTime = time.time()
            #print(beforewhileTime-inTime)
            #while (time.time()-inTime) > (5 / len(moves)):
            while True:
                currentTime = time.time()
                #print(currentTime - inTime)
                if (currentTime - inTime) > (0.5 / len(moves)):
                    #print(currentTime - inTime)
                    #print("my time out")
                    break
                #print("hello")
                
                if not copyGS.TilesRemaining():
                    #print("end of the round")
                    break
                counter = counter + 1
                #result = self.simulatorAlwaysBest(copyGS, i)
                result = self.simulatorRandomMove(copyGS, i)
                i = abs(i-1)
                if (i == self.id):
                    futureReward = result[1]
                    reward = reward + futureReward * (discountFactor**counter)
                copyGS = result[0]
                #print(time.time()-currentTime)
                #print(reward)

                
            

            '''
            #Here is the opponent
            opponnentPS = copyGS.players[opponentId]
            opponentMoves = opponnentPS.GetAvailableMoves(copyGS)
            oppMaxReward = 0
            oppBestMove = None
            for mid,fid,tgrab in opponentMoves:
                oppReward = 0
                (mid,fid,tgrb) = oppMove
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
            '''
            if reward > maxReward:
                best_move = (mid,fid,tgrab)
                maxReward = reward

        #copyGS = copy.deepcopy(game_state)
        #myPS = copyGS.players[self.id]
        #copyGS.ExecuteMove(self.id, best_move) #update the game state
        #opponnentPS = copyGS.players[opponentId]
        #opponentMoves = opponnentPS.GetAvailableMoves(copyGS)

        #print(moves[1])這是可以的!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        
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