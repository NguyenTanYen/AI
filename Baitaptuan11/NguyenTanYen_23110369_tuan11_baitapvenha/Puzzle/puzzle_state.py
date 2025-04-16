import random

class PuzzleState:
    def __init__(self, board, parent=None, move="", cost=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

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
        goal_positions = {}
        for i in range(3):
            for j in range(3):
                goal_positions[goal_state[i][j]] = (i, j)

        distance = 0
        for i in range(3):
            for j in range(3):
                num = self.board[i][j]
                if num != 0:
                    goal_i, goal_j = goal_positions[num]
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def misplaced_tiles(self, goal_state):
        return sum(
            1 for i in range(3) for j in range(3)
            if self.board[i][j] != 0 and self.board[i][j] != goal_state[i][j]
        )

    def randomize_state(self, steps=10):
        state = self
        for _ in range(steps):
            possible_moves = state.get_possible_moves()
            random_move = random.choice(possible_moves)
            state = state.get_new_state(random_move)
        return state