from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # premise: A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # if and only if A is a knight, then A is both a knight and a knave
    Biconditional(AKnight, And(AKnight, AKnave)),
    # if and only if A is a knave, than A is not both a knight and a knave
    Biconditional(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # premise: A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # premise: B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # if and only if A is a knight, then A and B are both knaves
    Biconditional(AKnight, And(AKnave, BKnave)),

    # if and only if A is a knave, then A and B are not both knaves,
    # which in turn implies B is a knight
    Biconditional(AKnave, Not(And(AKnave, BKnave))),
    Implication(AKnave, BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # premise: A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # premise: B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # if and only if A is a knight, then A and B are the same kind
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # if and only if A is a knave, then A and B are of different kinds
    Biconditional(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # if and only if B is a knight, then A and B are of different kinds
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # if and only if B is a knave, then A and B are the same kind
    Biconditional(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # premise: A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # premise: B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # premise: C is either a knight or a knave, but not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # if and only if B is a knight, then A claimed to be a knave, and C is a knave
    Biconditional(BKnight, And(
        # if and only if A is a knight, then A is a knave
        Biconditional(AKnight, AKnave),
        # if and only if A is a knave, then A is a knight
        Biconditional(AKnave, AKnight)
    )),
    Biconditional(BKnight, CKnave),

    # if and only if B is a knave, then A claimed to be a knight, and C is a knight
    Biconditional(BKnave, And(
        # if and only if A is a knight, then A is a knight
        Biconditional(AKnight, AKnight),
        # if and only if A is a knave, then A is a knave
        Biconditional(AKnave, AKnave)
    )),
    Biconditional(BKnave, CKnight),

    # if and only if C is a knight, then A is a knight
    Biconditional(CKnight, AKnight),

    # if and only if C is a knave, then A is a knave
    Biconditional(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
