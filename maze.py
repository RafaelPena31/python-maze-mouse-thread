import heapq
import random

# Create maze generating random graph and applying Kruskal's algorithm:
class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
    
    def generate_maze(self):
        graph = []

        for line in range(self.rows):
            for column in range(self.cols):
                neighbors = []

                if line > 0:
                    neighbors.append((line - 1, column))  # Up neighbor;
                if line < self.rows - 1:
                    neighbors.append((line + 1, column))  # Down neighbor;
                if column > 0:
                    neighbors.append((line, column - 1))  # Left neighbor;
                if column < self.cols - 1:
                    neighbors.append((line, column + 1))  # Right neighbor;
                graph.append(((line, column), neighbors))
        
        # Assign random weights to the edges:
        edges = []
        for node, neighbors in graph:
            for neighbor in neighbors:
                if (neighbor, node) not in edges:
                    weight = random.randint(1, 100)
                    edges.append((node, neighbor, weight))
        
        # Sort the edges by weight in ascending order:
        edges.sort(key=lambda x: x[2])
        
        clusters = {node: node for node, _ in graph}
        
        # Find the root of the cluster:
        def find(cluster, node):
            if cluster[node] != node:
                cluster[node] = find(cluster, cluster[node])
            return cluster[node]
        
        # Merge the clusters:
        def union(cluster, node1, node2):
            root1 = find(cluster, node1)
            root2 = find(cluster, node2)
            cluster[root2] = root1
        
        # Apply Kruskal's algorithm to build the `minimum spanning tree`:
        minimum_spanning_tree = []

        for node1, node2, weight in edges:
            root1 = find(clusters, node1)
            root2 = find(clusters, node2)
            if root1 != root2:
                union(clusters, root1, root2)
                minimum_spanning_tree.append((node1, node2))
        
        # Convert the minimum spanning tree into a maze representation:
        maze = [['#'] * (2 * self.cols + 1) for _ in range(2 * self.rows + 1)]

        for node1, node2 in minimum_spanning_tree:
            row1, col1 = node1
            row2, col2 = node2
            maze[2 * row1 + 1][2 * col1 + 1] = ' '
            maze[2 * row2 + 1][2 * col2 + 1] = ' '
            if row1 == row2:
                maze[2 * row1 + 1][col1 + col2 + 1] = ' '
            else:
                maze[row1 + row2 + 1][2 * col1 + 1] = ' '
        
        # Choose a random starting point (mouse - `R`):
        start_x = random.randint(0, self.rows - 1)
        start_y = random.randint(0, self.cols - 1)
        position_x = 2 * start_x + 1
        position_y = 2 * start_y + 1
        maze[position_x][position_y] = 'R'

        # Set specific ending point (cheese - `Q`):
        maze[1][1] = 'Q'

        # Build response:
        response = dict()
        response['maze'] = maze
        response['point_x'] = position_x
        response['point_y'] = position_y

        return response

# Create utils method for calc the solution
class SolutionUtils:
    # Calculate manhattan distance between two points:
    def manhattan_distance_predictability(self, current, goal):
        x1, y1 = current
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    # Build the path's list:
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []

        while current != start:
            path.append(current)
            current = came_from[current]
            
        path.append(start)
        path.reverse()
        return path

# Implement a* algorithm for finding the path from starting point to ending point in a connected graph with minimum spanning tree:
class MazeSolution:
    def __init__(self, maze_graph, start, goal):
        self.maze_graph = maze_graph
        self.start = start
        self.goal = goal
        self.solution_utils = SolutionUtils()

    # A* algorithm implementation:
    def a_star(self):
        rows = len(self.maze_graph)
        cols = len(self.maze_graph[0])

        def is_valid(row, col):
            return 0 <= row < rows and 0 <= col < cols and self.maze_graph[row][col] != '#'

        def get_neighbors(row, col):
            neighbors = []
            actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Actions for up, down, left, right:

            for point_x, point_y in actions:
                new_row, new_col = row + point_x, col + point_y
                if is_valid(new_row, new_col):
                    neighbors.append((new_row, new_col))

            return neighbors

        open_set = []  # Set of nodes to be explored:
        heapq.heappush(open_set, (0, self.start))  # Add self.start node to priority queue:
        came_from = {}  # Mapping of visited nodes and their predecessors:
        cost_so_far = {self.start: 0}  # Cumulative cost to reach each node:

        while open_set:
            _, current = heapq.heappop(open_set)  # Get the node with the lowest estimated cost:
            if current == self.goal:
                break

            for neighbor in get_neighbors(*current):  # Get current neighbors:
                new_cost = cost_so_far[current] + 1  # Fixed cost of moving between neighbors:

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.solution_utils.manhattan_distance_predictability(neighbor, self.goal)  # Cumulative cost + manhattan estimate:
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

        path = self.solution_utils.reconstruct_path(came_from, self.start, self.goal) # Build the path's list:
        return path


# Running:
rows = 10
cols = 20

maze_generator = MazeGenerator(rows, cols)
maze = maze_generator.generate_maze()

start = (maze['point_x'], maze['point_y'])
goal = (1, 1)

maze_solution = MazeSolution(maze['maze'], start, goal)
path = maze_solution.a_star()

for row in maze:
    print(''.join(row))

for index, pos in enumerate(path):
    if index == 1:
        prev_x, prev_y, prev_char = start[0], start[1], 'S'
    else:
        prev_x, prev_y, prev_char = path[index - 1][0], path[index - 1][1], '*'

    maze['maze'][prev_x][prev_y] = prev_char
    maze['maze'][pos[0]][pos[1]] = 'R'

    print('\n')

    for row in maze['maze']:
        print(''.join(row))

print('\nComplete path:')
print(path)
