# Neural networks

- Neurons are connected to and receive electrical signals from other neurons
- Neurons process input signals and can be activated

## Artificial Neural Network (ANN): mathematical model for learning inspired by biological neural networks
- Model mathematical function from inputs to outputs based on the structure and parameters of the network
- Allows for learning the network's parameters based on data

Neuron will be a unit (kind of a node in a graph)
Units can be connected to each other

Inputs (x1, x2) --> Perform a task (ex: tell whether it is going to rain)
how we did it before:
h(x1, x2) = w0 + w1x1 + w2x2
x1, x2: inputs
w0, w1, w1: weights

activation function possibilities:
- step function: for some values output is 0, for others output is 1 (rain)
- logistic sigmoid function: g(x) = eˆx / (eˆx + 1) (represents probability of raining)
- rectified linear unit (ReLU): g(x) = max(0, x)
any of them:
h(x1, x2) = g(g0 + w1x1 + w2x2)  (g is the activation function)

representing this as a neural network:
x1 unit -(w1)-> output unit
x2 unit -(w2)-> output unit
output unit = g(w0 + w1x1 + w2x2)

Example:
- Or function: how can we train a neural network to do the Or function?
w1 = w2 = 1
bias (w0) = -1
step function as activation with step on 0 (where it goes from 0 to 1 on y axis)
inputs 0 and 0: result is -1 + 0 + 0 = -1, after activation 0
inputs 1 and 0: result is -1 + 1 + 0 = 0, after activation 1
inputs 1 and 1: result is -1 + 1 + 1 = 1, after activation 1

- And function
w1 = w2 = 1
bias (w0) = -2
step function as activation with step on 0 (where it goes from 0 to 1 on y axis)
inputs 0 and 0, result is -2, after activation 0
inputs 0 and 1: result is -1, after activation 0
inputs 1 and 1: result is 0, after activation 1

generalizing:
ex1:
first unit: humidity
second unit: pressure
output unit: probability of rain

ex2:
first unit: advertising
second unit: month
output unit: sales

could have more than 2 inputs (units): could be n

and/or functions: simple enough for us to tell what are the weights:
in a given problem: how we train a neural network to find the weights?

how we do this: gradient descent

## gradient descent: algorithm for minimizing loss when training neural network

## Gradient descent implementation
- Start with a random choice of weights
- Repeat:
    - Calculate the gradient based on *all data points*: direction that will lead to decreasing loss
    - Update weights according to the gradient

Purple part is the computational expensive part

Solutions:
- Stochastic gradient descent: use one random data point instead
- Mini-batch gradient descent: use one small batch instead

We can also have more than one output: we will a form a net of inputs and outputs, and each input-output pair will have its weight
ex for multiple outputs: weather, we could do multiple classifications (one output is rainy, one output is sunny, one output is cloudy, in the result we would have the probability of each one in the outputs)

we could use neural networks in reinforcement learning:
ex: inputs are data we have, outputs are possible actions: we choose action that had higher output (probability)

training a neural network with 4 outputs = training 4 independent neural networks (one output at a time, with its own weights)

limintation: only can predict things that are linearly separable (ex: can draw a line to separate red and blue balls, but can't draw a circle)
- Single perceptron: only capable of learning linearly separable decision boundary

solution:
## multilayer neural network: artificial neural network with an input layer, an output layer, and at least one hidden layer

in practice, each unit of the hidden layer defines one of the boundaries (a line, for example)

how do we train a neural network with hidden layers? (we only have data for inputs and outputs):

if you calculate the error of the output and you know the weights from hidden layer to output, you can calculate an estimate of how much of error is coming from each unit of hidden layer ==> Back-propagate the error from output to hidden layer
- Backpropagation: algorithm for training neural networks with hidden layers
Pseudocode:
- Start with a random choice of weights
- Repeat:
    - Calculate error for output layer
    - For each layer, starting with output layer, and moving inwards towards earliest hidden layer:
        - Propagate the error back one layer
        - Update weights

# deep neural networks: neural network with multiple hidden layers (deep learning)

risk: overfitting
dealing with overfitting in neural networks: dropout
- dropout: temporarily removing units - selected at random - from a neural network to prevent over-reliance on certain units (prevent overfitting)

neural network libraries
most popular: tensorflow
playground.tensorflow.org

import tensorflow as tf

model = tf.keras.models.Sequential()
(sequential because one layer comes after another)
(keras is an api)

- add hidden layer
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))
(dense layer: each of the nodes from layer is connected to each of the nodes from previous layer)
(we have 4 inputs)

- add output layer
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

with more layers, we can apply it to more complex problems

# computer vision
computational methods for analyzing and understanding digital images
image: a grid of pixels filled with a particular color
you can represent each pixel with a number from 0 to 255 (color)
or with three numbers (RGB)

deep neural network to get which number is a handwritten one:
for each pixel of image, 1 (or 3 if RGB) inputs (nodes)
hidden layers
outputs are 0 to 9 (probability of being each one of them)
issues:
- a lot of weights to calculate
- we lose access to information about the macro-structure of the image by having pixels as inputs

ideas to extract info from an image:
- image convolution: applying a filter that adds each pixel value of an image to its neighbors, weighted according to a kernel matrix (you may predict curves, lines, etc)
explanation in 00:59:00
useful to detect edges, etc -> strip out details and get most important features of image

- pooling: reducing the size of an input by sampling from regions in the input
(take a big image and turn into a small image)
- max-pooling: pooling by choosing the maximum value in each region

- convolutional neural network: neural networks that use convolution, usually for analyzing images
    - start with an input image
    - rather than immediately put that into the neural network, we apply a convolution step in the image (usually multiple times), outputting multiple feature maps (one for each convolution done)
    - apply pooling in the feature maps to reduce their size
    - flatten out the inputs from the feature maps, and this become the input to a neural network

you could do convolution-pooling multiple times before feeding it into a neural network
first convolution-pooling: highlight low-level features: identify edges, curves, shapes
second convolution-pooling: high-level features: identify objects


## abstract reprsentation of neural network

- feed-forward neural network: neural network that has connections only in one direction
input -> network -> output
this is a one-to-one neural network (one input -> one output, ex: the number handwritten in the image)

- recurrent neural network: network passes information to itself
this allows one-to-many neural networks (one input -> many outputs, ex: a sentence describing an image)
input -> network -> output (first word of sentence)
         | (output)
         v
         network (same one) -> output (second word of sentence)
         |
         v
         ...

videos: we can use recurrent neural network to pass multiple frames of video as inputs (1:36:00)

Google translate: takes text written in one language and convert to text in other language
we can't translate word by word because each language structure things differently
we can use recurrent neural network to pass each word at a time to a neural network (first word, then second word + output of first word to second neural network, then third word + output of second word to neural network, etc...)
