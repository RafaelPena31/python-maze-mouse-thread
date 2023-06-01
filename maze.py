import heapq
import random

def generate_maze(rows, cols):
    # Create a grid graph
    graph = []
    for i in range(rows):
        for j in range(cols):
            neighbors = []
            if i > 0:
                neighbors.append((i - 1, j))  # Up neighbor
            if i < rows - 1:
                neighbors.append((i + 1, j))  # Down neighbor
            if j > 0:
                neighbors.append((i, j - 1))  # Left neighbor
            if j < cols - 1:
                neighbors.append((i, j + 1))  # Right neighbor
            graph.append(((i, j), neighbors))
    
    # Assign random weights to the edges
    edges = []
    for node, neighbors in graph:
        for neighbor in neighbors:
            if (neighbor, node) not in edges:
                weight = random.randint(1, 100)  # Assign a random weight to the edge
                edges.append((node, neighbor, weight))
    
    # Sort the edges by weight in ascending order
    edges.sort(key=lambda x: x[2])
    
    # Create a dictionary to track the clusters
    clusters = {node: node for node, _ in graph}
    
    def find(cluster, node):
        # Find the root of the cluster
        if cluster[node] != node:
            cluster[node] = find(cluster, cluster[node])
        return cluster[node]
    
    def union(cluster, node1, node2):
        # Merge the clusters
        root1 = find(cluster, node1)
        root2 = find(cluster, node2)
        cluster[root2] = root1
    
    # Apply Kruskal's algorithm to build the minimum spanning tree
    minimum_spanning_tree = []
    for node1, node2, weight in edges:
        root1 = find(clusters, node1)
        root2 = find(clusters, node2)
        if root1 != root2:
            union(clusters, root1, root2)
            minimum_spanning_tree.append((node1, node2))
    
    # Convert the minimum spanning tree into a maze representation
    maze = [['#'] * (2 * cols + 1) for _ in range(2 * rows + 1)]
    for node1, node2 in minimum_spanning_tree:
        row1, col1 = node1
        row2, col2 = node2
        maze[2 * row1 + 1][2 * col1 + 1] = ' '
        maze[2 * row2 + 1][2 * col2 + 1] = ' '
        if row1 == row2:
            maze[2 * row1 + 1][col1 + col2 + 1] = ' '
        else:
            maze[row1 + row2 + 1][2 * col1 + 1] = ' '
    
    # Choose a random Starting Point
    start_x = random.randint(0, rows - 1)
    start_y = random.randint(0, cols - 1)
    position_x = 2 * start_x + 1
    position_y = 2 * start_y + 1
    maze[position_x][position_y] = 'R'

    maze[1][1] = 'Q'

    response = dict()
    response['maze'] = maze
    response['point_x'] = position_x
    response['point_y'] = position_y

    return response

def a_star(mapa, start, goal, heuristic):
    rows = len(mapa)
    cols = len(mapa[0])

    def is_valid(row, col):
        return 0 <= row < rows and 0 <= col < cols and mapa[row][col] != '#'

    def get_neighbors(row, col):
        neighbors = []
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # movimentos para cima, baixo, esquerda, direita

        for dx, dy in offsets:
            new_row, new_col = row + dx, col + dy
            if is_valid(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    open_set = []  # conjunto de nós a serem explorados
    heapq.heappush(open_set, (0, start))  # adicionar o nó inicial à fila de prioridade
    came_from = {}  # mapeamento de nós visitados e seus predecessores
    cost_so_far = {start: 0}  # custo acumulado para chegar a cada nó

    while open_set:
        _, current = heapq.heappop(open_set)  # obter o nó com menor custo estimado
        if current == goal:
            break  # chegamos ao objetivo, interrompa o loop

        for neighbor in get_neighbors(*current):  # percorrer os vizinhos do nó atual
            new_cost = cost_so_far[current] + 1  # custo fixo de movimento entre vizinhos
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)  # custo acumulado + estimativa heurística
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current

    path = reconstruct_path(came_from, start, goal)
    return path

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def heuristic(current, goal):
    x1, y1 = current
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

# Example usage
rows = 10
cols = 20

maze = generate_maze(rows, cols)

start = (maze['point_x'], maze['point_y'])
goal = (1, 1)

path = a_star(maze['maze'], start, goal, heuristic)
print(path)

for row in maze:
    print(''.join(row))

for index, pos in enumerate(path):
    if index == 1:
        prev_x, prev_y, prev_char = start[0], start[1], 'S'
    else:
        prev_x, prev_y, prev_char = path[index - 1][0], path[index - 1][1], '0'

    maze['maze'][prev_x][prev_y] = prev_char
    maze['maze'][pos[0]][pos[1]] = 'R'

    print('\n')

    for row in maze['maze']:
        print(''.join(row))


