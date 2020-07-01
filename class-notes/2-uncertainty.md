Uncertainty: make inferences when we are not sure about things

Probability

Possible worlds: w (omega)
When you roll a die, there are 6 possible worlds, and each one has a probability P(w)

Axxioms:
0 <= P(w) <= 1
sum of P(w) for all w in W (all possible worlds) = 1

when we consider 2 dice:
P(sum to 12) = 1/36
P(sum to 7) = 6/36 = 1/6

- unconditional probability: degree of belief in a proposition in the absence of any other evidence (ex: P(sum to 12), P(sum to 7))

- conditional probability: degree of belief in a proposition given some evidence that has already been revealed, ex: P(a|b) probability of a given b, P(sum to 7 | first dice was 3)
P(rain today | rain yesterday)
P(pacient has a disease | test results)

formula: P(a|b) = P(a^b) / P(b)
another form: P(a^b) = P(b) * P(a|b)
another form: P(a^b) = P(a) * P(b|a)

P(sum 12 | first die was a 6) = ?
P(sum 12 and first die is a 6) = 1/36
P(first die is a 6) = 1/6
result = 1/6

- random variable: a variable in probability theory with a domain of possible values it can take on
format: random variable {values it can take on}
ex: variable Roll that has 6 possible values {1, 2, 3, 4, 5, 6}: in this case all have the same probability
ex: Weather {sun, cloud, rain, wind, snow}: in this case they do not have all the same probability
ex: Traffic {none, light, heavy}
ex: Flight {on time, delayed, cancelled}
random variable {values it can take on}

probability distribution: takes a random variable and gives the probability of each of the possible values
ex for Flight:
P(Flight = on time) = 0.6
P(Flight = delayed) = 0.3
P(Flight = cancelled) = 0.1

P(Flight) = <0.6, 0.3, 0.1>

independence: the knowledge that one event occurs does not affect the probability of the other event
for dice: one die does not impact the result of other
for weather: cloudy may be correlated to rain (they are not independent)
from before: P(a^b) = P(a) * P(b|a)
if they are independent, P(b|a) = P(b)
therefore P(a^b) = P(a) * P(b) ONLY IF THEY ARE INDEPENDENT!

an example that is not independent P(red die 6 ^ red die 4)
it is actually zero, but if you multiply the individual probabilities you would get 1/36 (you can't because they are not independent)
P(red die 6 ^ red die 4) = P(red die 6) * P(red die 4 | red die 6) = 1/6*0 = 0

- Bayes Rule:
P(a ^ b) = P(b)P(a|b)
P(a ^ b) = P(a)P(b|a)
P(a) * P(b|a) = P(b) * P(a|b)
dividing both sides by P(a):
we get bayes rule: *P(b|a) = (P(a|b) * P(b)) / P(a)*
this is important because we can express one conditional probability P(a|b) as a function of the other P(b|a)

Example
two events:
- cloudy in the morning (AM)
- rainy in the afternoon (PM)
Given clouds in the morning, what's the probability of rain in the afternoon?
information we have:
- 80% of rainy afternoons start with cloudy mornings
- 40% of days have cloudy mornings
- 10% of days have rainy afternoons

P(rain|clouds) = P(clouds|rain) * P(rain) / P(clouds)
               = 0.8 * 0.1 / 0.4
               = 0.2 = 20%
this means that knowing P(cloudy morning | rainy afternoon), we can calculate P(rainy afternoon | cloudy morning)
generalizing:
knowing P(visible effect | unknown cause), we can calculate P(unknown cause | visible effect)
example in real life:
knowing P(medical test result | person has a disease), I can calculate P(person has a disease | medical test result)

- Joint probability
example: I want to know about the prob. distribution of clouds in the morning (AM)
prob. distribution of AM:
C = cloud -> 0.4
C = ¬cloud -> 0.6
prob. distribution of PM:
R = rain -> 0.1
R = ¬rain -> 0.9
joint probability distribution:
            R = rain        R = ¬rain
C = cloud   0.08             0.32
C = ¬cloud  0.02             0.58

P(C | rain) = P(C, rain) / P(rain) = constant * P(C, rain)
conditional distribution of C (given rain) is proportional to the joint probability of C and rain
P(C | rain) = alpha * <0.08, 0.02> = <0.8, 0.2>

- Negation
P(¬a) = 1 - P(a)

- Inclusion-Exclusion (calculate 'or' probability)
P(a v b) = P(a) + P(b) - P(a ^ b)

- Marginalization (remembering , is AND (^))
P(a) = P(a,b) + P(a,¬b)

P(X = xi) = sum over j of P(X = xi, Y = yj)

On the joint distribution Example:
P(C = cloud) = P(C=cloud, R = rain) + P(C=cloud, R=¬rain)
             = 0.08 + 0.32
             = 0.4

- Conditioning (same rule, but using conditional instead of joint)
P(a) = P(a|b) * P(b) + P(a|¬b) * P(¬b)
P(X = xi) = sum over j of P(X=xi|Y=yi) * P(Y=yi)

# Probabilistic models
- Bayesian network: data structure that represents the dependencies among random variables
    - directed graph
    - each node represents a random variable (weather, train is on time)
    - arrow from X to Y means X is a parent of Y
    - each node X has probability distribution P(X | Parents(X)) (parents are the "causes" for some effect we are going to observe)

Example:

Rain {none, light, heavy} --> Maintenance {yes, no}
                |               |
                v               v
            Train {on time, delayed}
                    |  
                    v
            Appointment {attend, miss}

Rain: will not be conditional, because its values do not depend on anything (thre is no arrow pointing to it)
Rain {none 0.7, light 0.2, heavy 0.1}

Maintenance: will be a conditional distribution
            yes         no
Rain
none        0.4         0.6
light       0.2         0.8
heavy       0.1         0.9

Train: will be a conditional distribution, dependent on two nodes
R       M       on time         delayed
none    yes     0.8             0.2
none    no      0.9             0.1
light   yes     0.6             0.4
light   no      0.7             0.3
heavy   yes     0.4             0.6
heavy   no      0.5             0.5


Appointment: will be a conditional distribution, dependent on train node
T           attend      miss
on time     0.9         0.1
delayed     0.6         0.4

Computing joint probabilities
P(Rain=light) = 0.2
P(Rain=light, (and) Maintenance=no) = P(light) * P(no | light) (probability of light rain, times probability of no maintenance given light rain)

P(light, no, delayed) = P(light) *
                        P(no | light) *
                        P(delayed | light, no)

P(light, no, delayed, miss) =   P(light) *
                                P(no | light) *
                                P(delayed | light, no) *
                                P(miss | delayed)

# Inference

- Query X: variable for which to compute distribution
- Evidence variables E: observed variables for event e
- Hidden variables Y: non-evidence, non-query variable

- Goal: Calculate P(X | e)
I observe it is raining (e), I want to know the probability distribution over the variable X train (is it on time, is it delayed, etc)

Ex:
P(appointment | light, no)
Probability distribution of the appointment random variable, given that there's light rain and no maintenance
Train is a hidden variable here (it is not observed and also not in the query)

P(appointment | light, no) =                
constant * P(Appointment, light, no) =            (applying joint probability)
constant * [P(Appointment, light, no, on time)
            + P(Appointment, light, no, delayed)] (applying marginalization)

summary:
Inference by Enumeration
P(X | e) =
alpha * P(X, e) =
alpha * sum over y of P(X, e, y)        


# Approximate inference

- Sampling: Sample one of the values for each of the nodes according to probability distribution
random sample: R = none, M = yes, T = on time, A = attend
generate many of samples like this (ex: 8)
question: P(Train = on time)?
answer: Highlight the samples where the train is on time (6), so in 6 samples out of 8 the train was on time - approx. of answer is 6/8

another question (conditional): P(Rain=light | Train=on time)
answer: Ignore the samples where the train is delayed (don't match my evidence), highlight the samples where there's light rain (2), therefore 2 in 6

- Likelihood weighting
    - Start by fixing the values for evidence variables
    - Sample the non-evidence variabls using conditional probabilities in the Bayesian network
    - Weight each sample by its likelihood: the probability of all of the evidence

example:
P(Rain = light | Train = on time)?
start sampling by fixing the evidence variable: Train = On time
then sample for rain (light), sample for maintenance (yes), sample for appointment (attend)
then weight the sample: if rain=light and maintenance=yes, the likelihood of the train being on time os 0.6 -> this means this sample has a weight of 0.6

repeat the sample procedure and calculate the weight of each one

# Uncertainty over time
We've been considering the probability of raining or not, but what if we want to consider how this changes over time (probability of raining tomorrow? In the next day?)
Xt = Weather at time t

- Markov assumption: the assumption that the current state depends on only a finite fixed number of previous states

- Markov chain: a sequence of random variables where the distribution of each variable follows the Markov assumption

Transition model:
                        Tomorrow (Xt+1)
                        sunny   rainy
            sunny       0.8     0.2
Today (Xt)  rainy       0.3     0.7

X0 (sunny) -> x1 (sunny) -> x2 (rainy) -> x3 (rainy) -> x4 (rainy)

# Sensor models
Hidden State                     Observation
robot's position on Mars       robot sensor data
words spoken                   audio waveforms
user engagement                website or app analytics
weather                        whether or not people are using umbrella

- Hidden Markov Model: a Markov model for a system with hidden states that generates some observed event

Sensor model:
                        Observation (Et)
                        umbrella   not umbrella
            sunny       0.2            0.8
State (Xt)  rainy       0.9            0.1

- sensor Markov assumption: the assumption that the evidence variable depends only on the corresponding state (people bringing umbrellas depends entirely on if it's raining today)

task                definition
filtering       given observations from start until now, calcuilate
                distribution for current state
prediction      given observation from start until now, calculate
                distribution for a future state
smoothing       given distribution from start until now,
                calculate distribution for past state
most likely     given distribution from start until now,    
explanation     calculate most likely sequence of states

ex: given a sequence of observations (people using umbrella or not), what is the most likely sequence of weathers that caused this

real-life ex: given a pattern of audio waveforms, what is the most likely sequence of words that produced this audio waveform (audio recognition)


            # disclaimer: the chance of a person with one copy of passing the mutated gene is still 0.5,
            # because either the mutated gene and the non-mutated gene can undergo additional mutation
            # and therefore the mutation value cancels out
            # P(pass mutation) = P(select 1 and not mutation) + P(select 2 and mutation)
            # P(pass mutation) = 0.5 * (1 - mutation) + 0.5 * (mutation)
            # P(pass mutation) = 0.5

            # parent probability matrix when the person has zero genes
            # index i is mother_gene, index j is father_gene
            parent_probability[0] = [[(1 - mutation) * (1 - mutation), (1 - mutation) * 0.5, (1 - mutation) * mutation],
                                     [0.5 * (1 - mutation)           , 0.5 * 0.5           , 0.5 * mutation],
                                     [mutation * (1 - mutation)      , mutation * 0.5      , mutation * mutation]]

            # parent probability matrix when the person has one gene
            # index i is mother_gene, index j is father_gene
            parent_probability[1] = [[1, 1, ((1 - mutation) * (1 - mutation)) + (mutation * mutation)],
                                     [1, 1, 1],
                                     [1, 1, 1]]

            # parent probability matrix when the person has two genes
            # index i is mother_gene, index j is father_gene
            parent_probability[2] = [[mutation * mutation      , mutation * 0.5      , mutation * (1 - mutation)],
                                     [0.5 * mutation           , 0.5 * 0.5           , 0.5 * (1 - mutation)],
                                     [(1 - mutation) * mutation, (1 - mutation) * 0.5, (1 - mutation) * (1 - mutation)]]


joint_probability: issue must be here
update: ok
normalize: ok
