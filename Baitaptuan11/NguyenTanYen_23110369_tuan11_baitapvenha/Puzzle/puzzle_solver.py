import time
from collections import deque
import heapq
from puzzle_state import PuzzleState
import random
import math

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

    def stochastic_hill_climbing(self, initial_state, goal_state):
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
            valid_neighbors = [n for n in neighbors if str(n.board) not in self.visited_states]

            if not valid_neighbors:
                self.execution_time = time.time() - start_time
                return False

            self.visited_states.update(str(n.board) for n in valid_neighbors)
            current_state = random.choice(valid_neighbors)
            path.append(current_state)


    def beam_search(self, initial_state, goal_state, beam_width=2):
        start_time = time.time()
        current_states = [initial_state]
        self.visited_states = {str(initial_state.board)}

        while current_states:
            if any(state.board == goal_state for state in current_states):
                goal_state = next(state for state in current_states if state.board == goal_state)
                self.solution_path = self.get_path(goal_state)
                self.execution_time = time.time() - start_time
                return True

            all_neighbors = []
            for state in current_states:
                neighbors = [state.get_new_state(pos) for pos in state.get_possible_moves()]
                all_neighbors.extend(neighbors)

            all_neighbors = [n for n in all_neighbors if str(n.board) not in self.visited_states]
            self.visited_states.update(str(n.board) for n in all_neighbors)

            current_states = sorted(all_neighbors, key=lambda s: s.manhattan_distance(goal_state))[:beam_width]

        self.execution_time = time.time() - start_time
        return False

    def simulated_annealing(self, initial_state, goal_state, initial_temp=1000, cooling_rate=0.99):
        start_time = time.time()
        current_state = initial_state
        self.visited_states = {str(initial_state.board)}
        path = [current_state]
        temperature = initial_temp

        while temperature > 1:
            if current_state.board == goal_state:
                self.solution_path = path
                self.execution_time = time.time() - start_time
                return True

            neighbors = [current_state.get_new_state(pos) for pos in current_state.get_possible_moves()]
            valid_neighbors = [n for n in neighbors if str(n.board) not in self.visited_states]

            if not valid_neighbors:
                self.execution_time = time.time() - start_time
                return False

            self.visited_states.update(str(n.board) for n in valid_neighbors)
            next_state = random.choice(valid_neighbors)
            delta_e = current_state.misplaced_tiles(goal_state) - next_state.misplaced_tiles(goal_state)

            if delta_e > 0 or math.exp(delta_e / temperature) > random.random():
                current_state = next_state
                path.append(current_state)

            temperature *= cooling_rate

        self.execution_time = time.time() - start_time
        return False

    def genetic_algorithm(self, initial_state, goal_state, population_size=50, generations=100, mutation_rate=0.1):
        start_time = time.time()

        def fitness(state):
            return -state.manhattan_distance(goal_state)

        def mutate(state):
            moves = state.get_possible_moves()
            if moves:
                return state.get_new_state(random.choice(moves))
            return state

        def crossover(parent1, parent2):
            return random.choice([parent1, parent2])

        population = [initial_state]
        for _ in range(population_size - 1):
            random_state = initial_state
            for _ in range(random.randint(1, 10)):
                moves = random_state.get_possible_moves()
                if moves:
                    random_state = random_state.get_new_state(random.choice(moves))
            population.append(random_state)

        for _ in range(generations):
            population = sorted(population, key=fitness, reverse=True)
            if population[0].board == goal_state:
                self.solution_path = self.get_path(population[0])
                self.execution_time = time.time() - start_time
                return True

            next_generation = population[:population_size // 2]
            while len(next_generation) < population_size:
                parent1, parent2 = random.sample(next_generation, 2)
                child = crossover(parent1, parent2)
                if random.random() < mutation_rate:
                    child = mutate(child)
                next_generation.append(child)

            population = next_generation

        self.execution_time = time.time() - start_time
        return False

    def and_or_graph_search(self, initial_state, goal_state):

        start_time = time.time()

        def or_search(state, path):
            if state.board == goal_state:
                return True, [state]
            if str(state.board) in path:
                return False, []
            
            path.add(str(state.board))
            actions = state.get_possible_moves()
            for action in actions:
                new_state = state.get_new_state(action)
                success, plan = and_search(new_state, path)
                if success:
                    return True, [state] + plan
            path.remove(str(state.board))
            return False, []

        def and_search(state, path):
            actions = state.get_possible_moves()
            plans = []
            for action in actions:
                new_state = state.get_new_state(action)
                success, plan = or_search(new_state, path)
                if not success:
                    return False, []
                plans.append(plan)
            return True, plans

        success, plan = or_search(initial_state, set())
        self.execution_time = time.time() - start_time
        if success:
            self.solution_path = plan
            return True
        return False

    def belief_state_search(self, initial_state, goal_state):

        start_time = time.time()

        belief_states = [initial_state]
        visited = set()

        while belief_states:
            current_state = belief_states.pop(0)
            if current_state.board == goal_state:
                self.execution_time = time.time() - start_time
                self.solution_path = self.reconstruct_path(current_state)
                return True

            visited.add(str(current_state.board))

            for move in current_state.get_possible_moves():
                new_state = current_state.get_new_state(move)
                if str(new_state.board) not in visited:
                    belief_states.append(new_state)

        self.execution_time = time.time() - start_time
        return False

    def reconstruct_path(self, state):
        path = []
        while state:
            path.append(state)
            state = state.parent
        return path[::-1]


