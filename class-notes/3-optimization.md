# optimization:
choosing the best option from a set of options

in this algorithms, i don't care about the path to the solution, i care about the solution itself (what is the optimal solution? even though the path to find it is not optimal)

## local search
search algorithm that maintain a single node and searches by moving to a neighboring node

## state-space landscape
    - each bar is a possible state (ex: location of hospitals)
    - the height of each bar is a value that represents the state (ex: distance from each house to the nearest hospital)
    - in this case, we are optimizing for the minimum value (configuration of hospitals that leads to shorter distance)

- global minimum
if we are trying to find the global maximum: the function that does it is the *objective function* (receives a state, returns how good the state is)

- global maximum
if we are trying to find the global minimum: the function that dos it is the *cost function* (receives a state, returns how good the state is)

algorithm: maintains a "current state", represented inside a node, and from that state move to one of its neighbors

## hill climbing algorithm
considers the neighbors to decide which way to go
ex: current state has value of 50, left neighbor has value of 70, right neighbor has value of 30, hill climbing goes left (because it is trying to find a maximum)
whenever both neighbors have a lower value than current state, current state is the solution

same for finding minimum, but the opposite

function hill-climb(problem):
    current = initial state of problem
    repeat:
        neighbor = highest valued neighbor of current
        if neighbor not better than current:
            return current
        current = neighbor

issues:
- we can get stuck at a local maximum/minimum
- flat local maximum: various local maximum states with same value
- shoulder: various states with same value

## hill climbing variants
variant                 definition
normal                  choose the first one that is higher valued
steepest-ascent         choose the highest-valued neighbor
stochastic              choose randomly from higher-valued neighbors
first-choice            choose the first higher-valued neighbor
random-restart          conduct hill-climbing multiple times
local beam search       chooses the k highest-valued neighbors

problem: all those algorithms never make a move that makes the situation worse - that's what we need to do sometimes to find global maximums

## simulated annealing
start making more random moves
in the end make less random movs
- early on, higher "temperature": more likely to accept neighbors that are worse than current state
- later on, lower "temperature": less likely to accept neighbors that are worse than current state

function SIMULATED-ANNEALING(problem, max):
    current = initial state of problem
    for t = 1 to max:
        T = temperature(t)
        neighbor = random neighbor of current
        deltaE = how much better neigbor is than current
        if deltaE > 0:
            current = neighbor
        with probability e^(deltaE/T) set current = neighbor
    return current

(logic: the worse deltaE is (greater abs value), less inclined we will be to move to a worse state; also, with high T we are more inclined to move to a worse state (beginning of problem) than with low T (end of problem))

## traveling salesman problem
- i have some cities
- i want to find some route that goes through all cities and comes back to the initial place
- this route should minimize total distance

## linear programming
- minimize a cost function c1x1 + c2x2 + ... + cnxn (linear equation)
- with constraints of form a1x1 + a2x2 + ... + anxn <= b
or of form a1x1 + a2x2 + ... + anxn = b
- with bounds for each variable li <= xi <= ui

if you formulate a problem in this format: there are some algorithms that can solve it

example of linear programming:
- Two machines X1 and X2. X1 costs $50/hour to run, X2 costs $80/hour to run. Goal is to minimize total cost
- X1 requires 5 units of labor per hour. X2 requires 2 units of labor per hour. Total of 20 units of labor to spend.
- X1 produces 10 units of output per hour. X2 produces 12 units of output per hour. Company needs 90 units of output

- cost function: 50x1 + 80x2 (x1 is how many hours we run x1, x2 is how many hours we run x2)
- constraint: 5x1 + 2x2 < 20
- constraint: 10x1 + 12x2 >= 90
in linear programming we should have only equal or lower/equal equations, so we should multiply the last one by -1
(-10x1) + (-12x2) <= -90

algorithms to solve this type of problem:
- simplex
- interior-point
scipy.optimize.linprog(
    [50, 80],                   # Cost function: 50x_1 + 80x_2
    A_ub=[[5, 2], [-10, -12]],  # Coefficients for inequalities
    B_ub=[20, -90]               # Constraints for inequalities: 20 and -90
    )

## constraint satisfaction problems
ex: student 1, 2, 3, 4 and courses A, B, C, D, E, F, G
1: enrolled in courses A, B, C
2: B, D, E
3: C, E, F
4: E, F, G

three exam slots: Mo, Tu, We
constraint: minimize students taking 2 exams in the same day

- represent courses as nodes
- draw a line if there's a constraint between nodes
- forms constrain graph

definition:
- Set of variables {X1, X2, ..., Xn}
- Set of domains for each variable {D1, D2, ..., Dn}
- Set of constraints C

example of this: sudoku
variables: all of empty cells in puzzle
domain: {1, 2, 3, 4, 5, 6, 7, 8, 9} for each variable
constraints: empty cell 1 != empty cell 2 != empty cell 3 ...

example of student and courses:
variables: {A, B, C, D, E, F, G}
domain: {Monday, Tuesday, Wednesday} for each variable
constraints: A != B, B != C , ...

- hard constraints: constraints that must be satisfied in a correct solution
- soft constraints: constraints that express some notion of which solutions are preferred over others

categories of constraints:
- unary constraint: constraint involving only one variable
ex: {A != Monday}
- binary constraint: constraint involving two variables
ex: {A != B}

### node consistency: when all the values in a variable's domain satisfy the variable's unary constraints

simplified example:
two classes: A, B
domain: {Mon, Tue, Wed}
constraints: {A != Mon, B != Tue, B != Mon, A != B}

making node A node-consistent:
Monday does not satisfy the unary constraints
therefore A: {Tue, Wed} - now it is node consistent
making node B node-consistent
Mon and Tue do not satisfy unary constraints
therefore B: {Wed} - now it is node consistent

updated, enforcing node consistency: A {Tue, Wed}, B {Wed}

### arc consistency: when all the values in a variable's domain satisfy the variable's binary constraints
- To make X arc-consistent with respect to Y, remove elements from X's domain until every choice for X has a possible chance for Y

making node A arc-consistent with B:
if A=Tue, is there a value for B there satisfies binary constraint? Yes, Wed
if A=Wed, is there a value for B there satisfies binary constraint? No
    therefore I remove Wed from A's domain

updated, enforcing arc consistency: A {Tue} B {Wed}

### arc consistency in pseudocode:

function REVISE(csp (constraint satisfaction problem), X, Y):
    revised = false
    for x in X.domain:
        if no y in Y.domain satisfies constraint for (X, Y):
            delete x from X.domain
            revised = true
    return revised

enforce arc consistency for the whole problem
function AC-3(csp):
    queue = all arcs in csp
    while queue non-empty:
        (x, y) = dequeue(queue)
        if revise(csp, X, Y):           # if we reduced X's domain, reconsider
            if size of X.domain == 0:
                return false            # impossible to solve problem
            for each Z in X.neighbors - {Y}:
                enqueue (queue, (Z, X))
    return true

### search problems (recap)
- initial state
- actions
- transition model
- goal test
- path cost function

### csp as search problems
- initial state: empty assignment (no variables)
- actions: add a {variable = value} to assignment
- transition model: shows how adding an assignment changes the assignment
- goal test: check if all variables assigned and constraints all satisfied
- path cost function: all paths have the same cost

## backtracking search
function BACKTRACK(assignment, csp):
    if assingment complete:                 # assignment will start empty
        return assignment
    var = SELECT-UNASSIGNED-VAR(assignment, csp)
    for value in DOMAIN-VALUES(var, assignment, csp): # try all possible valus
        if value consistent with assigment:           # not violate constraint
            add {var = value} to assignment
            result = BACKTRACK(assignment, csp)
            if result != failure:
                return result
        remove {var = value} from assignment    # failure: violate constraints
    return failure

demonstration example in 1:20:00

## inference
in the middle of the process above, we can enforce arc-consistency and get to a solution without need to backtrack (go back and redefine a val because a certain path did not work)

- maintaining arc-consistency: algorithm for enforcing arc-consistency every time we make a new assignment
- how: when we make a new assignment to X, calls AC-3, starting with a queue of all arcs (Y, X) where Y is a neighbor of X

revised form of backtrack:
function BACKTRACK(assignment, csp):
    if assingment complete:                 # assignment will start empty
        return assignment
    var = SELECT-UNASSIGNED-VAR(assignment, csp)
    for value in DOMAIN-VALUES(var, assignment, csp): # try all possible valus
        if value consistent with assigment:           # not violate constraint
            add {var = value} to assignment
            *inferences = INFERENCE(assignment, csp)*
            *if inferences != failure: add inferences to assignment*
            result = BACKTRACK(assignment, csp)
            if result != failure:
                return result
        remove {var = value} *and inferences* from assignment
    return failure

we can make the search process more efficient using heuristics in SELECT-UNASSIGNED-VAR function:
- minimum remaining values (MRV) heuristic: select the variable that has the smallest domain
- degree heuristic: select the variable that has the highest degree (connected to the highest number of other nodes)


DOMAIN-VALUES: this function can also be more efficient
not efficient: go through domain vals in order {Mon, Tue, Wed}
better: choose values which are more likely to be a solution
- least constraining value heuristic: return variables in order by number of choices that ar ruled out for neighboring variables
    - try least-constraining values first (value that rules out the fewest possible options)

## problem formulation
- local search
- linear programming
- constraint satisfaction

todo:
- record video
- quiz
- submit project
