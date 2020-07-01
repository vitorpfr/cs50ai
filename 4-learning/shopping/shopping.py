import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Load csv in a pandas dataframe, which already infers data int and float data types
    df = pd.read_csv(filename)

    # Set conversion dict to convert string columns to int
    conversion_dict = {
        'Month':        {'Jan': 0, 
                         'Feb': 1, 
                         'Mar': 2,
                         'Apr': 3,
                         'May': 4,
                         'June': 5,
                         'Jul': 6,
                         'Aug': 7,
                         'Sep': 8,
                         'Oct': 9,
                         'Nov': 10,
                         'Dec': 11},
        'VisitorType':  {'New_Visitor': 0,
                         'Other': 0,
                         'Returning_Visitor': 1},
        'Weekend':      {False: 0,
                         True: 1},
    }

    # Loop through evidence columns and convert string ones to int according to conversion dict
    for column in conversion_dict:
        df[column] = df[column].apply(lambda x: conversion_dict[column][x])

    # Set evidence as list of lists of the whole dataframe, removing the 17th element (which is the label)
    evidence = df.values.tolist()
    for x in evidence:
        del x[17]

    # Set label as list, converting boolean to int before
    labels = df['Revenue'].apply(lambda x: int(x)).tolist()

    # Return evidence and labels as tuple
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Define model with 1 neighbor and train on evidence and labels
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    # Return trained model
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Initialize counters to totals and labels correctly identified
    positive_labels_identified = 0
    negative_labels_identified = 0
    positive_labels = 0
    negative_labels = 0

    # Iterate through list of labels and predictions
    for label, prediction in zip(labels, predictions):

        # If label is positive, add to positive labels counter
        if label == 1:
            positive_labels += 1

            # Also, if prediction is also positive (model was right), add to identified counter
            if prediction == 1:
                positive_labels_identified += 1
        
        # If label is negative, add to negative labels counter
        elif label == 0:
            negative_labels += 1

            # Also, if prediction is also negative (model was right), add to identified counter
            if prediction == 0:
                negative_labels_identified += 1

    # Define sensitivity as the number of positive labels identified over total of positive labels
    sensitivity = positive_labels_identified / positive_labels

    # Define specificity as the number of negative labels identified over total of negative labels
    specificity = negative_labels_identified / negative_labels

    # Return tuple
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
