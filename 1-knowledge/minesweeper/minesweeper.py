import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # We know that all cells in a sentence are mines if the number of mines is 
        # equal to the number of cells.
        # Therefore, if that's true, return all cells. If it's not, return an empty set
        if self.count == len(self.cells):
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # We know that all cells in a sentence are safe if the number of mines is equal to zero
        # Therefore, if that's true, return all cells. If it's not, return an empty set
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If we know a cell is a mine and it is in the current sentence, we can 
        # remove it from the knowledge and subtract mine count by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If we know a cell is safe and it is in the current sentence, we can 
        # remove it from the knowledge maintaining current mine count
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base, based on the value of `cell` and `count`
        # Start empty array to store neighbor cells and current number of neighbor mines
        undetermined_neighbor_cells = []
        undetermined_neighbor_count = count

        # Loop over all cells within one row and column 
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Check if current neighbor cell candidate is within bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    # If current neighbor cell is known as safe, don't add cell to knowledge base
                    if (i, j) in self.safes:
                        continue
                    # If current neighbor cell is known as mine, don't add and also subtract original neighbor mine count in 1
                    elif (i, j) in self.mines:
                        undetermined_neighbor_count -= 1
                        continue
                    # Else (current neighbor cell state is undetermined), mark to add it to knowledge base
                    else:
                        undetermined_neighbor_cells.append((i, j))

        # Add knowledge of undetermined neighbor cells to knowledge base, with its number of mines
        self.knowledge.append(
            Sentence(cells=undetermined_neighbor_cells, count=undetermined_neighbor_count)
        )

        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # loop through sentences
        for sentence in self.knowledge:

            # if there are known safes in the sentence, mark them as safes
            if len(sentence.known_safes()) > 0:
                known_safes = sentence.known_safes().copy()
                for cell in known_safes:
                    self.mark_safe(cell)

            # if there are known mines in the sentence, mark them as mines
            if len(sentence.known_mines()) > 0:
                known_mines = sentence.known_mines().copy()
                for cell in known_mines:
                    self.mark_mine(cell)

        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        # remove empty sentences from knowledge since they add unneccessary overhead
        # before looping to find new sentences:
        self.knowledge = [value for value in self.knowledge if value != Sentence(cells=set(), count=0)]
    
        # initialize empty array to store possible new sentences
        sentences_to_add = []

        # loop through pairs of sentences
        for sentence in self.knowledge:          
            for sentence_two in self.knowledge:
                # if a new sentence can be inferred, add it to array
                # criteria: one sentence is subset of the other, both are not empty and not equal
                if (sentence.cells.issubset(sentence_two.cells) and sentence.cells != set() and sentence_two.cells != set() and sentence.cells != sentence_two.cells):
                    sentences_to_add.append(
                        Sentence(
                            cells=(sentence_two.cells - sentence.cells), 
                            count=(sentence_two.count - sentence.count)
                        )
                    )

        # add new sentences inferred to knowledge base, only if they are not already there
        for sentence in sentences_to_add:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # check which safe moves haven't been made
        safe_moves_available = (self.safes - self.moves_made)

        # if there's a safe move to be made, choose one. otherwise, return Non
        if len(safe_moves_available) > 0:        
            return safe_moves_available.pop()
        return None
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # store all cells of the board in an array
        all_cells = set()
        for i in range(self.height):
            for j in range(self.width):
                all_cells.add((i, j))

        # infer possible moves removing moves made and known mines from all cells
        possible_moves = all_cells - self.moves_made - self.mines

        # if there's any move to be made, choose one randomly
        if len(possible_moves) > 0:
            return random.sample(possible_moves, 1)[0]
        return None
