from copy import deepcopy
#initializing all the directions
All_Directions = (UP_DIR, DOWN_DIR, LEFT_DIR, RIGHT_DIR) = ((-1, 0), (1, 0), (0, -1), (0, 1))
Directions_Index_Range = [UP, DOWN, LEFT, RIGHT] = range(4)
#Creating a class for Grid
class Grid:
    def __init__(self, size = 4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]
#Making a copy of Grid
    def copy(self):
        counter = self.counter_fun()
        return counter

    def counter_fun(self):
        counter = Grid()
        counter.map = deepcopy(self.map)
        counter.size = self.size
        return counter
#Obtaining empty tails
    def Empty_tiles(self):
        Total_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    Total_cells.append((i,j))
        return Total_cells
#getting the top tail
    def Top_Tile(self):
        Top_Cell = 0
        for i in range(self.size):
            for j in range(self.size):
                Top_Cell = max(Top_Cell, self.map[i][j])
        return Top_Cell
#Checking number of insertions
    def No_of_Insertion(self, position):
        return self.return_Cell_Value(position) == 0
#Defining total number of moves in all directions
    def Total_move(self, direction):
        direction = int(direction)
        if direction == UP:
            return self.move_UpDown(False)
        if direction == DOWN:
            return self.move_UpDown(True)
        if direction == LEFT:
            return self.move_LeftRight(False)
        if direction == RIGHT:
            return self.move_LeftRight(True)
# function for moving in the up or down direction
    def move_UpDown(self, down):
        Moved = self.Up_OR_Down(down)
        return Moved

#fuction for moving left or right directions
    def move_LeftRight(self, right):
        move = range(self.size - 1, -1, -1) if right else range(self.size)
        initial_move = move
        Moved = self.Left_OR_Right(initial_move)
        return Moved

    def Left_OR_Right(self, initial_move):
        Moved = False
        for i in range(self.size):
            Total_cells = []
            for j in initial_move:
                cell = self.map[i][j]
                if cell != 0:
                    Total_cells.append(cell)
            self.Merging_cells(Total_cells)
            for j in initial_move:
                value = Total_cells.pop(0) if Total_cells else 0
                if self.map[i][j] != value:
                    Moved = True
                self.map[i][j] = value
        return Moved


    def Up_OR_Down(self, down):
        initial_move = range(self.size -1, -1, -1) if down else range(self.size)
        Moved = False
        for j in range(self.size):
            Total_cells = []
            for i in initial_move:
                cell = self.map[i][j]
                if cell != 0:
                    Total_cells.append(cell)
            self.Merging_cells(Total_cells)
            for i in initial_move:
                value = Total_cells.pop(0) if Total_cells else 0
                if self.map[i][j] != value:
                    Moved = True
                self.map[i][j] = value
        return Moved

# checking for possibility of total number of moves

    def likelihood_of_move(self, directions = Directions_Index_Range):
        check_likelihoodMoves = set(directions)
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j]:
                    for x in check_likelihoodMoves:
                        possible_Move = All_Directions[x]
                        adjacent_Value = self.return_Cell_Value((i + possible_Move[0], j + possible_Move[1]))
                        if adjacent_Value == self.map[i][j] or adjacent_Value == 0:
                            return True
                elif self.map[i][j] == 0:
                    return True
        return False

    def get_position(self, position):
        return position[0] < 0 or position[0] >= self.size or position[1] < 0 or position[1] >= self.size


    def get_likelihood_Moves(self, directions=Directions_Index_Range):
            possible_Moves = []
            for value in directions:
                counter = self.copy()
                if counter.Total_move(value):
                    possible_Moves.append(value)
            return possible_Moves

    def return_Cell_Value(self, pos):
        if not self.get_position(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None

    def Merging_cells(self, cells):
        if len(cells) <= 1:
            return cells
        count = 0
        while count < len(cells) - 1:
            if cells[count] == cells[count+1]:
                cells[count] *= 2
                del cells[count+1]
            count += 1