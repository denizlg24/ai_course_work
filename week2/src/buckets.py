class BucketState:
    c1 = 11   # capacity for bucket 1
    c2 = 6   # capacity for bucket 2

    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2

    '''needed for the visited list'''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.b1, self.b2))
    ''' - '''

    def __str__(self):
        return "(" + str(self.b1) + ", " + str(self.b2) + ")"

def empty1(state):
        if state.b1 > 0:
            return BucketState(0, state.b2), state.b1   # using unitary costs
        return None

def empty2(state):
    if state.b2 > 0:
        return BucketState(state.b1, 0), state.b2   # using unitary costs
    return None

def fill1(state):
    if state.b1 < BucketState.c1:
        return BucketState(BucketState.c1, state.b2), BucketState.c1-state.b1
    return None

def fill2(state):
    if state.b2 < BucketState.c2:
        return BucketState(state.b1, BucketState.c2), BucketState.c2-state.b2
    return None

def pour12(state):
    if(state.b1 > 0 and state.b2 < BucketState.c2):
        pour_amount = min(state.b1, BucketState.c2 - state.b2)
        return BucketState(state.b1 - pour_amount, state.b2 + pour_amount), pour_amount
    return None
    
def pour21(state):
    if(state.b2 > 0 and state.b1 < BucketState.c1):
        pour_amount = min(state.b2, BucketState.c1 - state.b1)
        return BucketState(state.b1 + pour_amount, state.b2 - pour_amount), pour_amount
    return None

def child_bucket_states(state):
    new_states = []
    if(empty1(state)):
        new_states.append((empty1(state)))
    if(empty2(state)):
        new_states.append((empty2(state)))
    if(fill1(state)):
        new_states.append((fill1(state)))
    if(fill2(state)):
        new_states.append((fill2(state)))
    if(pour12(state)):
        new_states.append((pour12(state)))
    if(pour21(state)):
        new_states.append((pour21(state)))
    return new_states

def heuristic_bucket(node):
    state = node.state
    if state.b1 == 0 and state.b2 == 0:
        return 1
    return 0 if state.b1 == state.b2 else 1

def goal_bucket_state(goal, state):
    return state.b1 == goal

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = 0
        self.isVisited = False

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    def visited(self):
        return self.isVisited
    def mark_visited(self):
        self.isVisited = True

from collections import deque

def greedy_search(initial_state, goal_state_func, operators_func, heuristic_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = [(root, heuristic_func(root))]   # initialize the queue to store the nodes
    visited = set()
    while queue:
        (node, _) = queue.pop(0) 
        if goal_state_func(node.state): 
            return node
        if node.state in visited:
            continue
        visited.add(node.state)

        for state, cost in operators_func(node.state):
            newNode = TreeNode(state)
            newNode.cost = cost+node.cost
            node.add_child(newNode)
            queue.append((newNode,heuristic_bucket(newNode)));
            
        queue = sorted(queue, key=lambda x: x[1])
            
            
    return None

def a_star_search(initial_state, goal_state_func, operators_func, heuristic_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    root.cost = 0
    queue = [(root, 0+heuristic_func(root))]   # initialize the queue to store the nodes
    visited = set()
    while queue:
        (node, _) = queue.pop(0) 
        if goal_state_func(node.state): 
            return node
        if node.state in visited:
            continue
        visited.add(node.state)

        for state, cost in operators_func(node.state):
            newNode = TreeNode(state)
            newNode.cost = cost+node.cost
            node.add_child(newNode)
            queue.append((newNode,cost+heuristic_bucket(newNode)));
            
        queue = sorted(queue, key=lambda x: x[1])
            
            
    return None

def print_solution(node):
    if node is None:
        print("No solution found.")
        return

    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()

    print("Solution path:")
    for state in path:
        print(state)

def main():
    goal = greedy_search(BucketState(0,0), lambda s: goal_bucket_state(8, s), child_bucket_states,heuristic_bucket)
    print_solution(goal)
    goala = a_star_search(BucketState(0,0), lambda s: goal_bucket_state(8, s), child_bucket_states,heuristic_bucket)
    print_solution(goala)
    return 0

if __name__ == "__main__":    main()