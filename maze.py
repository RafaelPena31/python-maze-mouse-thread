import heapq
import random
import threading

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
        
        edges = []
        for node, neighbors in graph:
            for neighbor in neighbors:
                if (neighbor, node) not in edges:
                    weight = random.randint(1, 100)
                    edges.append((node, neighbor, weight))
        
        edges.sort(key=lambda x: x[2])
        
        clusters = {node: node for node, _ in graph}
        
        def find(cluster, node):
            if cluster[node] != node:
                cluster[node] = find(cluster, cluster[node])
            return cluster[node]
        
        def union(cluster, node1, node2):
            root1 = find(cluster, node1)
            root2 = find(cluster, node2)
            cluster[root2] = root1
        
        minimum_spanning_tree = []

        for node1, node2, weight in edges:
            root1 = find(clusters, node1)
            root2 = find(clusters, node2)
            if root1 != root2:
                union(clusters, root1, root2)
                minimum_spanning_tree.append((node1, node2))
        
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
        
        start_x = random.randint(0, self.rows - 1)
        start_y = random.randint(0, self.cols - 1)
        position_x = 2 * start_x + 1
        position_y = 2 * start_y + 1

        maze[1][1] = 'Q'

        response = dict()
        response['maze'] = maze
        response['point_x'] = position_x
        response['point_y'] = position_y

        return response


class SolutionUtils:
    def manhattan_distance_predictability(self, current, goal):
        x1, y1 = current
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []

        while current != start:
            path.append(current)
            current = came_from[current]
            
        path.append(start)
        path.reverse()
        return path


class MazeSolution:
    def __init__(self, maze_graph, start, goal):
        self.maze_graph = maze_graph
        self.start = start
        self.goal = goal
        self.solution_utils = SolutionUtils()

    def a_star(self):
        rows = len(self.maze_graph)
        cols = len(self.maze_graph[0])

        def is_valid(row, col):
            return 0 <= row < rows and 0 <= col < cols and self.maze_graph[row][col] != '#'

        def get_neighbors(row, col):
            neighbors = []
            actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for point_x, point_y in actions:
                new_row, new_col = row + point_x, col + point_y
                if is_valid(new_row, new_col):
                    neighbors.append((new_row, new_col))

            return neighbors

        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {}
        cost_so_far = {self.start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == self.goal:
                break

            for neighbor in get_neighbors(*current):
                new_cost = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.solution_utils.manhattan_distance_predictability(neighbor, self.goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

        path = self.solution_utils.reconstruct_path(came_from, self.start, self.goal)
        return path

class MazeSolverThread(threading.Thread):
    def __init__(self, maze, start, goal, point_index):
        threading.Thread.__init__(self)
        self.maze = maze
        self.start_position = start
        self.goal = goal
        self.point_index = point_index

    def run(self):
        maze_solution = MazeSolution(self.maze, self.start_position, self.goal)
        path = maze_solution.a_star()

        for index, pos in enumerate(path):
            if index == 1:
                prev_x, prev_y, prev_char = self.start_position[0], self.start_position[1], str(self.point_index)
            elif index != 0:
                prev_x, prev_y, prev_char = path[index - 1][0], path[index - 1][1], '*'

            if index != 0:
                self.maze[prev_x][prev_y] = prev_char
            self.maze[pos[0]][pos[1]] = str(self.point_index)

            for row in self.maze:
                print(''.join(row))
            print('\n')

        print('Complete path for Starting Point', str(self.point_index) + ':')
        print(path)
        print('\n')

class MazeController:
    def __init__(self, rows, cols, num_starting_points):
        self.rows = rows
        self.cols = cols
        self.num_starting_points = num_starting_points

    def solve_maze(self):
        maze_generator = MazeGenerator(self.rows, self.cols)
        maze = maze_generator.generate_maze()

        starting_points = []
        for i, v in enumerate(range(self.num_starting_points)):
            start_x = random.randint(0, self.rows - 1)
            start_y = random.randint(0, self.cols - 1)
            position_x = 2 * start_x + 1
            position_y = 2 * start_y + 1
            starting_points.append((position_x, position_y))
            maze['maze'][position_x][position_y] = str(i)

        goal = (1, 1)

        threads = []
        for i, start in enumerate(starting_points):
            thread = MazeSolverThread(maze['maze'], start, goal, i)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return maze


# Running:
rows = 10
cols = 20
num_starting_points = 2

maze_controller = MazeController(rows, cols, num_starting_points)
maze = maze_controller.solve_maze()
