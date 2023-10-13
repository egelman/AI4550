import search as search
from search import EightPuzzle
from search import astar_search
from search import Problem

#calls solutions for water jug problem first
#calls seach heursitic for eight puzzle problem next
#calls for dating problem solution last

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
    initial_state = (3, 5, 1 ,8, 2, 6, 0 ,7, 4 )
    goal_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    
    #MANHATTAN HEURISTIC
    #defines the eight puzzle problem in terms of a manhattan heuristic
    manhattanProblem = ManhattanEight(initial_state, goal_state)
    #checks a* sokution for manhattan distance heuristic
    manhattanSolution = astar_search(manhattanProblem)
    if manhattanSolution:
        print("Manhattan Solution:" + "\n")
        for step in manhattanSolution.path():
            state_str = str(step.state)
            print(state_str)
        with open("solutionEight.txt", "w") as f:
            f.write(f"ManhattanSolution:" + "\n" )
            for step in manhattanSolution.path():
                state_str = str(step.state)
                f.write(state_str +"\n")
    else:
        print("No manhattan solution")


    #MISPLACED TILES HEURISTIC
    #defines the eight puzzle in terms of misplaced tiles heuristic
    misplacedProblem = MisplacedTiles(initial_state, goal_state)
    #checks a* for misplaced tiles heuristic
    misplacedSolution = astar_search(misplacedProblem)
    if misplacedSolution:
        print("Misplaced Tiles Solution:" + "\n")
        for step in misplacedSolution.path():
            state_str = str(step.state)
            print(state_str)
        with open("solutionEight.txt", "a") as f:
            f.write(f"MisplacedTilesSolution:" + "\n")
            for step in misplacedSolution.path():
                state_str = str(step.state)
                f.write(state_str +"\n")
    else:
        print("No misplaced tiles solution")


    #NILSSON SCORE HEURISTIC
    #defines the eight puzzle in temrs of nilsson heuristic
    nilssonProblem = NilssonScore(initial_state, goal_state)
    #checks a* for nilsson score heursitic
    nilssonSolution =  astar_search(nilssonProblem)
    if nilssonSolution:
        print("Nilsson Score Solution:" + "\n")
        for step in nilssonSolution.path():
            state_str = str(step.state)
            print(state_str)
        with open("solutionEight.txt", "a") as f:
            f.write(f"NilssonSolution:"+ "\n" )
            for step in nilssonSolution.path():
                state_str = str(step.state)
                f.write(state_str +"\n")
    else:
        print("No nilsson score solution")


    #NMAXSWAPS HEURISTIC
    #defines the eight puzzle in terms of nMaxSwaps heuristic
    nMaxSwapsProblem = NMaxSwaps(initial_state, goal_state)
    #checks a* for nmaxswaps heuristic
    nMaxSwapsSolution = astar_search(nMaxSwapsProblem)
    if nMaxSwapsSolution:
        print("N-MaxSwaps Solution:" + "\n")
        for step in nMaxSwapsSolution.path():
            state_str = str(step.state)
            print(state_str)
        with open("solutionEight.txt", "a") as f:
            f.write(f"NMaxSwapsSolution:" + "\n")
            for step in nMaxSwapsSolution.path():
                state_str = str(step.state)
                f.write(state_str +"\n")
    else:
        print("No n max swaps solution")


    #DATING PROBLEM SEARCH
    #set initial and goal states for dating problem
    initial_seating = ('M', 'M', 'M', ' ', 'F', 'F', 'F')
    goal_seating = ('M', 'F', 'M', 'F', 'M', 'F', ' ')
    datingProblem = DatingGameProblem(initial_seating, goal_seating)

    #checks DLS for dating problem
    datingDLSSolution = search.depth_limited_search(datingProblem)
    if datingDLSSolution:
        print("Dating DLS Solution:" + "\n")
        for step in datingDLSSolution.path():
            state_str = str(step.state)
            print(state_str)
        with open("solutionDating.txt", "w") as f:
            f.write(f"Dating DLS Solution:" + "\n")
            for step in datingDLSSolution.path():
                state_str = str(step.state)
                f.write(state_str +"\n")
    else:
        print("No dating DLS solution")
    
    #checks a* for dating problem
    datingAStarSolution = astar_search(datingProblem)
    #writes A* solution to file
    if datingAStarSolution:
        print("Dating A* Solution:" + "\n")
        for step in datingAStarSolution.path():
            state_str = str(step.state)
            print(state_str)
        with open("solutionDating.txt", "a") as f:
            f.write(f"Dating A* Solution:" + "\n")
            for step in datingAStarSolution.path():
                state_str = str(step.state)
                f.write(state_str +"\n")
    else:
        print("No dating A* solution")

    


###############WATER JUG PROBLEM#####################
#defines the water jug problem in terms of a search problem's states, initial state, transition model and goal test
class WaterJugProblem(Problem):
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





###############EIGHT PUZZLE PROBLEM##############
#defines all required heuristics as subclasses of the eight puzzle problem
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

        current_state = list(node.state)
        goal_state = list(self.goal)

        while current_state != goal_state:
            blank_index = current_state.index(0)  # finds the index of the blank tile
            goal_tile_at_blank = goal_state[blank_index]  # find what tile should be in the blank's position in the goal state
            
            if goal_tile_at_blank != 0:
                swap_with = current_state.index(goal_tile_at_blank)  # find the index of the tile to be swapped with blank tile
                current_state[blank_index], current_state[swap_with] = current_state[swap_with], current_state[blank_index]  # perform the swap
                nMaxSwaps += 1  
            else:  # if the blank is in the right position, find the first tile that is not in the right position and swap with the blank
                for i, tile in enumerate(current_state):
                    #look for tiles that dont match goal state
                    if tile != goal_state[i]:  
                        #swap to proper position
                        current_state[blank_index], current_state[i] = current_state[i], current_state[blank_index]
                        nMaxSwaps += 1
                        break

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
            if (row, col == 0,0):
                break
        return sequenceScore
    

#Defines the nilsson score
class NilssonScore(EightPuzzle):
    def h(self, node):
        # Combining both heuristics with a weight for the sequence score
        nilssonScore = ManhattanEight.h(self, node) + 3 * SequenceScore.h(self, node)
        return nilssonScore


###################DATING PROBLEM######################
class DatingGameProblem(Problem):
    """ The problem of six people, M and F, and seven seats which need to be arranged in
    the right order. A state is represented as a tuple of length 7, where  element at
    index i represents the tile number at index i (' ' if it's an empty square) """

    def __init__(self, initial, goal=('M', 'F', 'M', 'F', 'M', 'F', ' ')):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_seat(self, state):
        """Return the index of the blank seat in a given state"""
        return state.index(' ')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = []
        blank_index = self.find_blank_seat(state)
        
        # Check left movements
        if blank_index > 0: possible_actions.append(('MOVE', 1))
        if blank_index > 1: possible_actions.append(('JUMP', 2))
        if blank_index > 2: possible_actions.append(('JUMP', 3))
        
        # Check right movements
        if blank_index < 6: possible_actions.append(('MOVE', -1))
        if blank_index < 5: possible_actions.append(('JUMP', -2))
        if blank_index < 4: possible_actions.append(('JUMP', -3))

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        state_list = list(state)
        blank_index = self.find_blank_seat(state_list)
        action_type, action_value = action
        
        if action_type == 'MOVE':
            state_list[blank_index], state_list[blank_index - action_value] = state_list[blank_index - action_value], state_list[blank_index]
        elif action_type == 'JUMP':
            state_list[blank_index], state_list[blank_index - action_value] = state_list[blank_index - action_value], state_list[blank_index]
        
        return tuple(state_list)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        action_type, action_value = action
        # Moving to an adjacent empty chair has a cost of 1
        if action_type == 'MOVE':
            return c + 1
        
        # Jumping over one or two other persons
        elif action_type == 'JUMP':
            # The cost is equal to the number of persons jumped over
            return c + abs(action_value) - 1
    

    def h(self, node):
        """ Return the heuristic value for a given state. heuristic function used is 
        h(n) = number of people in wrong seats """
        return sum([1 for i in range(len(node.state)) if node.state[i] != self.goal[i] and node.state[i] != ' '])


if __name__ == "__main__":
    main()
