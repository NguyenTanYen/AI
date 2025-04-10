import os
import pygame
import tkinter as tk
from tkinter import ttk
import time
from puzzle_solver import PuzzleSolver
from puzzle_state import PuzzleState
from tkinter.filedialog import asksaveasfilename

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

        ttk.Label(input_frame, text="Trạng thái ban đầu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
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

        ttk.Label(input_frame, text="Trạng thái đích:").grid(row=0, column=2, padx=15, pady=5, sticky="w")
        goal_frame = ttk.Frame(input_frame)
        goal_frame.grid(row=0, column=3, padx=5, pady=5)
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
  
        algorithms = [
            "BFS", "DFS", "UCS", "IDS", "Greedy", "A*", "IDA*", 
            "Simple Hill Climbing", "Steepest Ascent Hill Climbing", 
            "Stochastic Hill Climbing", "Beam Search", 
            "Simulated Annealing", "Genetic Algorithm"
        ]
        algorithm_menu = ttk.OptionMenu(input_frame, self.algorithm_var, "BFS", *algorithms)
        algorithm_menu.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Beam Width:").grid(row=3, column=0, padx=5, pady=5)
        self.beam_width_var = tk.StringVar(value="2")
        beam_width_entry = ttk.Entry(input_frame, textvariable=self.beam_width_var, width=5)
        beam_width_entry.grid(row=3, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack(pady=5)


        style = ttk.Style()
        
    
        style.configure("Green.TButton", background="#32CD32", foreground="black", font=("Helvetica", 10, "bold"))
        style.configure("Blue.TButton", background="#1E90FF", foreground="black", font=("Helvetica", 10, "bold"))
        style.configure("Red.TButton", background="#FF4500", foreground="black", font=("Helvetica", 10, "bold"))
        style.configure("Orange.TButton", background="#FFA500", foreground="black", font=("Helvetica", 10, "bold"))

        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Giải", style="Green.TButton", command=self.solve).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Bước trước", style="Blue.TButton", command=self.previous_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Bước sau", style="Orange.TButton", command=self.next_step).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Dừng", style="Red.TButton", command=self.stop_auto_play).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tiếp tục", style="Green.TButton", command=self.resume_auto_play).pack(side=tk.LEFT, padx=5)



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


        ttk.Button(self.control_frame, text="Xuất file", command=self.export_solution_to_file).pack(pady=5)

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
        """Cập nhật nhãn hiển thị bước hiện tại."""
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
        """Xử lý giải bài toán và tự động chạy các bước."""
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
        elif algorithm == "Simple Hill Climbing":
            solved = self.solver.simple_hill_climbing(initial_state, goal_board)
        elif algorithm == "Steepest Ascent Hill Climbing":
            solved = self.solver.steepest_ascent_hill_climbing(initial_state, goal_board)
        elif algorithm == "Stochastic Hill Climbing":
            solved = self.solver.stochastic_hill_climbing(initial_state, goal_board)
        elif algorithm == "Beam Search":
            try:
                beam_width = int(self.beam_width_var.get())
            except ValueError:
                beam_width = 2  # Giá trị mặc định
            solved = self.solver.beam_search(initial_state, goal_board, beam_width=beam_width)
        elif algorithm == "Simulated Annealing":
            solved = self.solver.simulated_annealing(initial_state, goal_board)
        elif algorithm == "Genetic Algorithm":
            solved = self.solver.genetic_algorithm(initial_state, goal_board)
        else:
            solved = self.solver.ids(initial_state, goal_board)

        if solved:
            self.solution_path = self.solver.solution_path
            self.current_step = 0
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Đã tìm thấy lời giải!\nSố bước: {len(self.solution_path)-1}\n")
            self.result_text.insert(tk.END, f"Thời gian: {self.solver.execution_time:.3f} giây")
            self.update_step_label()  
            self.draw_board()

            self.auto_play = True
            self.last_auto_play_time = time.time() * 1000
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Không tìm thấy lời giải!")
            self.update_step_label()  

    def previous_step(self):
        if self.solution_path and self.current_step > 0:
            self.current_step -= 1
            self.update_step_label()  
            self.draw_board()

    def next_step(self):
        if self.solution_path and self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.update_step_label()  
            self.draw_board()

    def draw_board(self):
        if not self.solution_path:
            return

        self.screen.fill((173, 216, 230))  
        current_board = self.solution_path[self.current_step].board

        for i in range(3):
            for j in range(3):
                x = j * self.cell_size
                y = i * self.cell_size

            
                pygame.draw.rect(self.screen, (135, 206, 250), (x, y, self.cell_size, self.cell_size))  
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 2)  

                number = current_board[i][j]
                if number != 0:
                    
                    font = pygame.font.Font(None, 74)
                    text = font.render(str(number), True, (0, 0, 0)) 
                    text_rect = text.get_rect()
                    text_x = x + (self.cell_size - text_rect.width) // 2
                    text_y = y + (self.cell_size - text_rect.height) // 2
                    self.screen.blit(text, (text_x, text_y))

        pygame.display.flip()

    def export_solution_to_file(self):
        if not self.solution_path:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Không có lời giải để xuất!")
            return

        
        file_path = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Lưu file dưới dạng"
        )

        if not file_path:  
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Hủy lưu file!")
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("Các bước giải 8-Puzzle:\n")
                for step, state in enumerate(self.solution_path):
                    file.write(f"Bước {step}:\n")
                    for row in state.board:
                        file.write(" ".join(map(str, row)) + "\n")
                    file.write("\n")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Xuất file thành công: {file_path}")
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Lỗi khi xuất file: {e}")

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