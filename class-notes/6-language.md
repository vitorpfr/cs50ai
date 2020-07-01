natural language processing

syntax: words make sense (subject, verb)

meaning:
- we can have two or more sentences with the same meaning
- there are sentences wit correct syntax but meaningless (ex: two conflicting adjectives)

# formal grammar
a system of rules for generating sentences in a language (what english structures are valid and what are not valid in syntax)

# context-free grammar
way of generating sentences in a language using rewriting rules

ex:
she saw the city
each word: terminal symbols
non terminal symbol associated with each word:
N V D N
N -> she, city, car, Harry (could be any of these)
D -> the, a, an
V -> saw, ate, walked
P -> to, on, over
ADJ -> blue, busy, old
NP (noun phrase) -> N (noun) or D N (determiner + noun)
VP (verb phrase) -> V or V NP (ex: saw or "saw the city")
S (sentence) -> NP VP

python lib: nltk (natural language toolkit)

i ate a car: syntax is correct, but it doesn't make sense
some words go (or dont go) together with others

# n-gram
a contiguous sequence of n items from a sample of text

# word n-grams
a contiguous sequence of n words from a sample of text

# unigram
a contiguous sequence of 1 item from a sample of text

# bigram
a contiguous sequence of 2 items from a sample of text

# trigram
same (seq of 3 words)

# tokenization
the task of splitting a sequence of characters into pieces (tokens)

# word tokenization
the task of splitting a sequence of characters into words

split method in python (using space " ")
issue: punctuation goes with words

if we count all the trigrams of a text and order by freq. we can try to predict things: ex: if the most popular trigram is i-think-that and we see i-think, there's a reasonable chance that the next word is 'that'

We can use markov model to do this:
ex: markov folder in src (markovify lib)

stopped in 42:41

# text categorization
have a sample of text and want to put inside a category,
- should this e-mail go to inbox or spam
- sentiment analysis: does this text have a positive or negative meaning?

# bag-of-words model
model that represents text as an unordered collection of words
(does not care about word structure, only about which words are there)

# naive bayes approach
bayes rule: P(b|a) = P(a|b) * P(b) / P(a)
want to calculate P(+) and P(-) (sentiment)

ex: My grandson loved it
P(+ | "my grandson loved it") = P(+ |"my", "grandson", "loved", "it")
applying bayes rule:

= P("my", "grandson", "loved", "it" | +) * P(+) / P("my", "grandson", "loved", "it")

proportional to
P("my", "grandson", "loved", "it" | +) * P(+)
applying joint probability rule
= P(+, "my", "grandson", "loved", "it")
simplifying (naive): these words are independent of each other (having the word "loved" doesn't change the probability of having the word "grandson" in there)

naively proportional to:
P(+) * P("my"|+) + P("Grandson"|+) + P("loved"|+) + P("it"|+)
(this is something we can calculate with past data!)

Calculate this for + and for -, then normalize the result
result:
positive 0.68
negative 0.32
it seems like we are 68% confident that this message is a positive review

- issue: we may have P("Grandson"|+) as 0, for example (not enough reviews data): this will result as the probability of being positive as 0 (because of the multiplication)

how to solve:
- additive smoothing: adding a value alpha to each value in our distribution
- Laplace smoothing: adding 1 ot each value in our distribution pretending we've seen each value one more time than we actually have

- nltk package have naive bayes too: sentiment in src

# information retrieval
the task of finding relevant documents in response to a user query
starts from getting the topic of a document

## topic modeling
models for discovering the topics for a set of documents

## term frequency
- number of times a term appears in a document

- function words: words that have little meaning on their own, but are used to grammatically connect other words (an, by, do, is, the, with...)
- content words: words that have meaning independently (algorithm, category, computer)
in a topic modeling, we care only about content words

term frequency should exclude function words
issue: if we are analyzing sherlock holmes stories, the word "holmes" will appear in all, but this is expected

- inverse document frequency: measure of how common or rare a word is accross documents
log (totaldocuments / num of documents containing(word))
if a word appears in all docs: its inverse doc. frequency is 0 (log 1)

## tf-idf
ranking of what words are important in a document by multiplying term frequency (tf) by inverse document frequency (idf)

# semantics
## information extraction
the task of extracting knowledge from documents

ex: template: "when {company} was founded in {year}"
an AI can look the web for documents that match this pattern and discover the foundation year of companies

instead of giving AI the templates, we can give AI the data and it will try to find in which templates/pattern this data appear

## wordnet
- has all words and its possible meanings (like a dictonary), also has its category
nltk has it

## word representation
we need to transform words in vectors to use neural networks

## one-hot representation (encoding)
He wrote a book
he [1, 0, 0, 0]
wrote [0, 1, 0, 0]
a [0, 0, 1, 0]
book [0, 0, 0, 1]

not useful to represent numbers on a dictonary (55000 words would result in vectors of size 55000)
also not useful because close words will be totally different vectors (ex: wrote and authored, book and novel)

we want for similar words to have similar vectors representing each other

## distribution representation
representation of meaning distributed accross multiple values
he [0.34, -0.08, 0.02, -0.18...]
wrote [-0.27, 0.40, 0.00, -0.65, -0.15...]

similar words should have similar vector representations

what do the numbers mean?
"you shall know a word by the company it keeps"
we can define a word using the words that show around it

for xxx he ate
xxx = breakfast, dinner, etc.
words that can be in xxx are probably related

## word2vec
model for generating word vectors

## skip-gram architecture
neural network architecture for predicting context words given a target word

target words -> neural network -> context words prob. dist.
(lunch) -> neural network -> prob. dist. of words that appear in its context

target words are nodes in the first layer
weights are the numbers of the vector that represent a word


- you can subtract words (vectors): the result shows you what takes to go from word1 to word2

king - man = x

x + woman = ? (? is queen!)

if you do the same for paris and france (subtract), and apply the difference to england, the closest word of the result will be london
