# -*- coding: utf-8 -*-

from enum import Enum

Code = Enum('Code', ('Variable', 'int', '*', "=", '#'))

class Rule:
    def __init__(self, L, R):
        self.L = L
        self.R = R
        print("new Rule:", L, end=' --> [')
        for i in R:
            print(i, end=' ')
        print(']')

class Element:
    def __init__(self, name):
        self.name = name
        if name[0] == '[':
            self.code = Code.Variable
        elif name[0] == '"':
            for code in Code:
                if code.name == name[1:-1]:
                    self.code = code
    def __str__(self):
        return str((self.code, self.name))
    def __hash__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name

class ContextFreeLanguage:

    def __init__(self):
        self.rules = []
        self.elementsDict = {}
        self.elements = []
        self.starter = ""
        self.ender = ""

    def addElement(self, eleStr):
        if eleStr not in self.elementsDict:
            self.elements.append(Element(eleStr))
            self.elementsDict[eleStr] = self.elements[-1]
        return self.elementsDict[eleStr]

    def addRule(self, strL, strR):
        L = 0
        for i in range(len(strL)):
            if strL[i] == '[':
                j = i + 1
                while strL[j] != ']':
                    j += 1
                L = strL[i:j+1]

        R = []
        i = 0
        while i < len(strR):
            if strR[i] == '[':
                j = i + 1
                while strR[j] != ']':
                    j += 1
                R.append(self.addElement(strR[i:j+1]))
                i = j+1
            elif strR[i] == '"':
                j = i + 1
                while strR[j] != '"':
                    j += 1
                R.append(self.addElement(strR[i:j+1]))
                i = j+1
            else:
                i += 1
        self.rules.append(Rule(L, R))
        return self.rules[-1]
    def addStarter(self, strL):
        self.starter = self.addElement(strL)
        print(self.starter)
        return self.starter
    def addEnder(self, strL):
        self.ender = self.addElement(strL)
        print(self.ender)
        return self.ender

    '''
    Item is a tuple:
    (A->x.By, a) := ((A->xBy), 1, a)
    '''

    def closure(self, I):
        C = set(I)
        newItem = True
        while newItem:
            flag = False
            for c in C:
                if c[0].R[c[1]].code != Code.Variable:
                    continue
                f = first(c[0].R[c[1]+1:].append(c[2]))
                for r in rules:
                    if r.L == c:
                        for b in f:
                            if (r, 0, b) not in C:
                                flag = True
                                C.add((r, 0, b))
            newItem = flag
        return frozenset(C)

    def init(self):
        pass

    def parse(self, sentence):
        i = 0
        s = []
        while i < len(sentence):
            if sentence[i] == '[':
                j = i + 1
                while sentence[j] != '[':
                    j += 1
                s.append(self.elementsDict[sentence[i:j+1]])
                i = j + 1
            elif sentence[i] == '"':
                j = i + 1
                while sentence[j] != '"':
                    j += 1
                s.append(self.elementsDict[sentence[i:j+1]])
                i = j + 1
            else:
                i += 1
        for w in s:
            print(w)


if __name__ == "__main__" :
    grammarFile = open("test_grammar.g", "r")
    cfl = ContextFreeLanguage()

    while True:
        line = grammarFile.readline()
        if line == "":
            break
        [L,R] = line[:-1].split('-->')
        print("input", L, R)
        cfl.addRule(L, R)
    cfl.addRule("[S_p]", "[S]")
    cfl.addStarter("[S_p]")
    cfl.addEnder('"#"')

    testFile = open("test_file.g", "r")
    while True:
        line = testFile.readline()[:-1]
        if line == "":
            break
        cfl.parse(line + '"#"')
