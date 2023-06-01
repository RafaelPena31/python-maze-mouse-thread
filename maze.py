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
    
    maze[1][1] = 'Q'

    return maze

# Example usage
rows = 10
cols = 20

maze = generate_maze(rows, cols)

for row in maze:
    print(''.join(row))

print(maze[1][1])
