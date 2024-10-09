import math
#function defined to get the children
def selectchildren(grid):
    return get_child(grid)

def get_child(grid):
    movesposs = [0,1,2,3]
    children = []
    current_move = []
    for move in movesposs:
        Copy_grid = list(grid)
        moved = possiblemove(Copy_grid, move)
        if moved == True:
            children.append(Copy_grid)
            current_move.append(move)
    return [children,current_move]

def CombineCells(cells):
    if len(cells) <= 1:
        return cells
    count = 0
    while count < len(cells)-1:
        if cells[count] == cells[count+1]:
            cells[count] *= 2
            del cells[count+1]
        count += 1
#function to define the next possible move
def possiblemove(grid, direction):
    Flag_move = False
    if direction == 0:

        for i in range(4):
            cells = []

            for j in range(i,i+13,4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            CombineCells(cells)
            for j in range(i,i+13,4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    Flag_move = True
                grid[j] = value
        return Flag_move
    elif direction == 1:
        for i in range(4):
            cells = []
            for j in range(i+12,i-1,-4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            CombineCells(cells)
            for j in range(i+12,i-1,-4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    Flag_move = True
                grid[j] = value
        return Flag_move
    elif direction == 2:
        for i in [0,4,8,12]:
            cells = []
            for j in range(i,i+4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            CombineCells(cells)
            for j in range(i,i+4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    Flag_move = True
                grid[j] = value
        return Flag_move
    elif direction == 3:
        for i in [3,7,11,15]:
            cells = []
            for j in range(i,i-4,-1):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            CombineCells(cells)
            for j in range(i,i-4,-1):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    Flag_move = True
                grid[j] = value
        return Flag_move

def checkvalidmove(grid):
    if 0 in grid:
        return True
    for i in range(16):
        if (i+1)%4!=0:
            if grid[i]==grid[i+1]:
                return True
        if i<12:
            if grid[i]==grid[i+4]:
                return True
    return False
#function to define hueristics and next possible direction and move
def heuristics(grid):
    empty_Tiles = len([i for i, x in enumerate(grid) if x == 0])
    highest_Tile = max(grid)
    Tile_order = 0
    weights = [65536,32768,16384,8192,512,1024,2048,4096,256,128,64,32,2,4,8,16]
    # weights = [2048, 1024, 512, 256, 128, 64, 32, 2, 4, 8, 16]
    if highest_Tile == grid[0]:
        Tile_order += (math.log(grid[0])/math.log(2))*weights[0]
    for i in range(16):
    # for i in range(11):
        if grid[i] >= 8:
            Tile_order += weights[i]*(math.log(grid[i])/math.log(2))
        # return Order / (11 - emptyTiles)
    return Tile_order/(16-empty_Tiles)

    main_Grid = [[0] * 4 for i in xrange(4)]
    k = 0
    for i in range(4):
        for j in range(4):
            main_Grid[i][j] = grid[k]
            k += 1
    sm = 0
    grid_range(i)
    mn = 0
    up = 0
    down = 0
    left = 0
    right = 0
    for i in range(4):
        j = 0
        k = j+1
        while k < 4:
            if main_Grid[i][k] == 0:
                k += 1
            else:
                if main_Grid[i][j] == 0:
                    current = 0
                else:
                    current = math.log(main_Grid[i][j])/math.log(2)
                nextval = math.log(main_Grid[i][k])/math.log(2)
                if current > nextval:
                    up += nextval - current
                elif nextval > current:
                    down += current - nextval
            j = k
            k += 1
    for j in range(4):
        i = 0
        k = i+1
        while k < 4:
            if main_Grid[j][k] == 0:
                k += 1
            else:
                if main_Grid[j][i] == 0:
                    current = 0
                else:
                    current = math.log(main_Grid[j][i])/math.log(2)
                nextval = math.log(main_Grid[j][k])/math.log(2)
                if current > nextval:
                    left += nextval - current
                elif nextval > current:
                    right += current - nextval
            i = k
            k += 1
    nm = max(up,down) + max(left,right)
    return 0.1*sm+mn+math.log(highest_Tile)/math.log(2)+ empty_Tiles

def checkvalidmove(grid):
    if 0 in grid:
        return True
    for i in range(16):
        if (i+1)%4!=0:
            if grid[i]==grid[i+1]:
                return True
        if i<12:
            if grid[i]==grid[i+4]:
                return True
    return False

def grid_range(i):
    for i in range(4):
        for j in range(4):
            if main_Grid[i][j] != 0:
                val = math.log(main_Grid[i][j])/math.log(2)
                for k in range(3-j):
                    next_right = main_Grid[i][j+k+1]
                    if next_right != 0:
                        right_val = math.log(next_right)/math.log(2)
                        if right_val != val:
                            sm -= math.fabs(right_val - val)
                            break
                for k in range(3-i):
                    nextdown = main_Grid[i+k+1][j]
                    if nextdown != 0:
                        down_val = math.log(nextdown)/math.log(2)
                        if down_val != val:
                            sm -= math.fabs(down_val - val)
                            break
