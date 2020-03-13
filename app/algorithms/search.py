from tools.utils import *


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


def A_star_search(problem):
    # initialize 2 lists
    frontier = PriorityQueue('min', problem.h)
    visited = set()
    # add start node
    initial = Node(problem.initial)
    frontier.append(initial)
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            path = []
            curr = node
            while curr.parent:
                path.append(curr.state)
                curr = curr.parent
            path.reverse()
            return path
        visited.add(node.state)
        for child in node.expand(problem):
            if child.state not in visited and child not in frontier:
                frontier.append(child)
                child.parent = node
            elif child in frontier:
                if problem.h(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    child.parent = node
    return []

