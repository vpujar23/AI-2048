from game_grid import Grid
import numpy as np
import Helper_func
from random import randint
import time
import matplotlib.pyplot as plt
import numpy

initialTiles = 2
(Agent, Opponent) = (0, 1)
possibleDirections = {0: "UP", 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}
timeLimit = 1
prob = 0.9
max_tiles_array = []
game_itr = []


class user():
    def getMove(self, grid):
        copygrid = []
        for i in range(4):
            copygrid.extend(grid.map[i])
        [child, moves] = Helper_func.selectchildren(copygrid)
        maxpath = -np.inf
        direction = 0
        for i in range(len(child)):
            c = child[i]
            m = moves[i]
            highest_value = -np.inf
            maxdepth = 4
            # highest_value = Minimax.calculate(c, maxdepth, False)
            highest_value = Alpha_Beta_Prune.calculate(c, maxdepth, -np.inf, np.inf, False)
            if m == 0 or m == 2:
                highest_value += 10000
            if highest_value > maxpath:
                direction = m
                maxpath = highest_value

        return direction

class Opponent_agent():
    def getMove(self, grid):
        cells = grid.Empty_tiles()
        if cells:
            return cells[randint(0, len(cells) - 1)]
        else:
            None


class Minimax_algo():
    def calculate(grid, depth, isMax):
        if depth == 0:
            return Helper_func.heuristics(grid)
        if not Helper_func.checkvalidmove(grid):
            return Helper_func.heuristics(grid)
        if isMax:
            bestValue = -np.inf
            [child, moving] = Helper_func.selectchildren(grid)
            for ch in child:
                bestValue = max(bestValue, Minimax_algo.calculate(ch, depth - 1, False))
            return bestValue
        else:
            cells = [i for i, x in enumerate(grid) if x == 0]
            child = []
            bestValue = np.inf
            for c in cells:
                temp = list(grid)
                temp[c] = 2
                child.append(temp)
                temp = list(grid)
                temp[c] = 4
                child.append(temp)
            for ch in child:
                bestValue = min(bestValue, Minimax_algo.calculate(ch, depth - 1, True))
            return bestValue


class Alpha_Beta_Prune():
    def calculate(grid, depth, alpha, beta, isMax):
        if depth == 0:
            return Helper_func.heuristics(grid)
        if not Helper_func.checkvalidmove(grid):
            return Helper_func.heuristics(grid)
        if isMax:
            bestValue = -np.inf
            [child, moving] = Helper_func.selectchildren(grid)
            for ch in child:
                bestValue = max(bestValue, Alpha_Beta_Prune.calculate(ch, depth - 1, alpha, beta, False))
                if bestValue >= beta:
                    return bestValue
                alpha = max(alpha, bestValue)
            return bestValue
        else:
            cells = [i for i, x in enumerate(grid) if x == 0]
            child = []
            for c in cells:
                temp = list(grid)
                temp[c] = 2
                child.append(temp)
                temp = list(grid)
                temp[c] = 4
                child.append(temp)
            bestValue = np.inf
            for ch in child:
                bestValue = min(bestValue, Alpha_Beta_Prune.calculate(ch, depth - 1, alpha, beta, True))
                if bestValue <= alpha:
                    return bestValue
                beta = min(beta, bestValue)
            return bestValue


class AI2048:
    def __init__(self, size=4):
        self.grid = Grid(size)
        self.possibleTileValue = [2, 4]
        self.prob = prob
        self.initialTiles = initialTiles
        self.opponent = None
        self.agent = None
        self.end = False

    def set_Agent(self, agent):
        self.agent = agent

    def set_Opponent(self, opponent):
        self.opponent = opponent

    def set_Clock(self, time):
        if time - self.prevTime > timeLimit + 0.1:
            self.end = True
        else:
            self.prevTime = time

    def Game_Completed(self):
        return not self.grid.likelihood_of_move()

    def Randon_Tile(self):
        tile = self.Next_Tile()
        cells = self.grid.Empty_tiles()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.map[cell[0]][cell[1]] = tile

    def Next_Tile(self):
        if randint(0, 99) < 100 * self.prob:
            return self.possibleTileValue[0]
        else:
            return self.possibleTileValue[1];

    def start_game(self):
        self.start_move()

    def start_move(self):
        for i in range(self.initialTiles):
            self.Randon_Tile()

        self.Grid_Display(self.grid)

        turn = Agent
        highestTile = 0

        self.prevTime = time.perf_counter()
        itr = 0
        while not self.Game_Completed() and not self.end:
            itr = itr + 1
            temp = self.grid.copy()
            Total_move = None

            if turn == Agent:
                print("Agent is playing")
                Total_move = self.agent.getMove(temp)

                if Total_move != None and Total_move >= 0 and Total_move < 4:
                    if self.grid.likelihood_of_move([Total_move]):
                        self.grid.Total_move(Total_move)
                        highestTile = self.grid.Top_Tile()


                        if highestTile == 2048:
                            self.end = True

                    else:
                        print("Wrong Move")
                        self.end = True
                else:
                    print("Wrong Move - 1")
                    self.end = True
            else:
                print("Opponent is playing")
                Total_move = self.opponent.getMove(temp)
                if Total_move and self.grid.No_of_Insertion(Total_move):
                    self.grid.map[Total_move[0]][Total_move[1]] = self.Next_Tile()
                else:
                    print("Wrong move")
                    self.end = True


            if not self.end:
                # print(itr)
                self.Grid_Display(self.grid)


            self.set_Clock(time.perf_counter())
            turn = 1 - turn
        max_tiles_array.append(highestTile)
        print("Highest Score for this game:", highestTile)
        game_itr.append([itr, highestTile])
        self.Grid_Display(self.grid)

    def Grid_Display(self, grid):
        for i in range(grid.size):
            for j in range(grid.size):
                print("%6d  " % grid.map[i][j], end="")
            print("")
        print("")
        print("")


def driver_code():
    game = AI2048()
    agent = user()
    opponent = Opponent_agent()
    game.set_Agent(agent)
    game.set_Opponent(opponent)
    game.start_game()


if __name__ == '__main__':
    numofGames = 2
    for i in range(numofGames):
        print("--------------------------Iteration :", i + 1, "--------------------------------------")
        driver_code()
    number_of_iteration = []
    highest_tile = []
    number_of_games = []
    for i in range(numofGames):
        print("Game running now:", i + 1)
        number_of_games.append(i + 1)
        print('No.of Itr:', game_itr[i][0])
        number_of_iteration.append(game_itr[i][0])
        print('Highest Value:', game_itr[i][1])
        highest_tile.append(game_itr[i][1])
    #Plot the graph
    plt.plot(number_of_games, highest_tile)
    plt.title("Highest scores per game:")
    plt.xlabel('Number of games')
    plt.ylabel('Highest tile')
    plt.show()

