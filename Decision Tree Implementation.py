import csv
import time
import operator
import pandas as pd
from sklearn.preprocessing import LabelEncoder

#Functions
    #Information Gain
    #Entropy

#Classes
    #(2 Children per Node)
    #Decision Node
    #Leaf Node
    #Question Class (type, operator, column, value)


def euclideanDistance(X_train, X_test, y_train, i):
    train_val = X_train
    test_val = X_test.iloc[i]
    distances = pd.DataFrame()
    for x in range(len(test_val)):
        distances[x] = pow(pow((train_val.iloc[:,x] - test_val[x]), 2),.5)
    distances = distances.sum(axis=1)
    distances = pd.concat([distances, y_train], axis=1)
    distances.columns = ['distance', 'churn']
    distances = distances.sort_values(by=['distance'])
    return distances


def getAccuracy(answers, predictions):
    correct = 0
    for p in range(len(predictions)):
        if answers.iloc[p] == predictions[p]:
            correct += 1
    accuracy = (correct / float(len(answers))) * 100.0
    print('Accuracy: ' + repr(round(accuracy, 2)) + '%')


def getClassification(predictions, distances, k):
    classx = {}
    for z in range(k + 1):
        response = distances.iloc[z,1]
        if response in classx:
            classx[response] += 1
        else:
            classx[response] = 0
    sortedx = sorted(
        classx.items(),
        key=operator.itemgetter(1),
        reverse=True)
    result = sortedx[0][0]
    predictions.append(result)


def loadDataset(filename):
    le = LabelEncoder()
    dataset = pd.read_csv(filename)
    for x in range(len(dataset.columns)):
        le.fit(dataset.iloc[:,x])
        dataset.iloc[:,x] = le.transform(dataset.iloc[:,x])
    y = dataset.iloc[:,-1]
    X = dataset.drop(['Churn'], axis=1)
    #Normalize all columns
    X = (X - X.mean())/X.std()
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print('Train set: ' + repr(len(X_train)), end=', ')
    print('Test set: ' + repr(len(X_test)))
    return X_test, y_test, X_train, y_train

if __name__ == "__main__":
    for t in range(0,11):
        start = time.time()
        k = 3
        predictions = []
        filename='Telco-Customer-Churn_training_data.csv'
        #Load the dataset
        X_test, y_test, X_train, y_train = loadDataset(filename)
        for i in range(len(X_test)):
            distances = []
            #Get distances for each point (Prediction against test)
            distances = euclideanDistance(X_train, X_test, y_train, i)
            #Classify each point based on distance
            getClassification(predictions, distances, k)    
        #Get accuracy of each classification
        getAccuracy(y_test, predictions)
        print("(Time to complete: " + str(round(time.time() - start, 1)) + "s)")
