# https://submit.cs50.io/check50/8aab40698798393d9ba8a8a62b00d2e21c1a6e0f


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
        self.mines = set()
        
        for cell in self.cells:
            if self.count == len(self.cells):
                self.mines.add(cell) 

        return self.mines
        
        #raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        self.safes = set()
        
        for cell in self.cells:
            if self.count == 0:
                self.safes.add(cell)
        
        return self.safes
        
        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
            
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
                
        if cell in self.cells:

            self.cells.remove(cell)

        #raise NotImplementedError


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
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                sentence.count -= 1

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
    
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                

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
        
        # # Print current cell and count being processed
        # print(f"Processing cell {cell} with count {count}")

        # # Print current state of moves, safes, and mines
        # print(f"Moves made: {self.moves_made}")
        # print(f"Safes: {self.safes}")
        # print(f"Mines: {self.mines}")
        
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base
        new_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                neighbor = (i, j)
                if 0 <= i < self.height and 0 <= j < self.width and neighbor != cell:
                    if neighbor in self.mines:
                        count -= 1  # Deduct from count if neighbor is a known mine
                    elif neighbor not in self.safes:
                        new_cells.add(neighbor)

        if new_cells:
            new_sentence = Sentence(new_cells, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # Mark any additional cells as safe or as mines based on the AI's knowledge base
        made_inference = True
        while made_inference:
            made_inference = False
            for sentence in self.knowledge.copy():
                for cell in sentence.known_safes():
                    if cell not in self.safes:
                        self.mark_safe(cell)
                        made_inference = True
                for cell in sentence.known_mines():
                    if cell not in self.mines:
                        self.mark_mine(cell)
                        made_inference = True

        # Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        new_knowledge = []
        for set1 in self.knowledge:
            for set2 in self.knowledge:
                if set1.cells != set2.cells and set1.cells.issubset(set2.cells):
                    new_cells = set2.cells - set1.cells
                    new_count = set2.count - set1.count
                    inferred_sentence = Sentence(new_cells, new_count)
                    if inferred_sentence not in self.knowledge:
                        new_knowledge.append(inferred_sentence)
                        made_inference = True
        self.knowledge += new_knowledge

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        if len(self.safes) == 0:
            return None
        
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        return None

        
        
        
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        available_moves = set()
        
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    available_moves.add(cell)
        
        if len(available_moves) == 0:
            return None
        
        return random.choice(list(available_moves))
        
        
        
        #raise NotImplementedError