import heapq
from jaraco import functools
from basic_model.direction import Direction


def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)


# direction of neighbourhood coords a -> b
def single_step_dir(a, b):
    (xa, ya) = a
    (xb, yb) = b
    if dist(a, b) == 1:
        if xa == xb:
            return yb - ya + 1
        if ya == yb:
            return xb - xa + 2

    else:
        print("Error in finding direction.")
        return -1


def single_step_direction(a, b):
    (xa, ya) = a
    (xb, yb) = b
    if dist(a, b) == 1:
        if xa == xb:
            if ya - yb == 1:
                return Direction.UP
            else:
                return Direction.DOWN
        if ya == yb:
            if xa - xb == 1:
                return Direction.LEFT
            else:
                return Direction.RIGHT

    else:
        print("Error in finding direction.")
        return Direction.NONE


def advance(coord, dir):
    (x, y) = coord
    if dir == Direction.UP:
        return x, y - 1
    elif dir == Direction.DOWN:
        return x, y + 1
    elif dir == Direction.LEFT:
        return x - 1, y
    elif dir == Direction.RIGHT:
        return x + 1, y
    else:
        return x, y


# get hamilton distance between 2 coords
def dist(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return abs(xa - xb) + abs(ya - yb)


def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn


class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)
