import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP | S P S
NP -> N | Det N | AP N
AP -> Adj | Adj AP | Det AP
VP -> V | V NP | V NP PP | V PP | Adv VP | VP Adv
PP -> P NP | PP PP
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
    return [word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word)]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunk_list = []

    # Loop through subtrees whose label is 'NP'
    for s in tree.subtrees(lambda t: t.label() == 'NP'):
        # If s is here, it is a potential candidate to be in np_chunk
        # Now we need to assess if it does not contain any other noun phrases as subtrees

        # Check if there is any NP as subtree of s
        np_subtree_check = any([ss.label() == 'NP' for ss in s.subtrees() if ss != s])
        
        # If check is false, add it to np_chunk list
        if not np_subtree_check:
            np_chunk_list.append(s)

    # Return list with all chunks obtained in the loop
    return np_chunk_list


if __name__ == "__main__":
    main()
