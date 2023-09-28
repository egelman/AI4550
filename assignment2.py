import search as search
from search import EightPuzzle

#calls solutions for water jug problem, eight puzzle problem, dating problem
def main():
    problem1 = WaterJugProblem((0, 0), (2, 0))
    node = search.breadth_first_tree_search(problem1)

    # gets sequence of actions to the goal
    actions_to_goal = []
    while node.parent is not None:
        actions_to_goal.insert(0, (node.action, node.state))
        node = node.parent

    # Print the actions and states for running and debug
    for action, state in actions_to_goal:
        print("Breadth First Tree Search Solution:")
        print(f"Action: {action}, Resulting State: {state}")

    # write output of Water Jug Probelm into a separate file
    with open("solutionWater.txt", "w") as f:
        for action, state in actions_to_goal:
            f.write(f"Action: {action}, Resulting State: {state}\n")

    #changes goal state to the one shown in figure 1, sets the search method for eight puzzle problem to a* search
    problem2 = EightPuzzle((3, 5, 1 ,8, 2, 6, 0 ,7, 4 ), (1, 2, 3, 8, 0, 4, 7, 6, 5))
    search = search.astar_search(problem2)
    if search:
        print("A* Search Solution:")
        search.solution()



#WATER JUG PROBLEM
#defines the water jug problem in terms of a search problem's states, initial state, transition model and goal test
class WaterJugProblem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

#defining actions possible for the water jug problem
    def actions(self, state):
        actions = []
        jug1, jug2 = state
        #if jug1 is less than 4, fill it fully
        if jug1 < 4: actions.append('Fill Jug1')
        #if jug2 is less than 3, fill it fully
        if jug2 < 3: actions.append('Fill Jug2')
        #if jug1 is not empty, empty it
        if jug1 > 0: actions.append('Empty Jug1')
        #if jug2 is not empty, empty it
        if jug2 > 0: actions.append('Empty Jug2')
        #if jug1 is not empty and jug2 is not full, pour jug1 to jug2
        if jug1 > 0 and jug2 < 3: actions.append('Pour Jug1 to Jug2')
         #if jug2 is not empty and jug1 is not full, pour jug2 to jug1
        if jug2 > 0 and jug1 < 4: actions.append('Pour Jug2 to Jug1')
        return actions

#implementing result, which returns the result of the action
    def result(self, state, action):
        jug1, jug2 = state
        if action == 'Fill Jug1': return (4, jug2)
        if action == 'Fill Jug2': return (jug1, 3)
        if action == 'Empty Jug1': return (0, jug2)
        if action == 'Empty Jug2': return (jug1, 0)
        if action == 'Pour Jug1 to Jug2':
            return (jug1 - (3 - jug2), 3) if jug1 > 3 - jug2 else (0, jug1 + jug2)
        if action == 'Pour Jug2 to Jug1':
            return (4, jug2 - (4 - jug1)) if jug2 > 4 - jug1 else (jug1 + jug2, 0)

#finds out if the goal is reached
    def goal_test(self, state):
        return state == self.goal

#finds the path cost of each action
    def path_cost(self, c, state1, action, state2):
        return c + 1


#EIGHT PUZZLE PROBLEM 
#misplaced tiles heuristic
class MisplacedTiles(EightPuzzle):
    def h(self, node):
        misplacedTiles = sum(s != g for (s, g) in zip(node.state, self.goal))
        return misplacedTiles

#manhattan distance heuristic
class ManhattanEight(EightPuzzle):
    def h(self, node):
        manhattan_h = 0
        puzzle_length = 3 
        for tile in range(1, 9):  
        # Get current row (x) and column (y) of the tile
            current_index = node.state.index(tile)
            x_curr = current_index // puzzle_length
            y_curr = current_index % puzzle_length
        
            # Get goal row (x) and column (y) of the tile
            goal_index = self.goal.index(tile)
            x_goal = goal_index // puzzle_length
            y_goal = goal_index % puzzle_length
        
            # Calculate Manhattan distance for the tile and add to the total distance
            manhattan_h += abs(x_curr - x_goal) + abs(y_curr - y_goal)
        return manhattan_h

#nmaxswaps heuristic, calculating number of swaps needed for goal state
class NMaxSwaps(EightPuzzle):
    def h(self, node):
        nMaxSwaps = 0
        #Copy current state values to action swaps
        swap_state = list(node.state)
        for i in range(len(node.state)):
            for j in range(i + 1, len(node.state)):
                if node.state[i] > node.state[j]:
                    nMaxSwaps += 1
        while swap_state != self.goal:
                blankspot = swap_state.index(0)
                # if blank is in the correct position, swap with first incorrect tile from left
                if blankspot == self.goal.index(0):
                    for i in range(len(swap_state)):
                        if swap_state[i] != self.goal[i]:
                            swap_state[blankspot], swap_state[i] = swap_state[i], swap_state[blankspot]
                            nMaxSwaps += 1
                            break
                else:
                    # Finding the index of tile that should be in the current blank position and swap it with the blank
                    correct_tile_index = swap_state.index(self.goal[blankspot])
                    swap_state[blankspot], swap_state[correct_tile_index] = swap_state[correct_tile_index], swap_state[blankspot]
                    nMaxSwaps += 1

        return nMaxSwaps

#sequence score heursitic for nilsson score 
class SequenceScore(EightPuzzle):
    def h(self, node):
        sequenceScore = 0
        state = node.state  #temp storage for state
        # Convert state to a 2D grid
        grid = [[state[0], state[1], state[2]],
                [state[3], state[4], state[5]],
                [state[6], state[7], state[8]]]
        
        # Define a sequence of moves to navigate through the grid in a circle around the center tile
        # Each move around the center is represented as a (row_change, col_change) tuple
        moves_sequence = [(0, 1), (1, 0), (0, 1), (1, 0), (0, -1), (-1, 0), (0, -1), (-1, 0)]
        
        # Starts from first value of grid
        row, col = 0, 0
        
        # Loop through the sequence of moves and calculate the score
        for move in moves_sequence:
            row_change, col_change = move
            next_row, next_col = row + row_change, col + col_change
            
            expected_value = (grid[row][col] + 1) % 9  #goes from 8 to 1 when wraps around
            if grid[next_row][next_col] != expected_value:
                sequenceScore += 2
            
            # moves to the next tile in the sequence
            row, col = next_row, next_col
        return sequenceScore
    

#Defines the nilsson score
class NilssonScore(EightPuzzle):
    def h(self, node):
        # Combining both heuristics with a weight for the sequence score
        nilssonScore = ManhattanEight.h(self, node) + 3 * SequenceScore.h(self, node)
        return nilssonScore
