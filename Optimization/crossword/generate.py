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
        
        #check if variable is unique
        if len(assignment) != len(set(assignment)):
            return False
        
        #check if all words are the correct length
        for variable in assignment:
            for value in variable:
                if len(value) != variable.length:
                    return False
        
        
        
        #no conflicts between neighboring variables
        for x in assignment:
            for y in assignment:
                if x != y:
                    overlap = self.crossword.overlaps[x, y]
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
        
        #create empty dict for new var, no. of constraints
        constraints = dict()
        
        #loop through var values
        for val in self.domains[var]:
            #init constraints = 0
            constraints = 0
            #loop through neighbours of var
            for neighbor in Crossword.neighbors[var]:
                #check if neighbour is assigned already
                if neighbor not in assignment:
                    #loop through vals within neighbors
                    for val in neighbor:
                        #check if assigning value to neighbour eliminates current var
                        #If var and neighbor do not overlap in the crossword puzzle, or
                        #If val is not present in the domain of values for var
                        if not self.crossword.overlaps(var, neighbor) or val not in self.domains[var]:
                            #update var constrainsts number
                            constraints[var] += 1

        # sort the values in the domain of the variable based on the number of constraints
        sorted_values = dict(sorted(constraints.items(), key=lambda item: item[1]))
        # return the ordered values
        print(f"sorted values: {sorted_values}")
        return sorted_values

        #raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        #create empty dict for unassigned words
        unassigned = dict()
        
        #find all the words not in assignment
        for var in self.domains:
            if var not in assignment:
                unassigned[var] = len(self.domains[var])
        
        #sort in order of values
        sorted_unassigned = dict(sorted(unassigned.items(), key=lambda item: item[1]))
        #return var with lowest val ([0])
        return sorted_unassigned[0]
        
        #raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        
        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment) == True:
            return assignment
        else:
            for variable in assignment:
                if variable.value is None:
                    for value in self.domains[variable]:
                        variable.value = self.solve(value)
            
 
 
            
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
