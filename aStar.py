import heapq
import matplotlib.pyplot as plt
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.blocked = False
    def __lt__(self, other):
        return self.f < other.f
def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)
def get_neighbors(node, grid):
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Cross-neighborhood
    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and not grid[nx][ny].blocked:
            neighbors.append(grid[nx][ny])
    return neighbors
def a_star(start, goal, grid, penalized_cells):
    open_set = []
    heapq.heappush(open_set, start)
    start.g = 0
    start.f = heuristic(start, goal)
    while open_set:
        current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]
        for neighbor in get_neighbors(current, grid):
            if (neighbor.x, neighbor.y) in penalized_cells:
                penalized_cost = 5  # Penalize the cost for traversing penalized cells
            else:
                penalized_cost = 1
            tentative_g = current.g + penalized_cost
            if tentative_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = tentative_g
                neighbor.f = neighbor.g + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)
    return None

def plot_path(grid, path):
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=plt.cm.binary)
    x_coords = [y for x, y in path]
    y_coords = [x for x, y in path]
    ax.plot(x_coords, y_coords, color="red", linewidth=2)
    ax.scatter(x_coords, y_coords, color="red")
    plt.show()
    
def read_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            # Satırı ayırıcıya göre böl ve her öğeyi integer'a çevir
            grid.append([int(x) for x in line.split()])
    return grid

def main():
    grid = read_grid_from_file('aStar.txt')
    
    rows = len(grid)
    cols = len(grid[0])

    nodes = [[Node(i, j) for j in range(cols)] for i in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 2 or 0 :
                nodes[i][j].blocked = True
    start_node = nodes[265][291]  # Start node at (0, 1)
    goal_node = nodes[307][390]  # Goal node at (1, 26)
    # Penalized cells between matrices
    penalized_cells = [
        (0, 10), (0, 11), (0, 17), (0, 18), (0, 19), (1, 10), (1, 11), (1, 27), (1, 28), (1, 29),
        (9, 10), (9, 11), (9, 17), (9, 18), (9, 19), (8, 10), (8, 11), (8, 27), (8, 28), (8, 29)
    ]
    path = a_star(start_node, goal_node, nodes, penalized_cells)
    if path:
        print("Shortest Path:", path)
        plot_path(grid, path)
    else:
        print("No path found!")
        
if __name__ == "__main__":
    main()