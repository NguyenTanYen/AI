import os
import pygame
import tkinter as tk
from tkinter import ttk
import time
from collections import deque
import heapq
import copy

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

class PuzzleSolver:
    def __init__(self):
        self.solution_path = []
        self.visited_states = set()
        self.execution_time = 0

    def get_path(self, state):
        path = []
        while state:
            path.append(state)
            state = state.parent
        return path[::-1]

    def bfs(self, initial_state, goal_state):
        start_time = time.time()
        queue = deque([initial_state])
        self.visited_states = {str(initial_state.board)}

        while queue:
            current_state = queue.popleft()
            if current_state.board == goal_state:
                self.solution_path = self.get_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for next_pos in current_state.get_possible_moves():
                new_state = current_state.get_new_state(next_pos)
                state_str = str(new_state.board)
                if state_str not in self.visited_states:
                    self.visited_states.add(state_str)
                    queue.append(new_state)
        
        self.execution_time = time.time() - start_time
        return False

    def dfs(self, initial_state, goal_state, depth_limit=None):
        start_time = time.time()
        stack = [(initial_state, 0)]
        self.visited_states = {str(initial_state.board)}

        while stack:
            current_state, depth = stack.pop()
            if current_state.board == goal_state:
                self.solution_path = self.get_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            if depth_limit is None or depth < depth_limit:
                for next_pos in current_state.get_possible_moves():
                    new_state = current_state.get_new_state(next_pos)
                    state_str = str(new_state.board)
                    if state_str not in self.visited_states:
                        self.visited_states.add(state_str)
                        stack.append((new_state, depth + 1))

        self.execution_time = time.time() - start_time
        return False

    def ucs(self, initial_state, goal_state):
        start_time = time.time()
        pq = [(0, initial_state)]
        self.visited_states = {str(initial_state.board)}

        while pq:
            cost, current_state = heapq.heappop(pq)
            if current_state.board == goal_state:
                self.solution_path = self.get_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for next_pos in current_state.get_possible_moves():
                new_state = current_state.get_new_state(next_pos)
                state_str = str(new_state.board)
                if state_str not in self.visited_states:
                    self.visited_states.add(state_str)
                    heapq.heappush(pq, (new_state.cost, new_state))

        self.execution_time = time.time() - start_time
        return False

    def ids(self, initial_state, goal_state, max_depth=50):
        start_time = time.time()
        for depth in range(max_depth):
            self.visited_states = set()
            if self.dfs(initial_state, goal_state, depth):
                self.execution_time = time.time() - start_time
                return True
        self.execution_time = time.time() - start_time
        return False
    
    def greedy(self, initial_state, goal_state):
        start_time = time.time()
        pq = [(initial_state.manhattan_distance(goal_state), initial_state)]
        self.visited_states = {str(initial_state.board)}

        while pq:
            _, current_state = heapq.heappop(pq)
            if current_state.board == goal_state:
                self.solution_path = self.get_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for next_pos in current_state.get_possible_moves():
                new_state = current_state.get_new_state(next_pos)
                state_str = str(new_state.board)
                if state_str not in self.visited_states:
                    self.visited_states.add(state_str)
                    heapq.heappush(pq, (new_state.manhattan_distance(goal_state), new_state))

        self.execution_time = time.time() - start_time
        return False
    def astar(self, initial_state, goal_state):
        start_time = time.time()
        pq = [(initial_state.cost + initial_state.manhattan_distance(goal_state), initial_state)]
        self.visited_states = {str(initial_state.board)}

        while pq:
            _, current_state = heapq.heappop(pq)
            if current_state.board == goal_state:
                self.solution_path = self.get_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for next_pos in current_state.get_possible_moves():
                new_state = current_state.get_new_state(next_pos)
                state_str = str(new_state.board)
                if state_str not in self.visited_states:
                    self.visited_states.add(state_str)
                    f_score = new_state.cost + new_state.manhattan_distance(goal_state)
                    heapq.heappush(pq, (f_score, new_state))

        self.execution_time = time.time() - start_time
        return False

    def ida_star_search(self, state, goal_state, g_score, bound, visited):
        f_score = g_score + state.manhattan_distance(goal_state)
        if f_score > bound:
            return f_score, None
        if state.board == goal_state:
            return -1, state

        min_bound = float('inf')
        for next_pos in state.get_possible_moves():
            new_state = state.get_new_state(next_pos)
            state_str = str(new_state.board)
            if state_str not in visited:
                visited.add(state_str)
                new_bound, found_state = self.ida_star_search(new_state, goal_state, g_score + 1, bound, visited)
                visited.remove(state_str)
                
                if new_bound == -1:
                    return -1, found_state
                if new_bound < min_bound:
                    min_bound = new_bound

        return min_bound, None

    def ida_star(self, initial_state, goal_state):
        start_time = time.time()
        bound = initial_state.manhattan_distance(goal_state)
        
        while True:
            visited = {str(initial_state.board)}
            new_bound, found_state = self.ida_star_search(initial_state, goal_state, 0, bound, visited)
            
            if new_bound == -1:
                self.solution_path = self.get_path(found_state)
                self.execution_time = time.time() - start_time
                return True
            if new_bound == float('inf'):
                self.execution_time = time.time() - start_time
                return False
            bound = new_bound

class PuzzleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Giải 8-Puzzle")
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        pygame.init()
        self.cell_size = 100
        self.width = self.cell_size * 3
        self.height = self.cell_size * 3
        os.environ['SDL_WINDOWID'] = '0'
        
        self.pygame_frame = ttk.Frame(self.main_frame)
        self.pygame_frame.pack(side=tk.LEFT, padx=5)
        
        self.pygame_embed = tk.Frame(self.pygame_frame, width=self.width, height=self.height)
        self.pygame_embed.pack()
        
        os.environ['SDL_WINDOWID'] = str(self.pygame_embed.winfo_id())
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.init()
        
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, padx=20)
        
        self.solver = PuzzleSolver()
        self.current_step = 0
        self.solution_path = []
        self.auto_play = False
        self.auto_play_speed = 1000
        self.last_auto_play_time = 0
        
        self.setup_gui()
        
        self.screen.fill((255, 255, 255))
        pygame.display.flip()

    def setup_gui(self):
        input_frame = ttk.LabelFrame(self.control_frame, text="Thông tin đầu vào")
        input_frame.pack(padx=5, pady=5, fill="x")

        ttk.Label(input_frame, text="Trạng thái ban đầu:").grid(row=0, column=0, padx=5, pady=5)
        initial_frame = ttk.Frame(input_frame)
        initial_frame.grid(row=0, column=1, padx=5, pady=5)
        self.initial_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(initial_frame, width=3)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.initial_entries.append(row_entries)

        ttk.Label(input_frame, text="Trạng thái đích:").grid(row=1, column=0, padx=5, pady=5)
        goal_frame = ttk.Frame(input_frame)
        goal_frame.grid(row=1, column=1, padx=5, pady=5)
        self.goal_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(goal_frame, width=3)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.goal_entries.append(row_entries)

        default_initial = [[2,6,5], [0,8,7], [4,3,1]]
        default_goal = [[1,2,3], [4,5,6], [7,8,0]]
        
        for i in range(3):
            for j in range(3):
                self.initial_entries[i][j].delete(0, tk.END)
                self.initial_entries[i][j].insert(0, str(default_initial[i][j]))
                self.goal_entries[i][j].delete(0, tk.END)
                self.goal_entries[i][j].insert(0, str(default_goal[i][j]))

        ttk.Label(input_frame, text="Thuật toán:").grid(row=2, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar(value="BFS")
        algorithms = ["BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*"]
        algorithm_menu = ttk.OptionMenu(input_frame, self.algorithm_var, "BFS", *algorithms)
        algorithm_menu.grid(row=2, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Giải", command=self.solve).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Bước trước", command=self.previous_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Bước sau", command=self.next_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Dừng", command=self.stop_auto_play).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tiếp tục", command=self.resume_auto_play).pack(side=tk.LEFT, padx=5)

        speed_frame = ttk.Frame(button_frame)
        speed_frame.pack(side=tk.LEFT, padx=5)
        ttk.Label(speed_frame, text="Tốc độ (ms):").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="1000")
        speed_entry = ttk.Entry(speed_frame, textvariable=self.speed_var, width=5)
        speed_entry.pack(side=tk.LEFT, padx=2)

        self.step_label = ttk.Label(self.control_frame, text="Bước: 0/0")
        self.step_label.pack(pady=5)

        self.result_text = tk.Text(self.control_frame, height=5, width=40)
        self.result_text.pack(padx=5, pady=5)

    def stop_auto_play(self):
        self.auto_play = False

    def resume_auto_play(self):
        try:
            self.auto_play_speed = int(self.speed_var.get())
        except ValueError:
            self.auto_play_speed = 1000
            self.speed_var.set("1000")
        self.auto_play = True
        self.last_auto_play_time = time.time() * 1000

    def toggle_auto_play(self):
        self.auto_play = not self.auto_play
        if self.auto_play:
            try:
                self.auto_play_speed = int(self.speed_var.get())
            except ValueError:
                self.auto_play_speed = 1000
                self.speed_var.set("1000")

    def update_step_label(self):
        if self.solution_path:
            self.step_label.config(text=f"Bước: {self.current_step + 1}/{len(self.solution_path)}")
        else:
            self.step_label.config(text="Bước: 0/0")

    def parse_state(self, entries):
        try:
            board = []
            for row in entries:
                board_row = []
                for entry in row:
                    num = int(entry.get().strip())
                    if not (0 <= num <= 8):
                        raise ValueError("Giá trị phải từ 0 đến 8")
                    board_row.append(num)
                board.append(board_row)
            return board
        except:
            return None

    def solve(self):
        initial_board = self.parse_state(self.initial_entries)
        goal_board = self.parse_state(self.goal_entries)

        if not initial_board or not goal_board:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Định dạng đầu vào không hợp lệ!")
            return

        initial_state = PuzzleState(initial_board)
        algorithm = self.algorithm_var.get()

        if algorithm == "BFS":
            solved = self.solver.bfs(initial_state, goal_board)
        elif algorithm == "DFS":
            solved = self.solver.dfs(initial_state, goal_board)
        elif algorithm == "UCS":
            solved = self.solver.ucs(initial_state, goal_board)
        elif algorithm == "Greedy": 
            solved = self.solver.greedy(initial_state, goal_board)
        elif algorithm == "A*":
            solved = self.solver.astar(initial_state, goal_board)
        elif algorithm == "IDA*":
            solved = self.solver.ida_star(initial_state, goal_board)
        else:  # IDS
            solved = self.solver.ids(initial_state, goal_board)

        if solved:
            self.solution_path = self.solver.solution_path
            self.current_step = 0
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Đã tìm thấy lời giải!\nSố bước: {len(self.solution_path)-1}\n")
            self.result_text.insert(tk.END, f"Thời gian: {self.solver.execution_time:.3f} giây")
            self.draw_board()
            
            try:
                self.auto_play_speed = int(self.speed_var.get())
            except ValueError:
                self.auto_play_speed = 1000
                self.speed_var.set("1000")
            self.auto_play = True
            self.last_auto_play_time = time.time() * 1000
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Không tìm thấy lời giải!")

    def previous_step(self):
        if self.solution_path and self.current_step > 0:
            self.current_step -= 1
            self.draw_board()

    def next_step(self):
        if self.solution_path and self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.draw_board()

    def draw_board(self):
        if not self.solution_path:
            return

        self.screen.fill((255, 255, 255))
        current_board = self.solution_path[self.current_step].board

        for i in range(3):
            for j in range(3):
                x = j * self.cell_size
                y = i * self.cell_size
                
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 1)
            
                number = current_board[i][j]
                if number != 0:
                    font = pygame.font.Font(None, 74)
                    text = font.render(str(number), True, (0, 0, 0))
                    
                    text_rect = text.get_rect()
                    text_x = x + (self.cell_size - text_rect.width) // 2
                    text_y = y + (self.cell_size - text_rect.height) // 2
                    self.screen.blit(text, (text_x, text_y))
        
        pygame.display.flip()
        self.update_step_label()

    def run(self):
        while True:
            current_time = time.time() * 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.root.quit()
                    return

            if self.auto_play and self.solution_path:
                if current_time - self.last_auto_play_time >= self.auto_play_speed:
                    if self.current_step < len(self.solution_path) - 1:
                        self.next_step()
                    else:
                        self.auto_play = False
                    self.last_auto_play_time = current_time

            pygame.display.flip()
            self.root.update()

if __name__ == "__main__":
    gui = PuzzleGUI()
    gui.run()