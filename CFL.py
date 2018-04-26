# -*- coding: utf-8 -*-

from enum import Enum
import time
from utils import Code, Element

Action = Enum('Action', ('Reduce', 'Shift', 'Acc'))


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

class ContextFreeLanguage:
    def __init__(self):
        self.rules = []
        self.elementsDict = {}
        self.elements = []
        self.starter = ""
        self.ender = ""
        self.first = {}
        self.empty = Element('"$"')

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
        L.producers.append(self.rules[-1])
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
        elif self.empty in firstSet:
            firstSet.remove(self.empty)
        return firstSet

    def initFirst(self):
        for ele in self.elements:
            if ele == self.empty:
                self.first[ele] = set({self.empty})
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
                    for r in B.producers:
                        for b in f:
                            if b == self.empty:
                                for e in slice:
                                    print(e, end=' ')
                                raise Exception("Found empty producers in closure calculation")
                            pos = 0
                            while pos < len(r.R) and r.R[pos] == self.empty:
                                pos += 1
                            if (r, pos, b) not in C:
                                newItem = True
                                D.add((r, pos, b))
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
        self.initialState = self.closure(frozenset({(self.rules[-1], 0, self.ender)}))
        self.C = {self.initialState:0}
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
        # printClan(self.C)

    def initActionGoto(self):
        self.goto = dict()
        self.action = dict()
        for clos in self.C:
            self.goto[clos] = dict()
            self.action[clos] = dict()
            for var in self.elements:
                if var.code == Code.Variable:
                    goto_tmp = self.go(clos, var)
                    if goto_tmp in self.C:
                        self.goto[clos][var] = goto_tmp
            for item in clos:
                if item[1] >= len(item[0].R):
                    self.action[clos][item[2]] = (Action.Reduce, item[0])
                else:
                    a = item[0].R[item[1]]
                    if a == self.empty:
                        raise Exception("Found empty in initActionGoto")
                    if a.code != Code.Variable:
                        self.action[clos][a] = (Action.Shift, self.go(clos, a))
                if self.rules[-1] == item[0] and item[1] == 1 and item[2] == Element('"#"'):
                    self.action[clos][Element('"#"')] = (Action.Acc, 0)
        # for clos in self.action:
        #     for c in self.action[clos]:
        #         print("action of")
        #         print(c)
        #         self.printClosure(clos)
        #         print(self.action[clos][c][0])
        #         print(self.action[clos][c][1])
        #         self.printClosure(self.action[clos][c][1])


    def init(self):
        t1 = time.time()
        self.initFirst()
        t2 = time.time()
        self.initClan()
        t3 = time.time()
        self.initActionGoto()
        t4 = time.time()
        print(t2-t1, t3-t2, t4-t3)

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

        stateStack = [self.initialState]
        symbolStack = [Element('"#"')]
        i = 0
        while i < len(s):
            print("---------------------------")
            w = s[i]
            print(w)
            S = stateStack[-1]
            for j in range(len(stateStack)):
                self.printClosure(stateStack[j])
                print(symbolStack[j])
            if w not in self.action[S]:
                return False
            elif self.action[S][w][0] == Action.Shift:
                symbolStack.append(w)
                stateStack.append(self.action[S][w][1])
                i += 1
            elif self.action[S][w][0] == Action.Reduce:
                rule = self.action[S][w][1]
                A = rule.L
                print("Reduce", rule)
                if rule.R[0] != self.empty:
                    stateStack = stateStack[:-len(rule.R)]
                    symbolStack = symbolStack[:-len(rule.R)]
                S = stateStack[-1]
                symbolStack.append(A)
                stateStack.append(self.goto[S][A])
            elif self.action[S][w][0] == Action.Acc:
                print("OK")
                return True
    def onlineParse(self, token, initFlag):
        if initFlag:
            self.stateStack = [self.initialState]
            self.symbolStack = [Element('"#"')]
        w = token.elem
        print("---------------------------")
        print(w)
        S = self.stateStack[-1]
        if w not in self.action[S]:
            print("Failed")
            raise Exception("Parse Failed")
            return False
        if self.action[S][w][0] == Action.Reduce:
            while w in self.action[S] and self.action[S][w][0] == Action.Reduce:
                rule = self.action[S][w][1]
                A = rule.L
                if rule.R[0] != self.empty:
                    self.stateStack = self.stateStack[:-len(rule.R)]
                    self.symbolStack = self.symbolStack[:-len(rule.R)]
                S = self.stateStack[-1]
                self.symbolStack.append(A)
                self.stateStack.append(self.goto[S][A])
                S = self.stateStack[-1]
                print("Reduction:", rule)
        S = self.stateStack[-1]
        if self.action[S][w][0] == Action.Shift:
            self.symbolStack.append(w)
            self.stateStack.append(self.action[S][w][1])
        # for i in range(len(self.stateStack)):
        #     self.printClosure(self.stateStack[i])
        #     print(self.symbolStack[i])
        if self.action[S][w][0] == Action.Acc:
            print("OK")
            return True


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
        print(cfl.parse(line + '"#"'))
