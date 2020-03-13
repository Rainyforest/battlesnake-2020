import math

from tools.utils import is_in, dist


class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError


class BoardProblem(Problem):
    """The problem of searching a graph from one node to another."""

    def __init__(self, initial, goal, board):
        super().__init__(initial, goal)
        self.board = board

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        neighbors = list(self.board.neighbors(A))
        valid_neighbors = [nb for nb in neighbors if not self.board.is_obstacle(nb)]
        return valid_neighbors

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.board.get(A, B) or math.inf)

    def find_min_edge(self):
        return 1

    def h(self, node):
        """h function is straight-line distance from a node's state to goal."""
        if type(node) is str:
            return dist(node, self.goal)

        return dist(node.state, self.goal)