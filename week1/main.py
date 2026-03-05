class BucketState:
    c1 = 4   # capacity for bucket 1
    c2 = 3   # capacity for bucket 2

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
            return BucketState(0, state.b2), 1   # using unitary costs
        return None

def empty2(state):
    if state.b2 > 0:
        return BucketState(state.b1, 0), 1   # using unitary costs
    return None

def fill1(state):
    if state.b1 < BucketState.c1:
        return BucketState(BucketState.c1, state.b2), 1
    return None

def fill2(state):
    if state.b2 < BucketState.c2:
        return BucketState(state.b1, BucketState.c2), 1
    return None

def pour12(state):
    if(state.b1 > 0 and state.b2 < BucketState.c2):
        pour_amount = min(state.b1, BucketState.c2 - state.b2)
        return BucketState(state.b1 - pour_amount, state.b2 + pour_amount), 1
    return None
    
def pour21(state):
    if(state.b2 > 0 and state.b1 < BucketState.c1):
        pour_amount = min(state.b2, BucketState.c1 - state.b1)
        return BucketState(state.b1 + pour_amount, state.b2 - pour_amount), 1
    return None

def child_bucket_states(state):
    new_states = []
    if(empty1(state)):
        new_states.append(empty1(state))
    if(empty2(state)):
        new_states.append(empty2(state))
    if(fill1(state)):
        new_states.append(fill1(state))
    if(fill2(state)):
        new_states.append(fill2(state))
    if(pour12(state)):
        new_states.append(pour12(state))
    if(pour21(state)):
        new_states.append(pour21(state))
    return new_states

def goal_bucket_state(goal, state):
    return state.b1 == goal

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.isVisited = False

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    def visited(self):
        return self.isVisited
    def mark_visited(self):
        self.isVisited = True


from collections import deque
from logging import root

def breadth_first_search(initial_state, goal_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes

    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_func(node.state):   # check goal state
            return node

        for state, _ in operators_func(node.state):   # go through next states
            # create tree node with the new state
            # your code here
            new_node = TreeNode(state)

            # link child node to its parent in the tree
            # your code here
            node.add_child(new_node)

            # enqueue the child node
            # your code here
            queue.append(new_node)

    return None

def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    root.mark_visited();
    visited = [root.state]  
    return dfs_rec(root, goal_state_func, operators_func,visited);

def dfs_rec(root, goal_state_func, operators_func, visited):
    if goal_state_func(root.state):
        return root

    for state, _ in operators_func(root.state):
        new_node = TreeNode(state)
        root.add_child(new_node)

        if not new_node.visited() and new_node.state not in visited:
            new_node.mark_visited()
            visited.append(new_node.state)
            result = dfs_rec(new_node, goal_state_func, operators_func, visited)
            if result is not None:
                return result

    return None

def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    depth_limit = 1;
    goal = None
    while goal is None:
        root = TreeNode(initial_state)
        root.mark_visited();
        goal = depth_first_search_limited(root, goal_state_func, operators_func, depth_limit);
        depth_limit += 1;
    return goal;
        

def depth_first_search_limited(root,goal_state_func, operators_func, limit):
    visited = [root.state]  
    return dfs_rec_limited(root, goal_state_func, operators_func,visited,limit,0);

def dfs_rec_limited(root, goal_state_func, operators_func, visited, limit,depth):
    if goal_state_func(root.state):
        return root
    if depth >= limit:
        return None

    for state, _ in operators_func(root.state):
        new_node = TreeNode(state)
        root.add_child(new_node)
        
        if not new_node.visited() and new_node.state not in visited:
            new_node.mark_visited()
            visited.append(new_node.state)
            result = dfs_rec_limited(new_node, goal_state_func, operators_func, visited, limit, depth + 1)
            if result is not None:
                return result

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
    goal = breadth_first_search(BucketState(0,0), lambda s: goal_bucket_state(2, s), child_bucket_states)
    print("BFS Solution:")
    print_solution(goal)
    dfs_goal = depth_first_search(BucketState(0,0), lambda s: goal_bucket_state(2, s), child_bucket_states)
    print("DFS Solution:")
    print_solution(dfs_goal)
    dls_goal = depth_limited_search(BucketState(0,0), lambda s: goal_bucket_state(2, s), child_bucket_states, 1)
    print("DLS Solution:")
    print_solution(dls_goal)

if __name__ == "__main__":    main()