# -*- coding: utf-8 -*-
from utils import Code, Element, Token
from scanner import Scanner
from CFL import ContextFreeLanguage, Action
import pickle

class Symbol:
    def __init__(self, mold, addr, width, dim=[]):
        self.mold = "int"
        self.addr = addr
        self.width = width
        self.dim = dim

SymbolTable = dict

class TriAddr:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    def __str__(self):
        return "%10s|%10s|%10s|%10s"%(self.op, str(self.arg1), str(self.arg2), str(self.result))

class SynInfo:
    def __init__(self, name="", mold=None):
        self.code = []
        self.addr = 0
        self.mold = None
        self.width = 0
        self.name = name

class Semantic:
    def __init__(self, cfl_file_name):
        self.cfl = pickle.load(open(cfl_file_name, "rb"))
        self.stateStack = [self.cfl.initialState]
        self.symbolStack = [Element('"#"')]
        self.tableStack = [SymbolTable()]
        self.offsetStack = [0]
        self.tempCount = 0
        self.labelCount = 0
    def newTemp(self, mold, width):
        varName = "(" + str(self.tempCount) + ")"
        self.enterSymbol(varName, mold, width)
        self.tempCount += 1
        return varName
    def printSymbolTable(self, table):
        for item in table:
            if type(table[item]) == Symbol:
                print(item, table[item].mold, table[item].addr, table[item].width)
            else:
                print(item)
        for item in table:
            if type(table[item]) == SymbolTable:
                print("Table", item, ":")
                self.printSymbolTable(table[item])
    def enterProc(self, name, newtable):
        table = self.tableStack[-1]
        if name in table:
            raise Exception("Redefinition of " + name)
        table[name] = newtable
    def enterSymbol(self, name, mold, width, dim=[]):
        table = self.tableStack[-1]
        if name in table:
            raise Exception("Redefinition of " + name)
        table[name] = Symbol(mold, self.offsetStack[-1], width, dim)
        self.offsetStack[-1] += width
    def addTable(self):
        self.tableStack.append(self.tableStack[-1].copy())
        self.offsetStack.append(0)
    def f0(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code + childInfo[1].code
        print("---")
        for c in rootInfo.code:
            print(c)
        print("---")
        self.printSymbolTable(self.tableStack[-1])
    def f1(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code + childInfo[1].code
    def f2(self, rootInfo, childInfo):
        pass
    def f3(self, rootInfo, childInfo):
        t = self.tableStack[-1]
        del self.tableStack[-1]
        del self.offsetStack[-1]
        self.enterProc(childInfo[1].name, t)
        rootInfo.code = [TriAddr("Function", childInfo[1].name, None, None)] + childInfo[6].code
    def f4(self, rootInfo, childInfo):
        rootInfo.mold = "int"
        rootInfo.width = 4
    def f10(self, rootInfo, childInfo):
        rootInfo.mold = "void"
        rootInfo.width = 0
    def f12(self, rootInfo, childInfo):
        table = self.tableStack[-1]
        self.enterSymbol(childInfo[1].name, childInfo[0].mold, childInfo[0].width)
    def f13(self, rootInfo, childInfo):
        pass
    def f14(self, rootInfo, childInfo):
        self.enterSymbol(childInfo[2].name, childInfo[1].mold, childInfo[1].width)
    def f15(self, rootInfo, childInfo):
        pass
    def f17(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code[:]
    def f18(self, rootInfo, childInfo):
        rootInfo.code = childInfo[1].code + childInfo[2].code
    def f19(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code + childInfo[1].code
    def f20(self, rootInfo, childInfo):
        pass
    def f21(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code[:]
    def f22(self, rootInfo, childInfo):
        rootInfo.code = childInfo[1].code[:]
        rootInfo.name = childInfo[1].name
        rootInfo.width = 1
    def f23(self, rootInfo, childInfo):
        rootInfo.width = childInfo[1].name # The name here is actually a number
        rootInfo.mold = "array"
        rootInfo.name = ""
    def f24(self, rootInfo, childInfo):
        rootInfo.width = 1
        rootInfo.name = ""
    def f25(self, rootInfo, childInfo):
        rootInfo.name = childInfo[1].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        if childInfo[2].name != "":
            self.enterSymbol(rootInfo.name, rootInfo.mold, rootInfo.width)
            rootInfo.code += childInfo[2].code
            rootInfo.code += [TriAddr(":=", childInfo[2].name, None, childInfo[1].name)]
        elif childInfo[2].mold == "array":
            self.enterSymbol(rootInfo.name, rootInfo.mold, max(1, rootInfo.width*childInfo[2].width), [childInfo[2].width])
        else:
            self.enterSymbol(rootInfo.name, rootInfo.mold, rootInfo.width)
    def f26(self, rootInfo, childInfo):
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.name = childInfo[2].name
        rootInfo.code += childInfo[0].code
        if childInfo[3].name != "":
            self.enterSymbol(rootInfo.name, rootInfo.mold, rootInfo.width)
            rootInfo.code += childInfo[3].code
            rootInfo.code += [TriAddr(":=", childInfo[3].name, None, rootInfo.name)]
        elif childInfo[3].mold == "array":
            self.enterSymbol(rootInfo.name, rootInfo.mold, max(1, rootInfo.width*childInfo[3].width), [childInfo[3].width])
        else:
            self.enterSymbol(rootInfo.name, rootInfo.mold, rootInfo.width)
    def f27(self, rootInfo, childInfo):
        # [stmts] --> [stmt] [stmts]
        rootInfo.code += childInfo[0].code + childInfo[1].code
    def f28(self, rootInfo, childInfo):
        pass
    def f29(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
    def f30(self, rootInfo, childInfo):
        pass
    def f32(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
    def f33(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
    def f36(self, rootInfo, childInfo):
        pass
    def f40(self, rootInfo, childInfo):
        # [branch_stmt] --> "if" "(" [logical_expression] ")" [block_stmt] [result]
        rootInfo.code += childInfo[2].code
        rootInfo.code.append(TriAddr("goto>", childInfo[2].name, 0, "L"+str(self.labelCount)))
        rootInfo.code += childInfo[4].code
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount)))
        self.labelCount += 1
        rootInfo.code += childInfo[5].code
    def f42(self, rootInfo, childInfo):
        # [result] --> "$"
        pass
    def f44(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = 1
        rootInfo.mold = "char"
    def f45(self, rootInfo, childInfo):
        # [bool_expression] --> [bool_expression] [lop] [expression]
        rootInfo.code += childInfo[0].code + childInfo[2].code
        rootInfo.name = self.newTemp("char", 1)
        rootInfo.code.append(TriAddr(childInfo[1].name, childInfo[0].name, childInfo[2].name, rootInfo.name))
    def f46(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = 1
        rootInfo.mold = "char"
    def f47(self, rootInfo, childInfo):
        rootInfo.name = "&&"
    def f54(self, rootInfo, childInfo):
        # [block_stmt] --> "{" [stmts] "}"
        rootInfo.code += childInfo[1].code
    def f55(self, rootInfo, childInfo):
        pass
    def f57(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
    def f58(self, rootInfo, childInfo):
        # [expression] --> [value] [compare_op] [value]
        rootInfo.code += childInfo[0].code + childInfo[2].code
        rootInfo.name = self.newTemp("char", 1)
        rootInfo.code.append(TriAddr("goto"+childInfo[1].name, childInfo[0].name, childInfo[2].name, "L"+str(self.labelCount)))
        rootInfo.code.append(TriAddr("=", 0, None, rootInfo.name))
        rootInfo.code.append(TriAddr("goto", 0, None, "L"+str(self.labelCount+1)))
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount)))
        rootInfo.code.append(TriAddr("=", 1, None, rootInfo.name))
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount+1)))
        self.labelCount += 2
    def f59(self, rootInfo, childInfo):
        # [expression] --> [value] [equal_op] [value]
        rootInfo.code += childInfo[0].code + childInfo[2].code
        rootInfo.code.append(TriAddr(childInfo[1].name, childInfo[0].name, childInfo[2].name, childInfo[0].name))
    def f61(self, rootInfo, childInfo):
        # [compare_op] --> ">"
        rootInfo.name = ">"
    def f63(self, rootInfo, childInfo):
        rootInfo.name = "<"
    def f67(self, rootInfo, childInfo):
        rootInfo.name = "="
    def f73(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
    def f77(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
    def f83(self, rootInfo, childInfo):
        # [factor] --> "IDN" [call_func]
        rootInfo.name = childInfo[0].name
        symbol = self.tableStack[-1][rootInfo.name]
        rootInfo.mold = symbol.mold
        rootInfo.width = symbol.width
        rootInfo.addr = symbol.addr
    def f84(self, rootInfo, childInfo):
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.code += childInfo[0].code
    def f85(self, rootInfo, childInfo):
        pass
    def f86(self, rootInfo, childInfo):
        pass
    def f87(self, rootInfo, childInfo):
        pass
    def f88(self, rootInfo, childInfo):
        pass
    def f89(self, rootInfo, childInfo):
        pass
    def f90(self, rootInfo, childInfo):
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.code += childInfo[0].code
    def f94(self, rootInfo, childInfo):
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.code += childInfo[0].code
    def f97(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code
    def f98(self, rootInfo, childInfo):
        self.addTable()
    def onlineAnalyze(self, token):
        w = token.elem
        print("---------------------------")
        print(w)
        S = self.stateStack[-1]
        if w not in self.cfl.action[S]:
            print("Failed")
            raise Exception("Parse Failed")
            return False
        if self.cfl.action[S][w][0] == Action.Reduce:
            while w in self.cfl.action[S] and self.cfl.action[S][w][0] == Action.Reduce:
                rule = self.cfl.action[S][w][1]
                A = rule.L
                synInfo = SynInfo()
                if len(self.stateStack) != len(self.symbolStack):
                    print(len(self.stateStack), len(self.symbolStack))
                    raise Exception("Not equal")
                for i in range(len(rule.R)+1):
                    if i in rule.prod:
                        f = getattr(self, rule.prod[i][:-2])
                        f(synInfo, [x[1] for x in ([] if rule.R[0] == self.cfl.empty else self.symbolStack[-len(rule.R):])])

                print("---")
                print(synInfo.name, synInfo.mold)
                for c in synInfo.code:
                    print(c)
                print("---")
                if rule.R[0] != self.cfl.empty:
                    if len(self.symbolStack) < len(rule.R):
                        raise Exception("Fewer symbols than needed")
                    self.stateStack = self.stateStack[:-len(rule.R)]
                    self.symbolStack = self.symbolStack[:-len(rule.R)]
                S = self.stateStack[-1]
                try :
                    self.symbolStack.append((A, synInfo))
                    self.stateStack.append(self.cfl.goto[S][A])
                except:
                    self.cfl.printClosure(S)
                    raise Exception(A)
                S = self.stateStack[-1]
                print("Reduction:", rule)
        S = self.stateStack[-1]
        if self.cfl.action[S][w][0] == Action.Shift:
            self.symbolStack.append((w, SynInfo(token.info, token.elem.name[1:-1])))
            self.stateStack.append(self.cfl.action[S][w][1])
        # for i in range(len(self.stateStack)):
        #     self.printClosure(self.stateStack[i])
        #     print(self.symbolStack[i])
        if self.cfl.action[S][w][0] == Action.Acc:
            print("OK")
            return True

if __name__ == "__main__":
    scanner = Scanner(open("test.cpp", "rb"))
    semantic = Semantic("cfl.dump")
    while True:
        token = scanner.scan()
        print(token.elem, token.info)
        semantic.onlineAnalyze(token)
        if token.info == "":
            break
