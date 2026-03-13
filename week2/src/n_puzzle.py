from copy import deepcopy
from collections import deque

# definition of the problem
class NPuzzleState:

    def __init__(self, board, move_history=[]):
        # board(list[list[int]]) - the state of the board
        # move_history(list[list[list[int]]]) - the history of the moves up until this state
        self.board = deepcopy(board)
        blank = self.find_blank()
        assert(blank is not None)
        (self.blank_row, self.blank_col) = blank

        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]

    def children(self):
        # returns the possible moves
        functions = [self.up, self.down, self.left, self.right]

        children = []
        for func in functions:
            child = func()
            if child:
                children.append(child)

        return children

    def find_blank(self):
        # finds the blank row and col
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)

    def move(func):
        # decorator function to add to history everytime a move is made
        # functions with @move will apply this decorator
        def wrapper(self):
            state = NPuzzleState(self.board, self.move_history)
            value = func(state)
            if value:
                return state
            else:
                return None

        return wrapper

    @move
    def up(self):
        # moves the blank upwards
        if self.blank_row == 0:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row - 1][self.blank_col]
            self.board[self.blank_row - 1][self.blank_col] = 0
            self.blank_row -= 1
            return True

    @move
    def down(self):
        # moves the blank downwards
        if self.blank_row == len(self.board) - 1:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row + 1][self.blank_col]
            self.board[self.blank_row + 1][self.blank_col] = 0
            self.blank_row += 1
            return True

    @move
    def left(self):
        # moves the blank left
        if self.blank_col == 0:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col - 1]
            self.board[self.blank_row][self.blank_col - 1] = 0
            self.blank_col -= 1
            return True

    @move
    def right(self):
        # moves the blank right
        if self.blank_col == len(self.board[0]) - 1:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col + 1]
            self.board[self.blank_row][self.blank_col + 1] = 0
            self.blank_col += 1
            return True

    def is_complete(self):
        # checks if the board is complete
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != row * len(self.board[0]) + col + 1 and self.board[row][col] != 0:
                    return False
        return True

    def __hash__(self):
        # to be able to use the state in a set
        return hash(str([item for sublist in self.board for item in sublist]))

    def __eq__(self, other):
        # compares the two matrices
        return [item for sublist in self.board for item in sublist] == [item for sublist in other.board for item in sublist]

def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()


def problems():
    return (
        NPuzzleState([[1, 2, 3], [5, 0, 6], [4, 7, 8]]),
        NPuzzleState([[1, 3, 6], [5, 2, 0], [4, 7, 8]]),
        NPuzzleState([[1, 6, 2], [5, 7, 3], [0, 4, 8]]),
        NPuzzleState([[5, 1, 3, 4], [2, 0, 7, 8], [10, 6, 11, 12], [9, 13, 14, 15]]),
    )

def bfs(problem):
    # problem(NPuzzleState) - the initial state
    queue = deque([problem])
    visited = set()

    while queue:
        node = queue.popleft()
        if node.is_complete():
            return node.move_history

        visited.add(node)

        for child in node.children():
            if child not in visited and child not in queue:
                queue.append(child)
    return None

def target_position(number, side):
    # calculates the target position of a piece given its number
    # number (int) - the number of the piece
    # side (int) - the size of the side of the board (only for square boards)
    if number == 0:
        # if it is the last piece, it is 0
        row = col = side - 1
    else:
        # otherwise it is sequential, starting at 1
        row = (number-1) // side
        col = (number-1) % side
    return (row, col)

def h1(state):
    # heuristic function 1
    # returns the number of incorrect placed pieces in the matrix
    board = state.board
    side = len(board) # the size of the side of the board (only for square boards)
    total = 0
    for i in range(side):
        for j in range(side):
            (row,col) = target_position(board[i][j], side)
            if row != i or col != j:
                total += 1
    return total

def h2(state):
    # heuristic function 2
    # returns the sum of manhattan distances from incorrect placed pieces to their correct places
    board = state.board
    side = len(board) # the size of the side of the board (only for square boards)
    total = 0
    for i in range(side):
        for j in range(side):
            (row,col) = target_position(board[i][j], side)
            if row != i or col != j:
                total += abs(row - i) + abs(col - j)
    return total

import heapq # we'll be using a heap to store the states

def greedy_search(problem, heuristic):
    # problem (NPuzzleState) - the initial state
    # heuristic (function) - the heuristic function that takes a board (matrix), and returns an integer
    setattr(NPuzzleState, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [problem]
    visited = set()   # to not visit the same state twice
    
    while states:
        # your code here
        # heapq.heappop(states) can be used to POP a state from the state list
        # heapq.heappush(states, new_state) can be used to APPEND a new state to the state list
        node = heapq.heappop(states)
        if node.is_complete():
            return node.move_history
        visited.add(node)
        for child in node.children():
            if child not in visited and child not in states:
                heapq.heappush(states, child)
                visited.add(child)
    
    return None

def a_star_search(problem, heuristic):
    # problem (NPuzzleState) - the initial state
    # heuristic (function) - the heuristic function that takes a board (matrix), and returns an integer
    setattr(NPuzzleState, "__lt__", lambda self, other: heuristic(self) + len(self.move_history) < heuristic(other) + len(other.move_history))
    states = [problem]
    visited = set()   # to not visit the same state twice
    # Note: in the case of A*, a second finding of the same state might actually be a better path; this implementation does not take that into account
    
    while states:
        # your code here
        # heapq.heappop(states) can be used to POP a state from the state list
        # heapq.heappush(states, new_state) can be used to APPEND a new state to the state list
        node = heapq.heappop(states)
        if node.is_complete():
            return node.move_history
        visited.add(node)
        for child in node.children():
            if child not in visited and child not in states:
                heapq.heappush(states, child)
                visited.add(child)
    return None


def run_named_search(search_name, board):
    state = NPuzzleState(board)
    if search_name == 'bfs':
        return bfs(state)
    if search_name == 'greedy-h1':
        return greedy_search(state, h1)
    if search_name == 'greedy-h2':
        return greedy_search(state, h2)
    if search_name == 'a*-h1':
        return a_star_search(state, h1)
    if search_name == 'a*-h2':
        return a_star_search(state, h2)
    raise ValueError(f"Unknown search name: {search_name}")


def _worker_send(pipe, search_name, board):
    import time, tracemalloc
    try:
        tracemalloc.start()
        t0 = time.perf_counter()
        res = run_named_search(search_name, board)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        pipe.send(('ok', t1 - t0, peak, res))
    except Exception as e:
        try:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        except Exception:
            peak = 0
        pipe.send(('err', type(e).__name__, str(e)))
    finally:
        try:
            pipe.close()
        except Exception:
            pass


def benchmark_search_with_timeout(search_name, problem_board, timeout_seconds):
    import multiprocessing

    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=_worker_send, args=(child_conn, search_name, problem_board))
    p.start()
    p.join(timeout_seconds)
    if p.is_alive():
        p.terminate()
        p.join()
        try:
            parent_conn.close()
        except Exception:
            pass
        return ('timeout', None, None, None)

    if parent_conn.poll():
        tag, a, b, c = parent_conn.recv()
        parent_conn.close()
        if tag == 'ok':
            return ('ok', a, b, c)
        else:
            return ('err', None, None, f"{a}:{b}")
    else:
        parent_conn.close()
        return ('no-data', None, None, None)

if __name__ == "__main__":

    TIMEOUT_SECONDS = 10

    probs = problems()

    searches = [
        ("BFS", 'bfs'),
        ("Greedy-h1", 'greedy-h1'),
        ("Greedy-h2", 'greedy-h2'),
        ("A*-h1", 'a*-h1'),
        ("A*-h2", 'a*-h2'),
    ]

    print("Benchmark results:")
    header = ["Problem"] + [name for name, _ in searches]
    print('\t'.join(header))

    for i, prob in enumerate(probs, start=1):
        row = [f"Prob {i}"]
        for name, search_key in searches:
            status, t, peak, res = benchmark_search_with_timeout(search_key, prob.board, TIMEOUT_SECONDS)
            if status == 'ok':
                steps = len(res) - 1 if res else "-"
                peak_kb = (peak // 1024) if (peak is not None) else 0
                row.append(f"{t:.6f}s/{peak_kb}KB/{steps}")
            elif status == 'timeout':
                row.append("TIMEOUT")
            elif status == 'err':
                row.append(f"ERR:{res}")
            else:
                row.append("NO-DATA")
        print('\t'.join(row))
    