# -*- coding: utf-8 -*-

from scanner import Scanner
from CFL import ContextFreeLanguage
from semantic import Semantic, TriAddr, SynInfo, SymbolTable
import sys
import pickle

def getCFL(fileName):
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
    return cfl


def outputAssembler(codes, table, output):
    output.write(".data\n")
    for globalVar in table:
        if type(table[globalVar]) == Symbol:
            print(".global " + globalVar + "\n")
            if table[globalVar].mold == "int":
                print("")
    for code3 in codes:
        if code3.op == "label":
            output.write(code3.result + ":" + "\n")
        elif code3.op == "goto":
            output.write("  goto " + code3.result + "\n")
        elif code3.op == "":
            output.write("  ")



if __name__ == "__main__":
    # cfl = getCFL()
    scanner = Scanner(open("test.cpp", "rb"))
    semantic = Semantic("cfl.dump")

    while True:
        token = scanner.scan()
        semantic.onlineAnalyze(token)
        if token.info == "":
            break

    codes = semantic.symbolStack[-1][1].code
    table = semantic.tableStack[-1]

    output = open("test.asm", "w")
    outputAssembler(codes, table, sys.stdout)
