# Machine learning
we are going to give the computer instruction on how to find a solution, but we will give data and let the computer figure out what are the patterns

# Supervised learning
given a dataset of input-output pairs, learn a function to map inputs to outputs

## classification
supervised learning task of learning a function mapping an input point to a discrete category (ex: is the bill fake or not, weather going to be cloudy or rainy?)

ex:
Date | Humidity | Pressure | Rain (binary target)

f(humidity, pressure)
f(93, 999.7) = Rain
f(49, 1015.5) = No Rain
f(79, 1031.1) = No Rain

hypothesis function: h(humidity, pressure)
goal: figure out what does h look like (so it is very close to f)

methods of classification:

1) nearest-neighbor classification: algorithm that, given an input, chooses the class of the nearest data point to that input
ex: closest data point we have to this is rain, so this should be rain

2) k-nearest neighbor classification: algorithm that, given an input, chooses the most common class out of the k nearest data points to that input
ex: closest k (ex: 7) data points are 5 no rain and 2 rain, therefore this should be no rain
downsides: could be slow (for each point, needs to measure distance to all points - nˆ2)

3) linear regression: draw a line that separates rainy days and non-rainy days

x1 = humidity
x2 = pressure
hypothesis fn:
w0, w1, w2: weights
1 means rain, 0 means not rain
h(x1, x2) = 1 if w0 + w1x1 + w2x2 >= 0
            0 rain, otherwise

weight vector w: (w0, w1, w2)
input vector x: (1, x1, x2)

objective: determine what are the weight values so we can make accurate preds
dot product: multiply values of same index and sum result
w . x = w0 + w1x1 + w2x2

hw(x) = 1 if w.x >= 0 ;
        0 otherwise

how to determine weights to linear regression:
- perceptron learning rule:
start with random weights, and given datapoint (x, y) (x is the vector of inputs, y is the output (rain or not rain)), update each weight according to: _ _wi = wi + a(y - hw(x)) * xi_
y: actual value
hw(x): estimate (what we thought the output was)
alpha: learning rate

threshold function:
x axis: w * x
y axis: output
graphical representation:
1        _________
0________|
 not rain    rain
this would be a hard threshold function (output is only 0 or 1)

soft threshold: logistic regression fn (output is any value between 0 and 1)
advantage: output reflects probability/likelihood

4) support vector machines: designed to try to find the maximum margin separator
- maximum margin separator: boundary that maximizes the distance between any of the data points (line in the middle, but could be a circle, anything)


## regression
supervised learning task of learning a function mapping an input point to a continuous value (ex: how much the value spent on ads translate to sales)
f(advertising)
    f(1200) = 5800
    f(2800) = 13400
    f(1800) = 8400
h(advertising)

- linear regression: draw a line that estimates the relationship between advertising and sales


# evaluating hypotheses
we are trying to minimize a loss function to determine the best function for our problem

## loss function: function that expresses how poorly our hypothesis performs

for discrete categories:
- 0-1 loss function:
L(actual, predicted) = 0 if actual = predicted,
                       1 otherwise
loss function is 1 for data points that we miscategorized

for continuous categories:
- L1 loss function:
L(actual, predicted) = |actual - predicted|
- L2 loss function (most popular):
L(actual, predicted) = (actual - predicted)^2

## overfitting
a model that fits too closely to a particular data set and therefore may fail to generalize to future data - it's hard to avoid, because an overfitted model will have a lower loss function in training data    (therefore it may appear that it is better)

cost(h) = loss(h)
this might overfit!

- regularization: penalizing hypotheses that are more complex to favor simpler, more general hypotheses

to avoid overfitting, add a complexity parameter (simple solutions are better):
cost(h) = loss(h) + lambda * complexity(h)
lambda is a parameter for us to choose how much do we want to penalize complexity

- holdout cross-validation: splitting data into a training set and a test set, such that learning happens on the training set and is evaluated on the test set

- k-fold cross-validation: splitting data into k sets, and experimenting k times, using each set as a test set once, and using remaining data as training set

library with all algorithms above: scikit-learn


# reinforcement learning
given a set of rewards or punishments, learn what actions to take in the future

- agent is situated in a environment
- environment puts agent in a state (ex: position in the world)
- agent needs to choose action (ex: where to move) and choose one
- agent get two things back from env: new state after action and a numerical reward (positive means action was good, negative means action was bad)
- with this information, agent needs to learn what actions to take in the future

## Markov decision process: model for decision-making, representing states, actions and their rewards

formal definition:
- set of states S
- set of actions ACTIONS(S)
- transition model P(s' | s, a) (given i'm in state s and take action a, what's the probability that I go to state s')
(it could be a deterministic world where given s and a we know s' for sure, but the world may have randomness too, therefore it would be a probability
- reward function R(s, a, s') (what is the reward from going to s to s' by doing a)

Q-learning: method for learning a function Q(s, a) estimate of the value of performing action a in state s:
- Start with Q(s, a) = 0 for all s, a
- When we take an action and receive a reward:
    - Estimate the value of Q(s, a) based on current reward and expected future rewards
    - Update Q(s, a) to take into account old estimate as well as our new estimate

defining:
- Start with Q(s, a) = 0 for all s, a
- Every time we take an action a in state s and observe a reward r, we update:

Q(s, a) <- Q(s, a) + alpha(new value estimate - old value estimate)
alpha: learning rate (how much we value new information vs how much we value old information)
when alpha is 1: throw away old estimation and update value with new est
when alpha is 0: ignore new information, keep only old information
writing again:
Q(s, a) <- Q(s, a) + alpha((r + future reward estimate) - Q(s, a))
future reward estimate = max a' of Q(s', a') (of all actions, which one gets the highest reward)

- Greeding decision-making policy
    - When in state s, choose action a with highest Q(s, a) (estimated value of taking action)

contradiction: Explore (trying other actions) vs Exploit (using knowledge that AI already has)
if we only explore, we don't optimize for reward
if we only exploit, we don't discover new paths that could be better

- Epsilon-greedy:
    - set epsilon equal to how often we want to move randomly
    - with probability 1 - epsilon, choose estimated best move
    - with probability epsilon, choose random move

this can be good for the AI to "learn" how to play games
issue: this get very complex in games with more states (ex: chess)

- function approximation:
approximating Q(s, a), often by a function combining various features, rather than storing one value for every state-action pair
useful when it's not feasible to explore all possible states

# unsupervised learning
given input data without any additional feedback, learn patterns

- clustering: organizing a set of objects into groups in such a way that similar objects tend to be in the same group

some clustering applications:
    - genetic research
    - image segmentation
    - market research
    - medical imaging
    - social network analysis

- k-means clustering: algorithm for clustering data based on repeteadly assigning points to clusters and updating those clusters' centers
- select centers of cluster randomly
    - assign each point to a cluster (the center closest to the point)
    - reposition cluster centers in the weighted average position of cluster points
    - repeat
    - stop when the cluster centers and assignments are not changing anymore

Summmary:
Learning:
- Supervised learning
- Reinforcement learning
- Unsupervised learning
