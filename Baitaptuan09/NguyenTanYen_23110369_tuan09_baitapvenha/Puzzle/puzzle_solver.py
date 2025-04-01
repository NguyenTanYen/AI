import time
from collections import deque
import heapq
from puzzle_state import PuzzleState
import random

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
    
    def simple_hill_climbing(self, initial_state, goal_state):
        start_time = time.time()
        current_state = initial_state
        self.visited_states = {str(initial_state.board)}
        path = [current_state]

        while True:
            if current_state.board == goal_state:
                self.solution_path = path
                self.execution_time = time.time() - start_time
                return True

            neighbors = [current_state.get_new_state(pos) for pos in current_state.get_possible_moves()]
            best_neighbor = None
            best_heuristic = current_state.misplaced_tiles(goal_state)

            for neighbor in neighbors:
                state_str = str(neighbor.board)
                if state_str not in self.visited_states:
                    self.visited_states.add(state_str)
                    h = neighbor.misplaced_tiles(goal_state)
                    if h < best_heuristic:
                        best_neighbor = neighbor
                        best_heuristic = h

            if best_neighbor is None:  
                self.execution_time = time.time() - start_time
                return False

            current_state = best_neighbor
            path.append(current_state)

    def steepest_ascent_hill_climbing(self, initial_state, goal_state):
        start_time = time.time()
        current_state = initial_state
        self.visited_states = {str(initial_state.board)}
        path = [current_state]

        while True:
            if current_state.board == goal_state:
                self.solution_path = path
                self.execution_time = time.time() - start_time
                return True

            neighbors = [current_state.get_new_state(pos) for pos in current_state.get_possible_moves()]
            best_neighbor = min(
                neighbors,
                key=lambda s: s.misplaced_tiles(goal_state),
                default=None
            )

            if best_neighbor is None or best_neighbor.misplaced_tiles(goal_state) >= current_state.misplaced_tiles(goal_state):
                self.execution_time = time.time() - start_time
                return False 

            current_state = best_neighbor
            path.append(current_state)


