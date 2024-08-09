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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        for variable in self.domains:
            #update the domain of each variable to remove any values that do not have the correct length
            self.domains[variable] = {
            value for value in self.domains[variable]
            if len(value) == variable.length
        }
        
        
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revision = False
        if self.crossword.overlaps[x, y] is not None:
            self.domains[x] = {
            
            value_x for value_x in self.domains[x]
                if value_x not in self.crossword.overlaps[x, y]
            }
            revision = True
            
        return revision
        
        #raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        print(f"arcs: {arcs}")
        if arcs is None:
            #begin an initial queue of all of the arcs in the problem
            arcs = []
            for x in self.domains:
                for y in self.domains:
                    if x != y:
                        arcs.append((x, y))
        else:
            #begin with initial queue of only the arcs that are in `arcs`
            #each arc is a tuple, (x, y) of a variable x and a different var y
            arcs = arcs.copy()
            
        #loop through the arcs and remove the non consistent ones
        for arc in arcs:
            if self.revise(arc[0], arc[1]) == False:
                arcs.remove(arc)
            
        #
        if arcs is None:
            return False
        else:
            return True
        #raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        #check if all variables have been assigned a value
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False
        
        
        #raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
         # Check if all variables are unique
        if len(assignment) != len(set(assignment)):
            return False
        
        # Check if all words are the correct length
        for variable in assignment:
            value = assignment[variable]
            if len(value) != variable.length:
                return False
        
        # Check for no conflicts between neighboring variables
        for x in assignment:
            for y in assignment:
                if x != y:
                    overlap = self.crossword.overlaps.get((x, y), None)
                    if overlap is not None:
                        i, j = overlap
                        if assignment[x][i] != assignment[y][j]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        print(f"Type of var: {type(var)}")
        print(f"Type of self.domains: {type(self.domains)}")
        print(f"Keys in self.domains: {self.domains.keys()}")

        # Create a dictionary to store the constraint count for each value
        constraint_count = {}

        # Iterate over each value in the domain of the variable
        for value in self.domains[var]:
                count = 0
                # Iterate over each neighbor of the variable
                for neighbor in self.crossword.neighbors(var):
                    # Skip neighbors that are already assigned
                    if neighbor in assignment:
                        continue
                    
                    # Check if there is an overlap between the variable and its neighbor
                    overlap = self.crossword.overlaps.get((var, neighbor), None)
                    if overlap is None:
                        continue

                    # If there is an overlap, determine the position of the overlap
                    i, j = overlap
                    
                    # Check if assigning the current value to var conflicts with the neighbor's value
                    for neighbor_value in self.domains[neighbor]:
                        # If the neighbor's value conflicts with the current value, increment the count
                        if len(neighbor_value) > j and len(value) > i and neighbor_value[j] == value[i]:
                            count += 1
                            break
                
                # Store the constraint count for the current value
                constraint_count[value] = count
            
        # Sort values based on the constraint count (ascending order)
        sorted_values = sorted(self.domains[var], key=lambda val: constraint_count[val])
        
        # Print the sorted values for debugging
        print(f"sorted values: {sorted_values}")
        
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        # Create a dictionary for unassigned variables with their domain sizes
        unassigned = {}
        
        for var in self.domains:
            if var not in assignment:
                # Use the length of the domain for each variable
                unassigned[var] = len(self.domains[var])
        
        # Sort unassigned variables first by domain size (ascending) and then by degree (descending)
        sorted_unassigned = sorted(
            unassigned.items(),
            key=lambda item: (item[1], -len(self.crossword.neighbors(item[0])))
        )
        
        # Return the variable with the smallest domain size and highest degree if tied
        if sorted_unassigned:
            return sorted_unassigned[0][0]
        else:
            return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        
        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
         # If the assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Try each value in the domain of the variable
        for value in self.order_domain_values(var, assignment):
            # Check if assigning the value to the variable is consistent with the assignment
            assignment[var] = value
            if self.consistent(assignment):
                # Recursively call backtrack with the new assignment
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            
            # If no result is found, remove the assignment and try the next value
            assignment.pop(var)
        
        # If no value leads to a solution, return None
        return None
            
 
 
            
#        raise NotImplementedError


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
