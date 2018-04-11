# -*- coding: utf-8 -*-

from enum import Enum

Code = Enum('Code', ('Variable', '', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

class Variable:
    def __init__(self):
        pass

class ProductionRule:
    class Element:
        def __init__(self, name):
            self.name = 0
            if name[0] == '[':
                self.code = Code.Variable
            elif name[0] == '"':
                for code in Code:
                    if code.name == name[1:-1]:
                        self.code = code
    def __init__(self, strL, strR):
        for i in range(len(strL)):
            if strL[i] == '[':
                j = i + 1
                while strR[j] != ']':
                    j += 1
                self.L = Element(strL[i+1:j], VAR)

        self.R = []
        i = 0
        while i < len(strR):
            if strL[i] == '[':
                j = i + 1
                while strR[j] != ']':
                    j += 1
                self.R.append(Element(strR[i:j+1]))
                i = j+1
            elif strR[i] == '(':
                j = i + 1
                while strR[j] != ')':
                    j += 1
                self.R.append(Element(strR[i:j+1]))
                i = j+1
            elif strR[i] == '"':
                j = i + 1
                while strR[j] != '"':
                    j += 1
                self.R.append(Element(strR[i:j+1]))
                i = j+1
            else:
                i += 1


class Parser:
    def __init__(self):
        self.var = dict()
        self.dest = dict()
    def addVar(self, newVar):
        var.add(newVar)
        if var.get(newVar) == None:
            var[newVar] = Variable()
    def addDest(self, newDest):
        dest.add(newDest)
    def addStatement(self, nweProd):
        prod.add(newProd)

if __name__ == "__main__" :
    f = open("test_grammar.g", "r")
    while True:
        line = f.readline()
        if line == "\n" or line == "":
            break
        [L,R] = line[:-1].split('-->')
        print(L, R)
