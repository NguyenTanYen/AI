class PuzzleState:
    def __init__(self, board, parent=None, move="", cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def get_blank_pos(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def get_possible_moves(self):
        moves = []
        i, j = self.get_blank_pos()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for di, dj in directions:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                moves.append((new_i, new_j))
        return moves

    def get_new_state(self, new_pos):
        new_board = [row[:] for row in self.board]
        i, j = self.get_blank_pos()
        new_i, new_j = new_pos
        new_board[i][j], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[i][j]
        return PuzzleState(new_board, self, "", self.cost + 1)
    
    def manhattan_distance(self, goal_state):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    num = self.board[i][j]
                    for gi in range(3):
                        for gj in range(3):
                            if goal_state[gi][gj] == num:
                                distance += abs(i - gi) + abs(j - gj)
                                break
        return distance

    def misplaced_tiles(self, goal_state):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0 and self.board[i][j] != goal_state[i][j]:
                    count += 1
        return count