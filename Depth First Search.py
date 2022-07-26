import sys

class Node():
    """Node is a node that has properties like state, parent, action"""
    def __init__(self, state, parent, action):
        """Used for uninformed algorithm implementation"""
        self.state = state # stores to keep track of co-ordinates of the current node
        self.parent = parent # stores the parent of the node, used to backtrack the solution path once target is found
        self.action = action # action stores the action taken that lead to the current state

class Frontier():
    """Abstract class Frontier, a data structure to keep track of the nodes visited"""
    def __init__(self):
        """Frontier constructor initailizing to a python list"""
        self.frontier = []

    def push(self, node):
        """appends a nodes"""
        self.frontier.append(node)

    def containsState(self, state):
        """Checks weather a state exists in the frontier"""
        return any(node.state == state for node in self.frontier)

    def isEmpty(self):
        """Checks weather the frontier is empty"""
        return len(self.frontier) == 0
    
    def pop(self):
        """pops and returns a node in first-in-last-out"""
        if self.isEmpty():
            """Checks weather the frontier is empty"""
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class maze():
    """Solves a Maze, if it has got any solution"""

    def __init__(self, filename):
        """maze constructor to initailize the variables for a star algorithm"""
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must contain a single start point")
        if contents.count("B") != 1:
            raise Exception("maze mush contain a single goal")

        # get the dimensions of the maze
        contents = contents.splitlines()
        self.height = (len(contents))
        self.width = max(len(content) for content in contents)
        # perceive the maze
        self.walls = []
        for row in range(self.height):
            tem_row = []
            for col in range(self.width):
                try:
                    if(contents[row][col] == "A"):
                        self.start = (row, col)
                        tem_row.append(False)
                    elif(contents[row][col] == "B"):
                        self.goal = (row, col)
                        tem_row.append(False)
                    elif(contents[row][col] == " "):
                        tem_row.append(False)
                    else:
                        tem_row.append(True)
                except IndexError:
                    tem_row.append(False)
            self.walls.append(tem_row)

        self.solution = None

    def display(self):
        """display the maze and it's solution"""
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        """returns a transition model or a dictionary with all the actions that are possible from the current
        state and the new states the respective action leads to"""
        row, col = state
        actionSpace = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        transition_model = []
        for action, (row, col) in actionSpace:
            if 0<=row< self.height and 0<=col< self.width and not self.walls[row][col]:
                transition_model.append((action, (row, col)))
        return transition_model

    def solve(self):
        """solves the maze and outputs the solution"""

        self.explore = 0
        # uses the queue frontier for BFS and stack for DFS, any fronitier works with GBFS and A*
        frontier = Frontier()
    
        start = Node(state=self.start, parent=None, action=None)
        frontier.push(start)
        self.explored = set()
        while True:

            if frontier.isEmpty():
                raise Exception("The frontier is empty")

            node = frontier.pop()
            self.explore += 1

            if node.state == self.goal:
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)
                return

            self.explored.add(node.state)
            # expanding the current node or state and exploring the space
            for action, state in self.neighbors(node.state):
                if not frontier.containsState(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.push(child)
        
        
if len(sys.argv) != 2:
    sys.exit("Use: python maze.py maze.txt")

m = maze(sys.argv[1])
print("Maze:")
m.display()
print("Solving")
m.solve()
print("No of cells explored to find the optimal solution: ", m.explore)
m.display()