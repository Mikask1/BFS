class Node():
    def __init__(self, coord: tuple, parent, action: int):
        self.coord = coord
        self.parent = parent
        self.action = action

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

    def length(self):
        return len(self.frontier)

class BFS():
    def __init__(self, 
                file_path, 
                wall = "X", 
                path = " ", 
                goal = "+", 
                start  = "+", 
                searched = "*", 
                shortest = "?") -> None:

        self.wall = wall
        self.path = path
        self.start = start
        self.goal = goal
        self.searched = searched
        self.shortest = shortest

        self.frontier = Frontier()
        self.explored = []

        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()

        self.map = [list(line.strip("\n")) for line in lines]
        self.ylen = len(self.map)
        self.xlen = len(self.map[0])

        self.find_start_goal()
        self.start_node = Node(self.start_index, None, None)

        self.explored.append(self.start_index)
        
    def find_start_goal(self) -> None:
        for i in range(self.ylen):
            for j in range(self.xlen):
                if self.map[i][j] == self.start:
                    self.start_index = (i, j)
                if self.map[i][j] == self.goal:
                    self.goal_index = (i, j)
    
        
    def inside(self, i, j) -> bool:
        if ((i >= 0 and i < self.ylen) and (j >= 0 and j < self.xlen)):
            if self.map[i][j] != self.wall:
                if not ((i, j) in self.explored):
                    return True
        return False

    def print_map(self, show_explored = False):
        for i in self.map:
            if show_explored:
                print("".join(i))
            else:
                print("".join(i).replace(self.searched, self.path))

    def search(self, node: Node):
        self.explored.append(node.coord)
        
        if node.coord == self.goal_index:
            parent_node = node.parent
            steps = 1
            while parent_node.parent != None:
                i, j = parent_node.coord
                self.map[i][j] = self.shortest
                steps += 1

                tmp = parent_node
                parent_node = tmp.parent

            self.minimum_steps = steps
            return

        i, j = node.coord
        
        if self.map[i][j] != self.start:
            self.map[i][j] = self.searched

        if self.inside(i-1, j):
            tmp = Node((i-1, j), node, "up")
            self.frontier.add(tmp)
        if self.inside(i, j+1):
            tmp = Node((i, j+1), node, "right")
            self.frontier.add(tmp)
        if self.inside(i+1, j):
            tmp = Node((i+1, j), node, "down")
            self.frontier.add(tmp)
        if self.inside(i, j-1):
            tmp = Node((i, j-1), node, "left")
            self.frontier.add(tmp)

        self.search(self.frontier.remove())

bfs = BFS("example_map.txt", wall = "???", path = " ", goal = "=", start  = "+", searched = "???", shortest = "???")

bfs.search(bfs.start_node)
bfs.print_map(show_explored = True)
print(bfs.minimum_steps)
