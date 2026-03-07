class MisCanState:
    TOTAL_MIS = 3
    TOTAL_CAN = 3

    def __init__(self, mis, can, boat):
        self.mis = mis   # number of missionaries on the initial bank
        self.can = can   # number of cannibals on the initial bank
        self.boat = boat   # boat on the initial bank?

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
        return hash((self.mis, self.can, self.boat))
    ''' - '''

    def __str__(self):
        return "(" + str(self.mis) + ", " + str(self.can) + ", " + str(self.boat) + ")"

def is_valid(state):
    if state.mis < 0 or state.can < 0:
        return False
    if state.mis > MisCanState.TOTAL_MIS or state.can > MisCanState.TOTAL_CAN:
        return False
    other_mis = MisCanState.TOTAL_MIS - state.mis
    other_can = MisCanState.TOTAL_CAN - state.can
    if state.mis > 0 and state.can > state.mis:
        return False
    if other_mis > 0 and other_can > other_mis:
        return False
    return True

def move_1m(state):
    if state.boat:
        new = MisCanState(state.mis - 1, state.can, False)
    else:
        new = MisCanState(state.mis + 1, state.can, True)
    if is_valid(new):
        return new, 1
    return None

def move_2m(state):
    if state.boat:
        new = MisCanState(state.mis - 2, state.can, False)
    else:
        new = MisCanState(state.mis + 2, state.can, True)
    if is_valid(new):
        return new, 1
    return None

def move_1c(state):
    if state.boat:
        new = MisCanState(state.mis, state.can - 1, False)
    else:
        new = MisCanState(state.mis, state.can + 1, True)
    if is_valid(new):
        return new, 1
    return None

def move_2c(state):
    if state.boat:
        new = MisCanState(state.mis, state.can - 2, False)
    else:
        new = MisCanState(state.mis, state.can + 2, True)
    if is_valid(new):
        return new, 1
    return None

def move_1m1c(state):
    if state.boat:
        new = MisCanState(state.mis - 1, state.can - 1, False)
    else:
        new = MisCanState(state.mis + 1, state.can + 1, True)
    if is_valid(new):
        return new, 1
    return None

def child_miscan_states(state):
    new_states = []
    operators = [move_1m, move_2m, move_1c, move_2c, move_1m1c]
    for op in operators:
        result = op(state)
        if result:
            new_states.append(result)
    return new_states

def goal_miscan_state(state):
    return state.mis == 0 and state.can == 0 and not state.boat

from buckets import breadth_first_search, depth_first_search, depth_limited_search, print_solution

def main():
    goal = breadth_first_search(MisCanState(3, 3, True), goal_miscan_state, child_miscan_states)
    print("BFS Solution:")
    print_solution(goal)
    dfs_goal = depth_first_search(MisCanState(3, 3, True), goal_miscan_state, child_miscan_states)
    print("DFS Solution:")
    print_solution(dfs_goal)
    dls_goal = depth_limited_search(MisCanState(3, 3, True), goal_miscan_state, child_miscan_states, 1)
    print("DLS Solution:")
    print_solution(dls_goal)

if __name__ == "__main__":
    main()
