import random

def create_maze(rows, cols):
    maze = [['#'] * (cols * 2 + 1) for _ in range(rows * 2 + 1)]
    visited = [[False] * cols for _ in range(rows)]

    def generate(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny]:
                visited[nx][ny] = True
                maze[x * 2 + 1 + dx][y * 2 + 1 + dy] = ' '

                maze[x * 2 + 1 + dx // 2][y * 2 + 1 + dy // 2] = ' '

                generate(nx, ny)

    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    generate(start_x, start_y)

    maze[start_x * 2 + 1][start_y * 2 + 1] = 'R'  # Starting point
    maze[1][1] = 'Q'  # Ending point

    return maze

def print_maze(maze):
    for row in maze:
        print(' '.join(row))

# Example usage:
maze = create_maze(10, 10)
print_maze(maze)
