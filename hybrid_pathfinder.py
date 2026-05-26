import numpy as np
import heapq
import matplotlib.pyplot as plt
from ABC import ABC
from Config import Config
import sys


class HybridPathFinder:
    def __init__(self, txt_file_path, start, goal):
        self.grid = np.loadtxt(txt_file_path, dtype=int)
        self.grid_size = self.grid.shape
        self.start = start
        self.goal = goal
        self.penalized_cells = set()

        # ABC algoritması konfigürasyonu
        self.abc_config = Config(sys.argv[1:])

        #self.abc_config.DIMENSION = self.grid_size[0] * self.grid_size[1]
        
        estimated_used_cells = int((self.grid_size[0] * self.grid_size[1]) * 0.2)
        self.abc_config.DIMENSION = estimated_used_cells
        
        self.abc_config.FOOD_NUMBER = 50
        self.abc_config.LIMIT = 100
        self.abc_config.MAXIMUM_EVALUATION = 1000
        self.abc_config.LOWER_BOUND = 0
        self.abc_config.UPPER_BOUND = 1
        self.abc_config.OBJECTIVE_FUNCTION = self.evaluate_path
        self.abc_config.MINIMIZE = True

        self.abc = ABC(self.abc_config)

    def evaluate_path(self, solution):
        self.penalized_cells = set()
        for i, penalty in enumerate(solution):
            if penalty > 0.5:
                row = i // self.grid_size[1]
                col = i % self.grid_size[1]
                self.penalized_cells.add((row, col))

        path = self.a_star(self.start, self.goal)
        if path is None:
            return float('inf')

        cost = len(path)

        # Ceza puanı
        for cell in path:
            if cell in self.penalized_cells:
                cost += 5

        # Dönüş cezası
        turn_penalty = 2
        direction_changes = 0
        for i in range(1, len(path) - 1):
            dx1 = path[i][0] - path[i - 1][0]
            dy1 = path[i][1] - path[i - 1][1]
            dx2 = path[i + 1][0] - path[i][0]
            dy2 = path[i + 1][1] - path[i][1]
            if (dx1, dy1) != (dx2, dy2):
                direction_changes += 2

        cost += direction_changes * turn_penalty

        return cost

    def a_star(self, start, goal):
        open_set = []
        closed_set = set()
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])

        start_node.g = 0
        start_node.f = self.heuristic(start_node, goal_node)
        heapq.heappush(open_set, start_node)

        while open_set:
            current = heapq.heappop(open_set)
            if (current.x, current.y) == (goal_node.x, goal_node.y):
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]

            closed_set.add((current.x, current.y))

            for neighbor in self.get_neighbors(current):
                if (neighbor.x, neighbor.y) in closed_set:
                    continue

                tentative_g = current.g + 1
                if (neighbor.x, neighbor.y) in self.penalized_cells:
                    tentative_g += 5

                if neighbor not in open_set or tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.f = neighbor.g + self.heuristic(neighbor, goal_node)
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)

        return None

    def heuristic(self, node, goal):
        return abs(node.x - goal.x) + abs(node.y - goal.y)

    def get_neighbors(self, node):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            if (
                0 <= new_x < self.grid_size[0]
                and 0 <= new_y < self.grid_size[1]
                and self.grid[new_x, new_y] == 0
            ):
                neighbors.append(Node(new_x, new_y))
        return neighbors

    def find_optimal_path(self):

        # Hedefe ulaşılabilir mi kontrol et
        precheck = self.a_star(self.start, self.goal)
        if precheck is None:
            print("A* ile hedefe ulaşmak imkânsız.")
            return None

        self.abc.initial()
        while not self.abc.stopping_condition():
            self.abc.send_employed_bees()
            self.abc.calculate_probabilities()
            self.abc.send_onlooker_bees()
            self.abc.memorize_best_source()
            self.abc.send_scout_bees()
            self.abc.increase_cycle()

        best_solution = self.abc.globalParams
        self.evaluate_path(best_solution)
        optimal_path = self.a_star(self.start, self.goal)
        return optimal_path


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.f = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


def save_map_with_path(txt_path, path, save_path='map_visual.png'):
    grid = np.loadtxt(txt_path, dtype=int)

    # Görselleştirme formatı: 0 → beyaz, 1 → gri, 2 → siyah
    display_grid = np.ones_like(grid, dtype=float)
    display_grid[grid == 1] = 0.5
    display_grid[grid == 2] = 0.0

    plt.figure(figsize=(10, 10))
    plt.imshow(display_grid, cmap='gray')
    plt.axis('off')

    if path:
        path = np.array(path)
        plt.plot(path[:, 1], path[:, 0], 'b-', linewidth=1.5)  # mavi yol
        plt.plot(path[0, 1], path[0, 0], 'go', markersize=5, label='Start')
        plt.plot(path[-1, 1], path[-1, 0], 'ro', markersize=5, label='Goal')
        plt.legend()

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()


if __name__ == "__main__":
    txt_file_path = 'segmentation_output_half4.txt'
    start = (2, 35)
    goal = (4, 45)

    pathfinder = HybridPathFinder(txt_file_path, start, goal)
    optimal_path = pathfinder.find_optimal_path()

    if optimal_path:
        print("Optimal yol bulundu.")
    else:
        print("Yol bulunamadı!")

    # Sadece harita ve yol çizimi
    save_map_with_path(txt_file_path, optimal_path, save_path='map_visual.png')
