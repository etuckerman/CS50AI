# = https://submit.cs50.io/check50/5628f9f0e8e4eec15cc21e19e762e281d36f69c5

import csv
import sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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
    month_dict = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    
    df = pd.read_csv(filename)
    print(df.head(10))
    
    # Split DataFrame into 'evidence' and 'labels'
    
    #  selects all columns except the last one.
    evidence = df.iloc[:, :-1]
    
    #  selects the last column.
    labels = df.iloc[:, -1]
    
    print(evidence.head(10))
    print(labels.head(10))
    
    #Administrative, Informational, ProductRelated, Month, 
    # OperatingSystems, Browser, Region, TrafficType, VisitorType, 
    # and Weekend should all be of type int
    evidence['Administrative'] = evidence['Administrative'].astype(int)
    evidence['Informational'] = evidence['Informational'].astype(int)
    evidence['ProductRelated'] = evidence['ProductRelated'].astype(int)
    evidence['Month'] = evidence['Month'].apply(lambda x: month_dict.index(x))
    evidence['OperatingSystems'] = evidence['OperatingSystems'].astype(int)
    evidence['Browser'] = evidence['Browser'].astype(int)
    evidence['Region'] = evidence['Region'].astype(int)
    evidence['TrafficType'] = evidence['TrafficType'].astype(int)
    evidence['VisitorType'] = evidence['VisitorType'].apply(lambda x: 1 if x == 'Returning_Visitor' else 0)
    evidence['Weekend'] = evidence['Weekend'].apply(lambda x: 1 if x == True else 0)
    
    #Administrative_Duration, Informational_Duration, ProductRelated_Duration,
    # BounceRates, ExitRates, PageValues, and SpecialDay should all be of type float.
    
    evidence['Administrative_Duration'] = evidence['Administrative_Duration'].astype(float)
    evidence['Informational_Duration'] = evidence['Informational_Duration'].astype(float)
    evidence['ProductRelated_Duration'] = evidence['ProductRelated_Duration'].astype(float)
    evidence['BounceRates'] = evidence['BounceRates'].astype(float)
    evidence['ExitRates'] = evidence['ExitRates'].astype(float)
    evidence['PageValues'] = evidence['PageValues'].astype(float)
    evidence['SpecialDay'] = evidence['SpecialDay'].astype(float)
    
    #Each value of labels should either be the integer 1, if the user did go through with a purchase, or 0 otherwise.
    labels = labels.apply(lambda x: 1 if x == True else 0)
    
    print(evidence.head(10))
    print(labels.head(10))
    #print the first row of evidence
    print(evidence.iloc[0])
    #print the first value of labels
    print(labels.iloc[0])
    return(evidence, labels)
    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    k = 1

    #create test and train data and determine test train split
    X_train, X_test, y_train, y_test = train_test_split(evidence, labels, test_size = TEST_SIZE, random_state = 42)
    
    knn = KNeighborsClassifier(n_neighbors = k)
    
    knn.fit(X_train, y_train)
    
    return knn


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Convert predictions and labels to pandas Series
    labels = pd.Series(labels)
    predictions = pd.Series(predictions)
    
    # Calculate True Positives, False Negatives, True Negatives, and False Positives
    true_positives = ((labels == 1) & (predictions == 1)).sum()
    false_negatives = ((labels == 1) & (predictions == 0)).sum()
    true_negatives = ((labels == 0) & (predictions == 0)).sum()
    false_positives = ((labels == 0) & (predictions == 1)).sum()


    #values of 1 are: true positives and false negatives
    #values of 0 are: true negatives and false positives
    
    # Calculate Sensitivity and Specificity
    #how accurate values of 1 are
    sensitivity = true_positives / (true_positives + false_negatives)
    
    #how accurate values of 0 are
    specificity = false_positives / (false_positives + true_negatives)
    
    return(sensitivity, specificity)
    
    


if __name__ == "__main__":
    main()
