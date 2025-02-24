import copy
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
        if len(self.cells) == self.count:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return

        self.cells.remove(cell)
        self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell not in self.cells:
            return

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

        # mark move made
        self.moves_made.add(cell)

        # mark cell as safe
        self.mark_safe(cell)

        # explore unmarked neighbors
        neighbours, neighbor_mines = self.get_unmarked_neighbors(cell)

        count -= neighbor_mines

        # add new sentence to knowledge
        new_sentence = Sentence(neighbours, count)
        self.knowledge.append(new_sentence)

        # infer new knowledge
        self.infer_knowledge()

        # remove empty sentences
        self.remove_empty_sentences()

        updated = True

        # mark new safes and mines
        while updated:
            updated = self.mark_cells()

    def get_unmarked_neighbors(self, cell):
        """
        Returns set of unmarked neighbors of a cell and the number of mines around it
        """
        x, y = cell
        neighbors = set()
        mine_count = 0
        directions = [(i, j) for i, j in itertools.product([-1, 0, 1], repeat=2) if not (i == 0 and j == 0)]

        for (i, j) in directions:
            a, b = x + i, y + j

            if not (0 <= a < self.height and 0 <= b < self.width):
                continue

            if (a, b) in self.safes or (a, b) in self.moves_made:
                continue

            if (a, b) in self.mines:
                mine_count += 1
                continue

            neighbors.add((a, b))

        return neighbors, mine_count

    def mark_cells(self):
        """
        Marks cells as safe or mines based on knowledge
        """
        updated = False

        for sentence in self.knowledge:
            known_safes = sentence.known_safes()

            if known_safes:
                for cell in known_safes.copy():
                    self.mark_safe(cell)
                    updated = True

            known_mines = sentence.known_mines()

            if known_mines:
                for cell in known_mines.copy():
                    self.mark_mine(cell)
                    updated = True

        return updated

    def remove_empty_sentences(self):
        """
        Removes empty sentences from knowledge
        """
        for sentence in self.knowledge:
            if not sentence.cells:
                self.knowledge.remove(sentence)

    def infer_knowledge(self):
        """
        Infers new knowledge based on existing knowledge
        """
        inferred_sentences = []

        # infer new sentences
        for sentence, other in itertools.product(self.knowledge, self.knowledge):
            if sentence == other:
                continue

            if sentence.cells.issubset(other.cells):
                inferred_cells = other.cells - sentence.cells
                inferred_count = other.count - sentence.count

                inferred_sentence = Sentence(inferred_cells, inferred_count)

                inferred_sentences.append(inferred_sentence)
                updated = True

        # add inferred sentences to knowledge
        for sentence in inferred_sentences:
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
        # get all safe moves
        safe_moves = list(self.safes - self.moves_made)

        # return random safe move
        if safe_moves:
            return random.choice(safe_moves)

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # get all possible moves
        possible_moves = [(x, y) for x, y in itertools.product(range(self.height), range(self.width)) if (x, y) not in self.moves_made and (x, y) not in self.mines]

        # return random move
        if possible_moves:
            return random.choice(possible_moves)

        return None
