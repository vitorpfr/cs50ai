import nltk
import sys
import os
import string
import math
from itertools import chain
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Set empty map to receive content
    content = {}

    # Loop through files in directory
    for file in os.listdir(directory):
        # Define path of current file
        file_dir = os.path.join(directory, file)

        # Open file object in read mode and add file content to map
        f = open(file_dir, "r")
        content[file] = f.read()
    
    # Return map with files content
    return content


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    return [word.lower() for word in nltk.word_tokenize(document) 
            if (word.lower() not in nltk.corpus.stopwords.words("english")
                and all([char not in string.punctuation for char in word.lower()]))]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Calculate number of documents
    number_of_docs = len(documents.keys())
    
    # Convert dict values to sets to avoid having a word counted twice in the same document
    docsets = {key: set(value) for key, value in documents.items()}

    # Calculate in how many documents each word appears
    word_frequency = Counter([x for x in chain(*docsets.values())])

    # Apply IDF formula to each frequency and return the result
    return {k: math.log(number_of_docs / v) for k, v in word_frequency.items()}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Define frequency counter map for words that appear in the query, with file as key
    frequency_counter = {filename: Counter([word for word in words_list if word in query])
                         for filename, words_list in files.items()}
    
    # Calculate tf-idf for each word and sum to get a score for each file
    scored_files = {filename: sum({word: (freq * idfs[word]) for word, freq in counter.items()}.values()) 
                    for filename, counter in frequency_counter.items()}

    # Generate ordered list of top files (by summed tf-idf score descending)
    sorted_files = sorted(scored_files.keys(), key=lambda k: scored_files[k], reverse=True)
    
    # Filter n first files and return it
    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Sum IDFs of words in each sentence to get a a matching word measure score (first sorting criteria)
    matching_word_measure = {sentence: sum({word: idfs[word] for word in words if word in query}.values())
                             for sentence, words in sentences.items()}

    # Get density of query terms for each sentence (second sorting criteria)
    query_term_density = {sentence: len([word for word in words if word in query]) / len(words) 
                          for sentence, words in sentences.items()}

    # Generate ordered list of top sentences by matching word measure and query term density
    sorted_sentences = sorted(matching_word_measure.keys(), 
                              key=lambda k: (matching_word_measure[k], query_term_density[k]), 
                              reverse=True)

    # Filter n first sentences and return it
    return sorted_sentences[:n]


if __name__ == "__main__":
    main()
