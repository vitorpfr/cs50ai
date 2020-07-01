# 1)
 For which of the following will you always find the same solution, even if you re-run the algorithm multiple times? *
Assume a problem where the goal is to minimize a cost function, and every state in the state space has a different cost.
1 point

Steepest-ascent hill-climbing, each time starting from a different starting state - NO
Steepest-ascent hill-climbing, each time starting from the same starting state - YES
Stochastic hill-climbing, each time starting from a different starting state - NO
Stochastic hill-climbing, each time starting from the same starting state - NO
Both steepest-ascent and stochastic hill climbing, so long as you always start from the same starting state - NO
Both steepest-ascent and stochastic hill climbing, each time starting from a different starting state - NO
No version of hill-climbing will guarantee the same solution every time - NO

ANSWER: Steepest-ascent hill-climbing, each time starting from the same starting state

The following two questions will both ask you about the optimization problem described below.

# 2)
A farmer is trying to plant two crops, Crop 1 and Crop 2, and wants to maximize his profits. The farmer will make $500 in profit from each acre of Crop 1 planted, and will make $400 in profit from each acre of Crop 2 planted.

However, the farmer needs to do all of his planting today, during the 12 hours between 7am and 7pm. Planting an acre of Crop 1 takes 3 hours, and planting an acre of Crop 2 takes 2 hours.

The farmer is also limited in terms of supplies: he has enough supplies to plant 10 acres of Crop 1 and enough supplies to plant 4 acres of Crop 2.

Assume the variable C1 represents the number of acres of Crop 1 to plant, and the variable C2 represents the number of acres of Crop 2 to plant.

- minimize a cost function c1x1 + c2x2 + ... + cnxn (linear equation)
- with constraints of form a1x1 + a2x2 + ... + anxn <= b
or of form a1x1 + a2x2 + ... + anxn = b
- with bounds for each variable li <= xi <= ui

profit equation (to be minimized)
P = 500*c1 + 400*c2
c1: acres of crop1
c2: acres of crop2

Answer: 500 * C1 + 400 * C2

constraints:
3*c1 + 2*c2 <= 12
C1 <= 10
C2 <= 4

Answer: 3 * C1 + 2 * C2 <= 12, C1 <= 10, C2 <= 4

B: Tue
F: Wed
Enforcing arc consistency:
C: Mon
A: Wed
D: {Mon, Wed}
E: {Tue, Wed}

C's domain is {Mon}, D's domain is {Mon, Wed}, E's domain is {Tue, Wed}
