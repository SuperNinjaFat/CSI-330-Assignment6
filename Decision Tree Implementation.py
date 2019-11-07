import csv
import time
import operator
import numbers
import pandas as pd

#Functions
    #Information Gain
    #Entropy

#Classes
    #(2 Children per Node)
    #Decision Node
    #Leaf Node

def is_numeric(value):
    return isinstance(value, int)

class Question:
    def __init__(self, column, value, operator = '=='):
        self.column = column
        self.operator = operator
        self.value = value

    def ask_question(self):
        if is_numeric(self.value):
            print('is ' + str(self.column) + ' ' + str(self.operator) + ' ' + str(self.value) + '?')
        else:
            print('is ' + str(self.column) + ' equal to ' + str(self.value) + '?') 

    def answer_question(self, rows):
        for i, row in rows.iterrows():
            if is_numeric(self.value):
                if self.operator == '<':
                    print(row[self.column] < self.value)
                else:
                    print(row[self.column] >= self.value)
            else:
                print(row[self.column] == self.value)

if __name__ == "__main__":
    training_data = [
        ['Green', 3, 'Apple'],
        ['Yellow', 3, 'Apple'],
        ['Red', 1, 'Grape'],
        ['Red', 1, 'Grape'],
        ['Yellow', 3, 'Lemon']]

    training_data = pd.DataFrame(training_data, columns=['Color', 'Diameter', 'Fruit'])
    columns = training_data.columns

    q1 = Question(columns[0], 'Green')
    q1.ask_question()
    q1.answer_question(training_data)

    q2 = Question(columns[1], 3)
    q2.ask_question()
    q2.answer_question(training_data)
