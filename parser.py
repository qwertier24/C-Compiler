# -*- coding: utf-8 -*-

from enum import Enum

Code = Enum('Code', ('Variable', 'int', '*', '=', '#', 'e'))
Action = Enum('Action', ('Recuce', 'Shift', 'Acc'))

class Rule:
    def __init__(self, L, R):
        self.L = L
        self.R = R
        print("new Rule:", L, end=' --> [')
        for i in R:
            print(i, end=' ')
        print(']')
    def __str__(self):
        res = ""
        res += str(self.L) + " --> ["
        for i in self.R:
            res += str(i)
            res += ' '
        res += ']'
        return res

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
        return str(self.name)
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name

class ContextFreeLanguage:


    def __init__(self):
        self.rules = []
        self.elementsDict = {}
        self.elements = []
        self.starter = ""
        self.ender = ""
        self.first = {}
        self.empty = Element('"e"')

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
                L = self.addElement(strL[i:j+1])

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

    def getFirst(self, l):
        emptiable = True
        firstSet = set()
        for i in l:
            if not emptiable:
                break
            firstSet |= self.first[i]
            if self.empty not in self.first[i]:
                emptiable = False
        if emptiable:
            firstSet.add(self.empty)
        return firstSet

    def initFirst(self):
        for ele in self.elements:
            if ele == self.empty:
                self.first[ele] = set({empty})
            elif ele.code == Code.Variable:
                self.first[ele] = set()
            else:
                self.first[ele] = {ele}
        while True:
            newItem = False
            for r in self.rules:
                tmp = self.getFirst(r.R)
                if not self.first[r.L].issuperset(tmp):
                    self.first[r.L] |= tmp
                    newItem = True
            if not newItem:
                break
        # for ele in self.elements:
        #     print("First of ", ele, end=': ')
        #     for i in self.first[ele]:
        #         print(i, end = ' ')
        #     print()
    '''
    Item is a tuple:
    (A->x.By, a) := ((A->xBy), 1, a)
    '''

    def closure(self, I):
        C = set(I)
        while True:
            D = set()
            for c in C:
                if c[1] >= len(c[0].R) or c[0].R[c[1]].code != Code.Variable:
                    continue
                if c[1] < len(c[0].R) and c[0].R[c[1]].code == Code.Variable:
                    slice = c[0].R[c[1]+1:]
                    slice.append(c[2])
                    f = self.getFirst(slice)

                    B = c[0].R[c[1]]
                    for r in self.rules:
                        if r.L == B:
                            for b in f:
                                if (r, 0, b) not in C:
                                    newItem = True
                                    D.add((r, 0, b))
            if D == set():
                break
            else:
                C |= D
        return frozenset(C)


    def go(self, I, X):
        J = set()
        for c in I:
            if c[1] < len(c[0].R) and c[0].R[c[1]] == X:
                J.add((c[0], c[1]+1, c[2]))
        return self.closure(frozenset(J))


    def printClosure(self, C):
        #print(type(C))
        print("Closure of " + str(self.C[C]) + ":", end=" {\n")
        for c in C:
            print("(", c[0], c[1], c[2], end ='), \n')
        print("}")


    def initClan(self):
        def printClan(clan):
            for C in clan:
                print("Closure of " + str(clan[C]) + ":", end=" {\n")
                for c in C:
                    print("(", c[0], c[1], c[2], end ='), \n')
                print("}")
        self.C = {self.closure(frozenset({(self.rules[-1], 0, self.ender)})):0}
        while True:
            D = set()
            for I in self.C:
                for X in self.elements:
                    if X != self.empty:
                        cand = self.go(I, X)
                        if len(cand) != 0 and cand not in self.C:
                            D.add(cand)

            if len(D) == 0:
                break
            else:
                for d in D:
                    self.C[d] = len(self.C)
        printClan(self.C)

    def initActionGoto(self):
        pass

    def init(self):
        self.initFirst()
        self.initClan()
        self.initActionGoto()

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

    cfl.init()

    testFile = open("test_file.g", "r")
    while True:
        line = testFile.readline()[:-1]
        if line == "":
            break
        cfl.parse(line + '"#"')
