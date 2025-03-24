import tkinter as tk
from tkinter import messagebox, ttk
import time
import heapq
from collections import deque

class Puzzle8Solver:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.create_widgets()
        
    def create_widgets(self):
        # Input Panel
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=0, column=0, padx=10, pady=10)
        
        tk.Label(input_frame, text="Trạng thái xuất phát:").grid(row=0, column=0)
        self.initial_state_entries = [[tk.Entry(input_frame, width=3, font=("Arial", 14)) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.initial_state_entries[i][j].grid(row=i+1, column=j)
        self.fill_default_initial_state()
        
        tk.Label(input_frame, text="Trạng thái đích:").grid(row=4, column=0)
        self.goal_state_entries = [[tk.Entry(input_frame, width=3, font=("Arial", 14)) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.goal_state_entries[i][j].grid(row=i+5, column=j)
        self.fill_default_goal_state()
        
        # Search Controls
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        
        tk.Label(control_frame, text="Thuật toán:").grid(row=0, column=0)
        self.algorithm_var = tk.StringVar()
        self.algorithm_dropdown = ttk.Combobox(control_frame, textvariable=self.algorithm_var, state="readonly",
                                               values=["BFS", "DFS", "UCS", "IDFS", "Greedy", "A*"])
        self.algorithm_dropdown.grid(row=0, column=1)
        self.algorithm_dropdown.current(0)
        
        tk.Button(control_frame, text="Tìm kiếm", bg="lightgreen", command=self.start_search).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Search Result
        self.result_label = tk.Label(control_frame, text="Kết quả", font=("Arial", 12, "bold"))
        self.result_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.result_text = tk.Label(control_frame, text="")
        self.result_text.grid(row=3, column=0, columnspan=2)
        
    def fill_default_initial_state(self):
        default_state = [[2, 6, 5], [8, 7, 0], [4, 3, 1]]
        for i in range(3):
            for j in range(3):
                self.initial_state_entries[i][j].insert(0, str(default_state[i][j]))
    
    def fill_default_goal_state(self):
        default_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        for i in range(3):
            for j in range(3):
                self.goal_state_entries[i][j].insert(0, str(default_state[i][j]))
    
    def get_state_from_entries(self, entries):
        return tuple(int(entries[i][j].get()) for i in range(3) for j in range(3))
    
    def start_search(self):
        initial_state = self.get_state_from_entries(self.initial_state_entries)
        goal_state = self.get_state_from_entries(self.goal_state_entries)
        algorithm = self.algorithm_var.get()
        
        start_time = time.time()
        if algorithm == "BFS":
            moves, path = self.bfs(initial_state, goal_state)
        elif algorithm == "DFS":
            moves, path = self.dfs(initial_state, goal_state)
        elif algorithm == "UCS":
            moves, path = self.ucs(initial_state, goal_state)
        elif algorithm == "IDFS":
            moves, path = self.idfs(initial_state, goal_state)
        elif algorithm == "Greedy":
            moves, path = self.greedy(initial_state, goal_state)
        elif algorithm == "A*":
            moves, path = self.a_star(initial_state, goal_state)
        end_time = time.time()
        
        if moves is not None:
            self.result_text.config(text=f"Số bước: {moves}, Thời gian: {end_time - start_time:.4f}s")
        else:
            self.result_text.config(text="Không tìm thấy lời giải!")
            messagebox.showwarning("Lỗi", "Không tìm thấy lời giải")
    
