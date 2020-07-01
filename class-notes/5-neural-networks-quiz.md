What value will this network compute for y given inputs x1 = 3, x2 = 2, and x3 = 4 if we use a step activation function? What if we use a ReLU activation function? *

y = w0 + w1x1 + w2x2 + w3x3

result: 11
step: 1
relu: 11

1 for step activation function, 11 for ReLU activation function


      x
x     x     x
x     x     x
x     x     x
      x     x



input to hidden:
for each input node: 5 weights
(3 nodes + bias) * 5 weights = 20

hidden to output:
for each hidden node: 4 weights
(5 nodes + bias) * 4 weights = 24
total: 44


Consider a recurrent neural network that listens to a audio speech sample, and classifies it according to whose voice it is. What network architecture is the best fit for this problem? *
Input: audio speech sample (one)
Output: Which person is speaking (one)

One-to-one (single input, single output)

[[16 12] [32 28]]
