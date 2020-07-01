import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Unary constraint: word must be same length of var length
        # Re-defining self.domains with only words in the dict value that obey the constraint above
        self.domains = {
            var: {word for word in words if len(word) == var.length} 
            for var, words in self.domains.items()
        }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initialize variables
        overlap = self.crossword.overlaps[x, y]
        revised = False
        domain_x = self.domains[x].copy()
        domain_y = self.domains[y]

        # Loop through words in x's domain
        for word_x in domain_x:
            # If there's no corresponding value in the domain of y when selecting this word
            # in the domain of x, remove it from the domain of x
            if domain_y - {word_x} == set():
                self.domains[x].remove(word_x)
                revised = True

            # Also, if there's an overlap between variables
            elif overlap is not None:
                # Store overlap indexes and initialize compatibility boolean to False
                i, j = overlap   
                word_x_compatible_with_var_y = False

                # Loop through words in y's domain
                for word_y in self.domains[y]:

                    # If the current pair of words is compatible, set compatibility to true
                    # And exit loop (we found a compatibility, so no need to remove anything)
                    if word_x[i] != word_y[j]:
                        word_x_compatible_with_var_y = True
                        break

                # If no word from y domain satisfies the overlap with this word, remove it
                if word_x_compatible_with_var_y == False:
                    self.domains[x].remove(word_x)
                    revised = True

        # Return if we made changes to the domain of x or not
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Define arcs as an initial list of all possible arcs if not provided
        if arcs == None:
            arcs = []
            for var in self.crossword.variables:
                for other_var in self.crossword.variables:
                    if var != other_var:
                        arcs.append((var, other_var))

        # Loop while queue is not empty
        while len(arcs) != 0:
            # Dequeue one arc
            var_x, var_y = arcs.pop(0)

            # Check if there's any possible review on this arc
            # If true, it means that var_x was updated to enforce arc consistency
            if self.revise(var_x, var_y):
                # After update:
                # If the domain of var_x is now empty, the problem has no solution
                if len(self.domains[var_x]) == 0:
                    return False
                
                # Since var_x was updated, we need to re-add arcs with neighbors to queue
                for var_neighbor in self.crossword.neighbors(var_x) - {var_y}:
                    arcs.append((var_neighbor, var_x))

        # Return true if queue is empty (exited loop)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if there are no conflicts between neighboring variables
        # Loop through all variables in assignment
        for var in assignment:
            # Loop through neighbors of variable
            for neighbor in self.crossword.neighbors(var):
                # Proceed only if neighbor is already assigned
                if neighbor in assignment:
                    # Get overlap indexes between variable and neighbor
                    i, j = self.crossword.overlaps[var, neighbor]

                    # If chars are different in the overlap, we can already return false
                    # since we already know the assignment is not consistent
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False

        # If the assignment got to here, there are no conflicts with neighbor values
        # Two checks left:
        # Check if all values are distinct and if every value is the correct length
        check_distinct_values = (len(list(assignment.values())) == len(set(assignment.values())))
        check_length = all([len(assignment[var]) == var.length for var in assignment])

        # Return true if assignment passed on both tests
        return check_distinct_values and check_length

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Initialize empty dict to store priority for words in domain
        order = {}

        # Loop through words in domain
        for word in self.domains[var]:
            # Initialize number of ruled out neighbors as 0 for this choice
            ruled_out_values = 0

            # Get set of unassigned neighbors
            unassigned_neighbors = self.crossword.neighbors(var) - set(assignment)

            # Loop through unassigned neighbors
            for neighbor in unassigned_neighbors:
                # Get overlap between var and this neighbor
                i, j = self.crossword.overlaps[var, neighbor]

                # Loop through possible choices in neighbor's domain
                for neighbor_domain_word in self.domains[neighbor]:
                    # If var's word choice would rule out this neighbor's choice, 
                    # add 1 to ruled_out_values counter
                    if word[i] != neighbor_domain_word[j]:
                        ruled_out_values += 1

            # Assign number of ruled out neighbors to word
            order[word] = ruled_out_values
        
        # Define a sort function that returns the number of ruled out neighbor values
        def sort_words_function(x): return order[x]

        # Return the var's domain using the number of ruled out neighbor values
        # as a sorting key (default is ascending, which is the one we want:
        # words that rules out less neighbor options will come first)
        return sorted(self.domains[var], key=sort_words_function)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Initially implementing it returning any value - go back later and refine it
        # unassigned_variables = self.crossword.variables - set(assignment)
        # return next(iter(unassigned_variables))

        # Defining unassigned variables to choose from
        unassigned_variables = list(self.crossword.variables - set(assignment))

        # Create dicts to store number of remaining values in domain and degrees by var
        remaining_values = {var: len(self.domains[var]) for var in unassigned_variables}
        degree = {var: len(self.crossword.neighbors(var)) for var in unassigned_variables}

        # Create function that return the order criteria:
        # First order by remaining values ascending,
        # Then order by degree descending (therefore the minus signal)
        def sort_vars_function(x): return [remaining_values[x], -degree[x]]

        # sorted_list = sorted(unassigned_variables, key = lambda x: (x[1], x[2]))
        # Define sorted list using function as sorting key
        sorted_unassigned_variables = sorted(unassigned_variables, key=sort_vars_function)
        
        # Return first element of sorted list
        return sorted_unassigned_variables[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assingmnet is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # Select unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Go through each possible value in its domain 
        for value in self.order_domain_values(var, assignment):
            # Assign value to var
            assignment[var] = value

            # If assignment is consistent, proceed adding value to var in assignment
            if self.consistent(assignment):
                # Try to backtrack this new assignment: if successful, return it
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            
            # Otherwise, if assignment is violating constraints, remove var from assignment
            assignment.pop(var)

        # If all values doesn't work, return failure (None)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
