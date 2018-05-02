# -*- coding: utf-8 -*-

from scanner import Scanner
from CFL import ContextFreeLanguage
from semantic import Semantic
import pickle

if __name__ == "__main__":
    grammarFile = open("grammar.txt", "r")
    cfl = ContextFreeLanguage()

    while True:
        line = grammarFile.readline()
        if line == "":
            break
        [L,R] = line[:-1].split('-->')
        print("input", L, R)
        cfl.addRule(L, R)
    cfl.addStarter("[S_p]")
    cfl.addEnder('"#"')
    cfl.init()
    pickle.dump(cfl, open("cfl.dump", "wb"))


    testFile = open("test.cpp", "rb")
    scanner = Scanner(testFile)
    flag = True
    while True:
        token = scanner.scan()
        cfl.onlineParse(token, flag)
        flag = False
        if token.info == "":
            break
