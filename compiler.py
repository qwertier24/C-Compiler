# -*- coding: utf-8 -*-

from scanner import Scanner
from CFL import ContextFreeLanguage
from semantic import Semantic, TriAddr, SynInfo, SymbolTable, Symbol
import sys
import pickle

def getCFL(fileName):
    grammarFile = open(fileName, "r")
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

def isnum(num):
    return type(num) == int or type(num) == float

def getVar(varName, table):
    if varName not in table:
        if ".." in table:
            return getVar(varName, table[".."])
        else:
            raise Exception("No definition of " + str(varName))
    else:
        return table[varName]

def getop(op):
    if op == "+":
        return "addl"
    elif op == "-":
        return "subl"
    elif op == '*':
        return "mull"
    elif op in "/%":
        return "divl"
    elif op == "==":
        return "jz"
    elif op == "<":
        return "ja"
    elif op == ">":
        return "jb"
    elif op == "<=":
        return "jae"
    elif op == ">=":
        return "jbe"
    elif op == '!=':
        return "jnz"

def getaddr(var, table, output):
    if type(var) == int or type(var) == float:
        return "$"+str(var)
    elif "[" in var:
        [name, pos] = var.split('[')
        if "(" in pos:
            pos = pos[:-1]
            output.write("  movl %ebp, %eax\n")
            output.write("  addl %d, %%eax\n"%(table[pos].addr))
            if name in table:
                return str(-table[name].addr) + "(%ebp, %eax, 4)"
            elif name in table[".."]:
                return str(table[".."][var].addr+4*pos) + "(%eds)"
        else:
            pos = int(pos[:-1])
            if name in table:
                return str(-table[name].addr+4*pos) + "(%ebp)"
            elif name in table[".."]:
                return str(table[".."][name].addr+4*pos) + "(%eds)"
    elif var in table:
        return str(-getVar(var, table).addr) + "(%ebp)"
    elif var in table[".."]:
        return var


def outputAssembler(codes, table, output):
    output.write(".code32\n")
    output.write(".section .data:\n")
    for varName in table:
        var = table[varName]
        if type(var) == Symbol:
            output.write("%s:\n"%(varName))
            if var.mold == "int":
                output.write("  .fill %d,%d,%d\n"%(var.width/4, 4, 0))
    output.write("\n")

    output.write(".section .code:\n")
    funcTable = 0
    for code3 in codes:
        print(code3, "---")
        if code3.op == "function":
            output.write(".globl %s\n"%(code3.result))
            output.write("  pushl %ebp\n  movl %esp, %ebp\n")
            funcTable = table[code3.result]
        elif code3.op == "endf":
            output.write("  movl %ebp, %esp\n  popl %ebp\n")
            output.write("  ret\n\n")
        elif code3.op in "+-*/%":
            var1 = getaddr(code3.arg1, funcTable, output)
            var2 = getaddr(code3.arg2, funcTable, output)
            res = getaddr(code3.result, funcTable, output)
            # if var1.mold == "int" and var2.mold == "int" and res.mold == "int":
            if code3.op in "+-":
                output.write("  movl %s, %s\n"%(var1, res))
                output.write("  %s %s, %s\n"%(getop(code3.op), var2, res))
            if code3.op in "*/%":
                output.write("  movl $0, %edx\n")
                output.write("  movl %s, %%eax\n"%(var1))
                output.write("  %s %s\n"%(getop(code3.op), var2))
                if code3.op in '*/':
                    output.write("  movl %%eax, %s\n"%(res))
                elif code3.op == '%':
                    output.write("  movl %%edx, %s\n"%(res))
        elif code3.op == "label":
            output.write(code3.result + ":" + "\n")
        elif code3.op == "goto":
            output.write("  jmp " + code3.result + "\n")
        elif code3.op[:4] == "goto":
            var1 = getaddr(code3.arg1, funcTable, output)
            var2 = getaddr(code3.arg2, funcTable, output)
            res = code3.result
            output.write("  cmpl %s, %s\n"%(var1, var2))
            output.write("  %s %s\n"%(getop(code3.op[4:]), res))
        elif code3.op == "=" or code3.op == ":=":
            var1 = getaddr(code3.arg1, funcTable, output)
            res = getaddr(code3.result, funcTable, output)
            output.write("  movl %s, %s\n"%(var1, res))
        elif code3.op in {"+=", "-="}:
            var1 = getaddr(code3.arg1, funcTable, output)
            res = getaddr(code3.result, funcTable, output)
            output.write("  addl %s, %s\n"%(var1, res))
        elif code3.op == "return":
            output.write("  movl %ebp, %esp\n  popl %ebp\n")
            if code3.arg1 != None:
                var1 = getaddr(code3.arg1, funcTable, output)
                output.write("  movl %s, %%eax\n"%(var1))
            output.write("  ret\n")


if __name__ == "__main__":
    # cfl = getCFL("grammar.txt")
    scanner = Scanner(open("test.cpp", "rb"))
    semantic = Semantic("cfl.dump")

    while True:
        token = scanner.scan()
        print(token.elem, token.info)
        semantic.onlineAnalyze(token)
        if token.info == "":
            break

    codes = semantic.symbolStack[-1][1].code
    table = semantic.tableStack[-1]

    output = open("test.asm", "w")
    outputAssembler(codes, table, open("test.s", "w"))
