

# Search algorithm:
agent: entity that perceives its environment and acts upon that environment (ex: self-driving car)

state: a configuration of the agent and its environment (ex: beginning of maze)

actions: choices that can be made in a state
actions(s) that returns the set of actions that can be executed in state s (ex: go left or right)

transition model:
result(s, a) that returns the state resulting from performing action a in state s (ex: left of the beggining of maze)

state space: the set of all states reachable from the initial state by any sequence of actions

goal test: way to determine whether a given state is a goal state (ex: end of maze)

path cost: numerical cost associated with a given path (ex: cost of a path, that should be minimized)
we may either have differents costs for different actions, or all actions have same cost (therefore the lowest path cost is the path with less actions)

Search Problems:
- initial state 
- actions
- transition model
- goal test
- path cost function

solution: a sequence of actions that leads from the initials tate to a goal state
optimal solution: a solution that has the lowest path cost among all solutions

data structure: NODE
a data structure that keeps track of:
- a state
- a parent (node that generated this node)
- an action (action applied to parent to get node)
- a path cost (from initial state to node)

Approach:
- Start with a frontier that contains the initial state
- Repeat:
    - If the frontier is empty, then no solution
    - Remove a node from the frontier
    - If node contains goal state, return the solution
    - Expand node (look at all neighbors), add resulting nodes to the frontier

Issue: B can return to A
Revised Approach
- Start with a frontier that contains the initial state
- Start with an empty explored set
- Repeat:
    - If the frontier is empty, then no solution
    - Remove a node from the frontier
    - If node contains goal state, return the solution
    - Add the node to the explored set
    - Expand node (look at all neighbors), add resulting nodes to the frontier if they aren't already in the frontier or the explored set


which data structure is the frontier?

stack: last-in first-out data type
using a stack, we call this version `depth-first search`, because the algorithm goes deep in a branch before trying the other ones
depth-first search: search algorithm that always expands the deepest node in the frontier

queue: first-in first-out data type
using a queue, we call this version `breadth-first search`
breadth-first search: search algorithm that always expands the shallowest node in the frontier


uninformed search: search strategy that uses no problem-specific knowledge
informed search: search strategy that uses problem-specific knowledge to find solutions more efficiently

greedy best-first search: search algorithm that expands the node that is closest to the goal, as estimated by a heuristic function h(n)

issue: it may lead to a longer dynamo_capacity_indicators_with_costs

A* search: saerch algorithm that expands node with loest value of g(n) + h(n)
g(n) = cost to reach node
h(n) = estimated cost to goal

A* is the optimal path if:
- h(n) is admissible (never overestimates the true cost)
- h(n) is consistent (for every node n and successor n' with step cost c, h(n) <= h(n') + c)

# Adversarial search (ex: tic tac toe, jogo da velha)

algorithm: Minimax

ex: tic tac toe
O winning: -1
tie: 0
X winning: 1

MAX player (X) aims to maximize score
MIN player (O) aims to minimize score

- S0: initial state (empty TTT board)
- player(s): returns which player to move in state s (which turn it is)
- actions(s): returns legal moves in state s
- result (s, a): returns state after action a taken in state s
- terminal(s): checks if state s is a terminal state (game is over)
- utility(s): final numerical value for terminal state s

Minimax in pseudocode:
- Given a state s:
    - MAX picks action a in Actions(s) that produces highest value of MIN-VALUE(RESULT(s, a))
    - MIN picks action a in Actions(s) that produces smallest value of MAX-VALUE(RESULT(s, a))

function MAX-VALUE(state):
    "Returns value of state as output"
    if terminal(state):
        return utility(state)
    v = -infinite
    for action in Actions(state):
        v = max(v, MIN-VALUE(RESULT(state,action)))
    return v

function MIN-VALUE(state):
    "Returns value of state as output"
    if terminal(state):
        return utility(state)
    v = +infinite
    for action in Actions(state):
        v = min(v, MAX-VALUE(RESULT(state,action)))
    return v

optimizations:
alpha-beta pruning: avoid calculations if it's impossible to choose a different path already

minimax is not good for chess: it has 10^29000 possible states, so its impoossible to calculate
however, it works for tictactoe (255k possible states)

better approach: depth-limited minimax
it uses evaluation function: function that estimates the expected utility of the game from a given state, so it doesn't need to calculate as deep as the terminal state (it can stop earlier)


My quiz answers:
1) BFS will sometimes, but not always, find a shorter path than DFS
2) Could only be DFS
3) Depth-limited minimax can arrive at a decision more quickly because it explores fewer states
4) 4
