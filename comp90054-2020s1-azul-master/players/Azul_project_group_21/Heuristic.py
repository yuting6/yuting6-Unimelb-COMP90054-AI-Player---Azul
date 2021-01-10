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
# 963125, Ruoqian Pan


class myPlayer(AdvancePlayer):

    # initialize
    # The following function should not be changed at all
    def __init__(self, _id):
        super().__init__(_id)

    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and
    # you will receive a timeout warning
    def StartRound(self, game_state):
        return None

    # Each player is given 1 second to select next best move
    # If exceeds 5 seconds, all your code will be terminated,
    # a random action will be selected, and you will receive
    # a timeout warning
    def SelectMove(self, moves, game_state):
        # return random.choice(moves)
        return self.heuristic_search(game_state, moves)

    def heuristic_search(self, game_state, available_moves):
        # score before make a move
        current_round_score = game_state.players[self.id].ScoreRound()[0]
        current_bonus_score = game_state.players[self.id].EndOfGameScore()

        best_move = None
        highest_score = float('-inf')
        # find a best move
        moves_cnt = len(available_moves)
        for i in range(moves_cnt):
            move = available_moves[i]

            # get a copy of the game_state to avoid change the original game state
            game_state_copy = deepcopy(game_state)
            game_state_copy.ExecuteMove(self.id, move)
            # player state after executing the specified move
            player = game_state_copy.players[self.id]
            tiles_grab = move[2]
            # move tiles to floor
            if tiles_grab.pattern_line_dest == -1:
                # round score
                round_score, used_tiles = player.ScoreRound()
                h = round_score - current_round_score
            # move tiles to pattern line
            else:
                tiles_grabbed = player.lines_number[tiles_grab.pattern_line_dest]
                tiles_needed = tiles_grab.pattern_line_dest + 1 - tiles_grabbed
                player.AddToPatternLine(tiles_grab.pattern_line_dest, tiles_needed, tiles_grab.tile_type)
                # round score
                round_score, used_tiles = player.ScoreRound()
                # bonus score
                bonus_score = player.EndOfGameScore()
                # current score minus prevous score, minus needed tiles
                h = round_score + bonus_score - current_round_score - current_bonus_score - tiles_needed
            # select a move with highest score
            if h > highest_score:
                highest_score = h
                best_move = move

