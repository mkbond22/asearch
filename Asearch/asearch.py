import heapq

class Maze:
    def __init__(self, filename):
        self.start, self.goals, self.walls, self.width, self.height = self.read_maze(filename)

    # Method to create a array from the maze and find the starting and goal nodes
    def read_maze(self, filename):
        with open(filename, 'r') as f:
            maze = [[char for char in line.strip()] for line in f]
        start = None
        goals = set()
        walls = []
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 'P':
                    start = (i, j)
                elif maze[i][j] == '.':
                    goals.add((i, j))
                elif maze[i][j] == '%':
                    walls.append((i, j))
        width = len(maze[0])
        height = len(maze)
        return start, goals, walls, width, height

    # Method that gets the next nodes from current position
    def get_neighbors(self, pos):
        i, j = pos
        neighbors = [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]
        return [(x, y) for x, y in neighbors if 0 <= x < self.height and 0 <= y < self.width and (x, y) not in self.walls]

    # Defines the manhattan distance
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # Defines A* search with multiple goals
    def astar_multi_goal(self):
        visited = set()
        queue = [(0, self.start, frozenset(self.goals), [])]
        fringe_max = 1
        while queue:
            cost, pos, remaining_goals, path = heapq.heappop(queue)
            if len(remaining_goals) == 0:
                return path + [pos], cost, len(visited), fringe_max
            if pos in visited:
                continue
            visited.add(pos)
            for neighbor in self.get_neighbors(pos):
                new_remaining_goals = remaining_goals - {neighbor}
                new_cost = cost + self.manhattan_distance(pos, neighbor)
                heapq.heappush(queue, (new_cost, neighbor, frozenset(new_remaining_goals), path + [pos]))
            fringe_max = max(fringe_max, len(queue))
        return None

    # Finds the shortest path for the maze object and prints results
    def solve(self):
        multi_goal_sol = self.astar_multi_goal()
        print('A* search shortest path with multiple goals:')
        print('Path:', '.'.join([str(pos) for pos in multi_goal_sol[0]]))
        print('Path cost:', multi_goal_sol[1])
        print('Nodes expanded:', multi_goal_sol[2])
        print('Max tree depth:', len(multi_goal_sol[0]) - 1)
        print('Max fringe size:', multi_goal_sol[3], '\n')

# Print data on searches for each maze size
Maze('smallMaze.txt').solve()
Maze('mediumMaze.txt').solve()
Maze('bigMaze.txt').solve()
Maze('openMaze.txt').solve()

# Method to write the solution path to a new .txt file with '.' for visited nodes
def write_path(filename, output_filename, path):
    with open(filename, 'r') as f:
        maze = [[char for char in line.strip()] for line in f]
    for i, j in path:
        maze[i][j] = '.'
    with open(output_filename, 'w') as f:
        for row in maze:
            f.write(''.join(row) + '\n')


maze = Maze('smallMaze.txt')
solution = maze.astar_multi_goal()
write_path('smallMaze.txt', 'smallMaze_solution.txt', solution[0])

maze = Maze('mediumMaze.txt')
solution = maze.astar_multi_goal()
write_path('mediumMaze.txt', 'mediumMaze_solution.txt', solution[0])

maze = Maze('bigMaze.txt')
solution = maze.astar_multi_goal()
write_path('bigMaze.txt', 'bigMaze_solution.txt', solution[0])

maze = Maze('openMaze.txt')
solution = maze.astar_multi_goal()
write_path('openMaze.txt', 'openMaze_solution.txt', solution[0])