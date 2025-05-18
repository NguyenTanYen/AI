import numpy as np
from collections import defaultdict
import random
import time
import logging
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# moves
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def getStringRepresentation(x):
    return str(x).zfill(9)

def goalTest(state):
    return state == 123456780

def getPath(parentMap, start_state):
    path = []
    current_state = next((state for state, p in parentMap.items() if goalTest(state)), None)
    if current_state is None:
        return [start_state]
    while current_state is not None and current_state != start_state:
        path.append(current_state)
        current_state = parentMap.get(current_state)
    path.append(start_state)
    return path[::-1]

def getChildren(state):
    if not isinstance(state, str) or len(state) != 9 or '0' not in state:
        return {}
    
    zero_idx = state.index('0')
    row, col = zero_idx // 3, zero_idx % 3
    
    moves = [
        (0, (-1, 0)),  # Lên
        (1, (1, 0)),   # Xuống
        (2, (0, -1)),  # Trái
        (3, (0, 1))    # Phải
    ]
    
    children = {}
    for action, (dr, dc) in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            state_list = list(state)
            state_list[zero_idx], state_list[new_idx] = state_list[new_idx], state_list[zero_idx]
            children[str(action)] = ''.join(state_list)
    
    return children

def checkValid(i, j):
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1

def manhattanDistance(state):
    state_str = getStringRepresentation(state)
    total_distance = 0
    for i in range(9):
        if state_str[i] != "0":
            current_num = int(state_str[i])
            goal_x, goal_y = divmod(current_num - 1, 3)
            curr_x, curr_y = divmod(i, 3)
            total_distance += abs(goal_x - curr_x) + abs(goal_y - curr_y)
    return total_distance

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01, q_table_file="q_table.pkl"):
        self.Q_table = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.q_table_file = q_table_file
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.visited = set()
        self.best_path = None
        self.best_path_length = float('inf')
        self.distance_cache = {}

    def _string_to_2d(self, state_str):
        nums = [int(c) for c in state_str]
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def _validate_state(self, state_str):
        if not isinstance(state_str, str) or len(state_str) != 9 or not set(state_str).issubset(set('012345678')):
            logging.error(f"Trạng thái không hợp lệ: {state_str}")
            return False
        return True

    def is_solvable(self, state_str):
        state = [int(c) for c in state_str if c != '0']
        inversions = sum(1 for i in range(len(state)) for j in range(i+1, len(state)) if state[i] > state[j])
        return inversions % 2 == 0

    def choose_action(self, state, valid_moves):
        if not valid_moves:
            logging.warning(f"Không có hành động hợp lệ cho trạng thái: {state}")
            return None
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        q_vals = [self.Q_table[state][a] for a in valid_moves]
        return valid_moves[q_vals.index(max(q_vals))]

    def save_q_table(self):
        try:
            with open(self.q_table_file, "wb") as f:
                pickle.dump(dict(self.Q_table), f)
            logging.info(f"Đã lưu Q-table vào {self.q_table_file}")
        except Exception as e:
            logging.error(f"Lỗi khi lưu Q-table: {e}")

    def train(self, input_state, goal_state, episodes=5000, max_steps=50):
        logging.debug(f"Bắt đầu huấn luyện với input_state: {input_state}, goal_state: {goal_state}")
        start_time = time.perf_counter()
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.visited = set()
        self.best_path = None
        self.best_path_length = float('inf')
        self.distance_cache = {}

        if isinstance(input_state, (list, tuple)):
            input_state_str = getStringRepresentation(input_state)
        elif isinstance(input_state, str):
            input_state_str = input_state
        else:
            logging.error(f"input_state không hợp lệ: {input_state}")
            self.time_taken = time.perf_counter() - start_time
            return [], 0, self.counter, 0, self.time_taken, 0

        if not self._validate_state(input_state_str):
            self.time_taken = time.perf_counter() - start_time
            return [], 0, self.counter, 0, self.time_taken, 0

        if isinstance(goal_state, (int, str)):
            goal_state_str = str(goal_state)
        elif isinstance(goal_state, (list, tuple)):
            goal_state_str = getStringRepresentation(goal_state)
        else:
            logging.error(f"goal_state không hợp lệ: {goal_state}")
            self.time_taken = time.perf_counter() - start_time
            return [], 0, self.counter, 0, self.time_taken, 0

        if not self._validate_state(goal_state_str):
            self.time_taken = time.perf_counter() - start_time
            return [], 0, self.counter, 0, self.time_taken, 0

        if not self.is_solvable(input_state_str):
            logging.info(f"input_state không thể giải được: {input_state_str}")
            self.time_taken = time.perf_counter() - start_time
            return [], 0, self.counter, 0, self.time_taken, 0

        epsilon_decay = (self.epsilon - self.epsilon_end) / episodes

        for ep in range(episodes):
            state = input_state_str
            self.visited.add(state)
            episode_path = [state]

            for step in range(max_steps):
                self.counter += 1
                valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
                if not valid_moves:
                    break

                action = self.choose_action(state, valid_moves)
                if action is None:
                    break
                next_state = getChildren(state).get(action, state)

                self.visited.add(next_state)
                episode_path.append(next_state)

                if state not in self.distance_cache:
                    self.distance_cache[state] = manhattanDistance(int(state))
                if next_state not in self.distance_cache:
                    self.distance_cache[next_state] = manhattanDistance(int(next_state))

                current_distance = self.distance_cache[state]
                next_distance = self.distance_cache[next_state]

                reward = 100 if next_state == goal_state_str else (current_distance - next_distance) * 10

                next_valid_moves = [str(i) for i in range(4) if str(i) in getChildren(next_state)]
                max_q_next = max([self.Q_table[next_state][a] for a in next_valid_moves], default=0)
                self.Q_table[state][action] += self.alpha * (
                    reward + self.gamma * max_q_next - self.Q_table[state][action]
                )

                if next_state == goal_state_str:
                    if len(episode_path) < self.best_path_length:
                        self.best_path = episode_path
                        self.best_path_length = len(episode_path)
                    self.path = episode_path
                    self.cost = len(episode_path) - 1
                    self.depth = len(episode_path) - 1
                    break

                state = next_state

            if self.best_path and len(self.best_path) <= 31:
                break

        if not self.best_path:
            state = input_state_str
            path = [state]
            for _ in range(max_steps):
                if state == goal_state_str:
                    break
                valid_moves = [str(i) for i in range(4) if str(i) in getChildren(state)]
                if not valid_moves:
                    break
                action = self.choose_action(state, valid_moves)
                if action is None:
                    break
                state = getChildren(state).get(action, state)
                path.append(state)
            self.best_path = path
            self.path = path
            self.cost = len(path) - 1
            self.depth = len(path) - 1

        self.time_taken = time.perf_counter() - start_time
        memory_size = sum(len(actions) for state, actions in self.Q_table.items()) * 4

        self.save_q_table()

        logging.info(f"Hoàn thành huấn luyện: Path length = {self.cost}, Counter = {self.counter}, Time = {self.time_taken:.2f}s")
        return self.best_path, self.cost, self.counter, self.depth, self.time_taken, memory_size

def test_q_learning():
    input_state = "123405678"
    goal_state = 123456780
    print("Kiểm tra getChildren...")
    children = getChildren(input_state)
    print(f"getChildren('{input_state}') = {children}")
    print("\nKhởi tạo thuật toán Q-Learning...")
    q_learning = QLearning(alpha=0.1, gamma=0.95, epsilon_start=1.0, epsilon_end=0.01)
    print(f"Chạy Q-Learning với input_state: {input_state}, goal_state: {goal_state}")
    path, cost, counter, depth, time_taken, memory_size = q_learning.train(
        input_state=input_state,
        goal_state=goal_state,
        episodes=5000,
        max_steps=50
    )
    print("\n=== Kết quả Q-Learning ===")
    print(f"Đường đi: {path}")
    print("Đường đi (định dạng 2D):")
    for i, state in enumerate(path):
        state_2d = q_learning._string_to_2d(state)
        print(f"Bước {i}:")
        for row in state_2d:
            print(row)
        print()
    print(f"Chi phí (số bước): {cost}")
    print(f"Số trạng thái đã thăm: {counter}")
    print(f"Độ sâu: {depth}")
    print(f"Thời gian thực hiện: {time_taken:.2f} giây")
    print(f"Kích thước bộ nhớ: {memory_size} bytes")

if __name__ == "__main__":
    test_q_learning()