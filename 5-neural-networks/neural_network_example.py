def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Initialize sequential model
    model = tf.keras.Sequential([

    # Add convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

    # Max-pooling layer
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add hidden layer with dropout
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),

    # Add output layer
    tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # Configure a model for mean-squared error regression.
    model.compile(optimizer="adam",
                loss="categorical_crossentropy",
                metrics=["accuracy"])

    return model
