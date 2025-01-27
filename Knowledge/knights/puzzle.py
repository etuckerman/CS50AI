# https://submit.cs50.io/check50/713fd495891c659e19990fb7b45ed80ead4b66a5

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
    # A can only be a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is a knight, then A's statement (A is a knight and a knave) should be true
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a knave, then A's statement (A is a knight and a knave) should be false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a knight,
    # then A's statement (A is a knight and B is a knave)
    # should be true
    Implication(AKnight, And(AKnave, BKnave)),
    
    # If A is a knave,
    # then A's statement (A is a knight and B is a knave)
    # should be false
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # If A is a knight,
    # Then A and B are Knights or A and B are Knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    
    # If A is a knave,
    # Then A is a knight and B is a knave or A is a knave and B is a knight
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    
    # If B is a knight,
    # Then A is a knight and B is a nave or A is a knave and B is a knight
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If B is a knave,
    # Then A is a knight and B is a knight or A is a knave and B is a knave
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    # If A is a knight, then A's statement should be true
    Implication(AKnight, Or(AKnight, AKnave)),
    # If A is a knave, then A's statement should be false
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    
    # If B is a knight, then A's statement should be " I am a knave"
    Implication(BKnight, AKnave),
    # If B is a knave, then A's statement should be " I am a knight"
    Implication(BKnave, AKnight),
    
    # If B is a knight, then C is a knave
    Implication(BKnight, CKnave),
    # If B is a knave, then C is a knight
    Implication(BKnave, CKnight),
    
    # If C is a knight, then A is a knight
    Implication(CKnight, AKnight),
    # If C is a knave, then A is a knave
    Implication(CKnave, AKnave)
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
