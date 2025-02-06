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
        for var in self.domains:
            self.domains[var] = {word for word in self.domains[var] if len(word) == var.length}

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # terminate if x and y do not overlap
        if not self.crossword.overlaps[x, y]:
            return

        revised = False
        i, j = self.crossword.overlaps[x, y]
        # set of all overlapping letters of values in y's domain
        letters = {word_y[j] for word_y in self.domains[y]}

        for word_x in self.domains[x].copy():
            # remove value from x's domain,
            # if it does not overlap with any values in y's domain
            if word_x[i] not in letters:
                self.domains[x].remove(word_x)
                revised = True

        return revised

    def get_arcs(self):
        arcs = []

        # get all arcs
        for x in self.crossword.variables:
            for y in self.crossword.neighbors(x):
                arcs.append((x, y))

        return arcs

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # populate with all arcs if arcs not provided
        queue = arcs if arcs is not None else self.get_arcs()

        while queue:
            x, y = queue.pop(0)

            # if x's domain updated
            if self.revise(x, y):
                # no solution
                if not self.domains[x]:
                    return False

                # check other arcs associated with x
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # cool one-liner
        return all((var in assignment) for var in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # test 1: check all values are distinct
        if not len(assignment.keys()) == len(set(assignment.values())):
            return False

        # test 2: check all values are with correct length
        if not all(var.length == len(assignment[var]) for var in assignment):
            return False

        # test 3: check no conflicts between neighboring variables
        # populate with all arcs
        queue = self.get_arcs()

        for x, y in queue:
            # skip irrelavent arcs
            if x not in assignment or y not in assignment:
                continue

            word_x = assignment[x]
            word_y = assignment[y]
            i, j = self.crossword.overlaps[x, y]

            # different letters on overlapping cell
            if word_x[i] != word_y[j]:
                return False

        # congrats, you passed all tests!
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # unassigned_neighbors = unassigned_vars ∩ neighbors
        unassigned_vars = self.crossword.variables - set(assignment.keys())
        neighbors = self.crossword.neighbors(var)
        unassigned_neighbors = set.intersection(unassigned_vars, neighbors)

        domain_values = dict()

        for var_word in self.domains[var]:
            # init number of constraining values
            domain_values[var_word] = 0

            for nb in unassigned_neighbors:
                i, j = self.crossword.overlaps[var, nb]

                for nb_word in self.domains[nb]:
                    # duplicate and nonoverlapping words will be ruled out
                    if var_word == nb_word or var_word[i] != nb_word[j]:
                        # increment number of constraining values
                        domain_values[var_word] += 1

        # sort by number of constraining values
        ordered_domain_values = [val for val, count in sorted(domain_values.items(), key=lambda x: x[1])]

        return ordered_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = []

        for var in self.crossword.variables - set(assignment.keys()):
            remaining_values = len(self.domains[var])
            degree = len(self.crossword.neighbors(var))

            unassigned_vars.append((var, remaining_values, degree))

        # first sort by number of remaining values, then sort reversely by degree
        unassigned_vars.sort(key=lambda x: (x[1], -x[2]))

        # return variable with highest degree among those with least remaining values
        return unassigned_vars[0][0]

    def inference(self, assignment):
        """
        Used for enforcing arc-consistency after every new assignment of the backtracking search to improve efficiency.

        `assignment` is a mapping from variables (keys) to words (values).

        Outputs all the inferences that can be made through enforcing arc-consistency.
        """
        # run ac3 with all arcs, terminate if no solition
        if not self.ac3():
            return None

        inferences = {var: next(iter(words)) for var, words in self.domains.items() if var not in assignment and len(words) == 1}

        return inferences

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # terminate if assignment is done
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for val in self.order_domain_values(var, assignment):
            # update assignment if new assigned value does not violate consistency
            if self.consistent(assignment | {var: val}):
                assignment[var] = val

                # make inference by enforcing arc-consistency
                inferences = self.inference(assignment)

                if inferences:
                    assignment = assignment | inferences

                # go to next level
                result = self.backtrack(assignment)

                # yay
                if result:
                    return result

                # return to current level and revert to original assignment
                del assignment[var]

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
