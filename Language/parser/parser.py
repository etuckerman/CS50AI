# = https://submit.cs50.io/check50/d777e7a2fe4346d4f7fcaf71086190167541c824

import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


NONTERMINALS = """
S -> N V | NP VP | VP NP | S Conj S
NP -> N | Det N | NP PP | Det ADJP N
VP -> V | V PP | V NP | VP Adv | Adv VP
PP -> P NP
ADJP -> Adj | Adj ADJP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    #tokenize using word_tokenize to split sentence into words
    #params for tokenizer: lowercase string, contains at least one alphabetic char

    words = nltk.word_tokenize(sentence)
    processed_words = []

    for word in words:
        # Check if the word contains at least one alphabetic character
        has_alpha = False
        for char in word:
            if char.isalpha():
                has_alpha = True
                break

        # If the word contains an alphabetic character, convert to lowercase and add to the list
        if has_alpha:
            processed_words.append(word.lower())

    return processed_words

    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    #initialize list of noun phrase chunks
    np_chunks = []

    #iterate through each subtree in the tree
    for subtree in tree.subtrees():
        #if subtree is a noun phrase
        if subtree.label() == "NP":
            #initialize flag to check if subtree contains another noun phrase
            contains_np = False
            #iterate through each subtree in the subtree
            for subsubtree in subtree.subtrees():
                #if subtree is a noun phrase
                if subsubtree.label() == "NP" and subsubtree != subtree:
                    contains_np = True
            #if subtree does not contain another noun phrase, add to list of noun phrase chunks
            if contains_np == False:
                np_chunks.append(subtree)

    return np_chunks
    # raise NotImplementedError


if __name__ == "__main__":
    main()
