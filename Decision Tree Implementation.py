import csv
import math
import time
import operator
import numbers
import pandas as pd


class Question:
    def __init__(self, column, value):
        self.column = column
        self.operator = operator
        self.value = value

    def ask_question(self):
        if is_numeric(self.value):
            print('is ' + str(self.column) + ' < ' + str(self.value) + '?')
        else:
            print('is ' + str(self.column) + ' equal to ' + str(self.value) + '?') 

    def answer_question(self, rows):
        for i, row in rows.iterrows():
            if is_numeric(self.value):
                print(row[self.column] < self.value)
            else:
                print(row[self.column] == self.value)

def get_all_questions(data):
    questions = []
    for col in data.columns:
        for val in data[col].unique():
            q = Question(col, val)
            #q.ask_question()
            questions.append(q)
    return questions


class DNode:
    def __init__(self, question=None):
        self.question = question
        self.child_true = None
        self.child_false = None

    #???
    def add_node(self, question):
        if self.child_true:
            self.child_true.add_node(question)
        if self.child_false:
            self.child_false.add_node(question)
        else:
            self.child_true = DNode(question)
            self.child_false = DNode(question)
            

def is_numeric(value):
    return isinstance(value, int)

#???
def info_gain(data, questions):
    ent = entropy(data, questions)

    info_gain = []
    for i in ent:
        for j in ent[i]:
            if j != 'total':
                info_gain.append((j, ent[i]['total']-ent[i][j]))
    info_gain = sorted(info_gain, key=lambda x: x[1])
    return info_gain  

#???
def entropy(data, questions):
    vals = {}
    entropy = {}
    for j in range(len(data.columns)):
        vals[data.columns[j]] = {}
        for i in range(len(data)):
            try:
                vals[data.columns[j]][data.iloc[i, j]] += 1
            except KeyError:
                vals[data.columns[j]][data.iloc[i, j]] = 1                           
    for j in range(len(data.columns)):
        e = 0
        for i in vals[data.columns[j]]:
            num = vals[data.columns[j]][i]
            e += (num/len(data))*math.log2(num/len(data))
        entropy[data.columns[j]] = {'total': -e}
    for i in questions:
        for j in vals.keys():
            e = 0
            if i.column == j:
                for k in vals[j]:
                    if i.value != k:
                        num = vals[j][k]
                        e += (num/len(data))*math.log2(num/len(data))
                e = e*((len(data)-vals[j][i.value])*.1)
                entropy[i.column][i.value] = -e                   
    return entropy

#???
def printTree(node, ind=1):
    if node.child_true:
        printTree(node.child_true, ind+1)
    if node.child_false:
        printTree(node.child_false, ind+1)
    else:
        print('\t'*ind + 'leaf')

if __name__ == "__main__":
    training_data = [
        ['Green', 3, 'Apple'],
        ['Yellow', 3, 'Apple'],
        ['Red', 1, 'Grape'],
        ['Red', 1, 'Grape'],
        ['Yellow', 3, 'Lemon']
    ]

    training_data = pd.DataFrame(training_data, columns=['Color', 'Diameter', 'Fruit'])
    columns = training_data.columns

    q1 = Question(columns[0], 'Green')
    #q1.ask_question()
    #q1.answer_question(training_data)

    q2 = Question(columns[1], 3)
    #q2.ask_question()
    #q2.answer_question(training_data)

    #???
    root = None
    questions = get_all_questions(training_data)
    ig = info_gain(training_data, questions)
    print(ig)
    for i in ig:
        for j in questions:
            if i[0] == j.value:
                if root:
                    root.add_node(j)
                    ig.remove(i)
                else:
                    root = DNode(j)
                    ig.remove(i)

    print('root')
    printTree(root)
