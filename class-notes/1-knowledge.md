knowledge-based agents: agents that reason by operating on internal representations of knowledge

sentence: an assertion about the world in a knowledge representation language

- propositional logic:
propositional symbols: P, Q, R (each one represents a sentence/fact about the world)

logical connectives:
not: ¬ (option + L)
and: ^
or: v
implication ->
biconditional: <->


not: inverts meaning
P    |  ¬P
false  true
true   false

and: true when both operands are true
false and false: false
false and true: false
true and false: false
true and true: true

or: true when one of operands is true (or both are true)
false and false: false
false and true: true
true and false: true
true and true: true

(Xor: true when only one of operands are true, won't be focused)

implication:
ex: if it's sunny (P), i'll be outdoors (Q)
P: it's sunny: true (it is actually sunny)
Q: i'll be outdoors: false (i'm not outdoors)
therefore, the implication is false (because i'm not outdoors)

when P is false, it is impossible to evaluate the implication
P    |    Q   |   P -> Q
false| false  |  true
false| true   |  true
true | false  |  false
true | true   |  true

biconditional: condition that goes in both directions
(if and only if)
only true and P and Q are both true or both false
P    |    Q   |   P <-> Q
false| false  |  true
false| true   |  false
true | false  |  false
true | true   |  true

# model: assignment of a truth value to every propositional symbol (a "possible world")
Example: if I have two propositional symbols:
P: It is raining
Q: It is a Tuesday
sample model: {P=true, Q=false}
if there are n symbols, there are 2ˆn possible models (because each one can be true or false)

knowledge base: a set of sentences known by a knowledge-based agent

entailment (|=)
(alpha and beta are sentences)
alpha |= B means "In every model in which sentence alpha is true, sentence beta is also true"
Example:
alpha: It is Tuesday in January
beta: It is January

inference: the process of deriving new sentences from old ones

Example:
P: It is a Tuesday
Q: It is raining
R: Harry will go for a run

Knowledge base (KB):
1) (P ^ ¬Q) -> R
(Reads as: P and notQ implies R)
(Or: If it is Tuesday and it is not raining, Harry will go for a run)
2) P
3) ¬Q

P ^ ¬Q (P and notQ) is true only if P and notQ are true, which happens
if P and notQ is true, R is true
inference: R is true: Harry will go for a run

Given a knowledge base (KB) and a sentence alpha, does KB entails alpha (KB |= alpha)? (if KB is true, alpha is also true)

# Model checking:
To determine if KB |= alpha:
    - Enumerate all possible models
    - If in every model where KB is true, alpha is true, then KB entails alpha
    - Otherwise, KB does not entail alpha

Ex: If there's a KB with P, Q and R, "all models" will be all combinations of P, Q and R being true or false (2ˆ3 = 8 models)
Ask in each one of them: Is the knowledge base true here?

Knowledge engineering: take a problem and think about how to distill it down into knowledge that is representable by a computer

Clue: one person, one room and one weapon is the solution of the game

we want to infer what is the solution based on logic
propositional symbols:
- mustard, plum, scarlet (person)
- ballroom, kitchen, library (room)
- knife, revolver, wrench (weapon)

KB (knowledge base):
- (mustard v plum v scarlet) (one of those was the murder)
- (ballroom v kitchen v library)
- (knife v revolver v wrench)
- ¬plum (because his card is in my hand)
- ¬mustard v ¬library v ¬revolver (this guess was wrong, so one of them is wrong)
in python:
_
mustard = Symbol("Cl. Mustard") etc
knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench),
    )
knowledge.add(Not(mustard)) # card in hand
knowledge.add(Not(kitchen)) # card in hand
knowledge.add(Not(revolver)) # card in hand
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench)
    )) # wrong guess by another player
knowledge.add(Not(plum)) # someone showed prof plum card

Now we can conclude that it was Ms. Scarlet logically

knowledge.add(Not(ballroom))

Now we know its ms scarlet, library, knife
_

Issue with model check: exhaustive, consumes a lot of processing

# Inference rules - eliminates pieces of information by joining them together in the knowledge
- modus ponens: if we know alpha -> beta, and we know alpha is true, therefore beta is true
- and elimination: if we know alpha and beta are true, we know alpha is true
- double negation elimination: if we know not(not alpha) is true, we know alpha is true
- implication elimination: if alpha -> beta, then either not alpha or beta (¬a v b)
- biconditional elimination: if alpha <-> beta, then (alpha -> beta) ^ (beta -> alpha) (alpha implies beta and beta implies alpha)
- de morgan's law: if it's not true that alpha and beta , then either not alpha or not beta [if ¬(a ^ b), then (¬a v ¬b)]
- de morgan's law: [if ¬(a v b), then (¬a ^ ¬b)]
- distributive property: if (a ^ (b v g)), then (a ^ b) v (a ^ g)
- distributive property: if (a v (b ^ g)), then (a v b) ^ (a v g)

Theorem proving: we can use search to solve this problem
- initial state: starting knowledge base (KB)
- actions: inference rules
- transition model: new knowledge base after Inference
- goal test: check statement we're trying to prove
- path cost function: number of steps in proof

# Resolution
ex: (v is or)
(Ron is in the great hall) v (Hermione is in the library)
Ron is not in the great hall
therefore Hermione is in the library
Resolution rule: if we know P v Q, and we know ¬P, then Q

We can generalize it:
P v Q1 v Q2 V ... v Qn
¬P
then Q1 v Q2 V ... v Qn

We can generalize it ever further:
(Ron is in the great hall) v (Hermione is in the library)
(Ron is not in the great hall) v (Harry is sleeping)
then (Hermione is in the library) or (Harry is sleeping)
---
P v Q
¬P v R
then Q v R
---
P v Q1 v Q2 V ... v Qn
¬P v R1 v R2 V ... v Rm
then
(Q1 v Q2 V ... v Qn) ^ (R1 v R2 V ... v Rm) # CHECK THIS

- Clause: a disjunction of literals (disjuction: things connected with 'or'; literals: propositional symbols (P) or not (¬P))
e.g. P v Q v R

- Conjunctive normal form (CNF): logical sentence that is a conjunction of clauses
(conjunction: things connected with 'and')
e.g. (A v B v C) ^ (D v ¬E) ^ (F v G)

we can take any sentence and transform it in conjunctive normal form by applying inference rules and transformations

Conversion to CNF:
- Eliminate biconditionals
    - turn (a <-> b) into (a -> b) ^ (b -> a)
- Eliminate implications
    - turn (a -> b) into ¬a v b
- Move ¬ inwards using De Morgan's Laws
    - turn ¬(a ^ b) into ¬a v ¬b
---- Now we have only ands (^) and ors (v)
- Use distributive law to distribute v whenever possible
---- Now we should have ands outside the clauses and ors inside clauses

Example of conversion to CNF
(P v Q) -> R
¬(P v Q) v R                    # eliminate implication
(¬P ^ ¬Q) v R                   # de morgan's law
(¬P v R) ^ (¬Q v R)             # distributive law
converted!

once the sentence is in CNF, we can use resolution's law to resolve them
this process is called inference by resolution
P v Q
¬P v R
then (Q v R)

some points:
P v Q v S
¬P v R v S
then (Q v S v R v S) = (Q v S v R)

P
¬P
then ()
empty clause () is always false

Inference by resolution (algorithm):
To determine if KB |= a:
    - Check if (KB ^ ¬a) is a contradiction?
        - If so, then KB |= a
        - Otherwise, no entailment

more detailed steps:
To determine if KB |= a:
    - Convert (KB ^ ¬a) to Conjunctive Normal Form
    - Keep checking to see if we can use resolution to produce a new clause
        - If ever we produce the empty clause (equivalent to False), we have a contradiction, and KB |= a
        - Otherwise, if we can't add new clauses, no entailment

actual example:
Does (A v B) ^ (¬B v C) ^ (¬C) entail A?
- First step: convert (KB ^ ¬A) to Conjunctive normal form
(A v B) ^ (¬B v C) ^ (¬C) ^ (¬A)
- Now I have four different clauses:
(A v B)
(¬B v C)
(¬C)
(¬A)
- I can resolve clause (¬B v C) and clause (¬C) because they are complementary literals -> If (¬B v C) and (¬C), then ¬B
new clause generated: (¬B)
- Now I have five different clauses:
(A v B)
(¬B v C)
(¬C)
(¬A)
(¬B)
- I can resolve clause (¬B) and clause (A v B): A
- Now I have six different clauses:
(A v B)
(¬B v C)
(¬C)
(¬A)
(¬B)
A
- I can resolve clause (¬A) and clause (A): It's a contradiction, therefore KB |= A (knowledge base entails A)

Limitations in propositional logic: It may lead to a lot of symbols (ex: harry potter puzzle with people and hogwars houses)

# First-order logic:
More powerful

How it was in propositional logic:
Propositional symbols:
- MinervaGryffindor
- MinervaHufflepuff
- MinervaRavenclaw
- MinervaSlytherin
...

How it would be in first-order logic:
Constant symbol:
- Minerva
- Pomona
- Horace
- Gilderoy
- Gryffindor
- Hufflepuff
- Ravenclaw
- Slytherin
Predicate symbol:
- person
- house
- belongs to

Example:
Person(Minerva)                         # Minerva is a person
House(Gryffindor)                       # Gryffindor is a house
¬House(Minerva)                         # Minerva is not a house
BelongsTo(Minerva, Gryffindor)          # Minerva belongs to gryffindor

there are also two quantifiers
- Universal quantification: lets me express an idea, for ex: that something is true for all values of x (upside down A)
ForAll x.BelongsTo(x, Gryffindor) -> ¬BelongsTo(x, Hufflepuff)
(or) For all objects x, if x belongs to Gryffindor, then x does not belong to Hufflepuff
(or) Anyone in gryffindor is not in hufflepuff

- Existential quantification: lets me express an idea, for ex: that something is true for some values of x (at least one) (backwards E)
ThereExistsAn x.House(x) ^ BelongsTo(Minerva, x)
(or) There exists an object x such that x is a house and Minerva belongs to x
(or) Minerva belongs to a house

- Combining both
ForAll x.Person(x) -> (ThereExistsA y.House(y) ^ Belongsto(x, y))
(or) For all objects x, if x is a person, then there exists an object y such that y is a house and x belongs to y
(or) every person belongs to a house

Minesweeper:
Known issue: sometimes the AI is selecting cells as "safe" but they are not safe - the issue must be when we mark cells as safe; maybe test with a smaller board
