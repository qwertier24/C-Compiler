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
        self.dim = dim[:]

SymbolTable = dict

class TriAddr:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    def __str__(self):
        if True:
            return "%10s|%10s|%10s|%10s"%(self.op, str(self.arg1), str(self.arg2), str(self.result))
        else:
            if self.op == "label":
                return self.result + ":"
            elif self.op == "goto":
                return "  " + "goto " + self.result
            elif self.op[:4] == "goto":
                return "  " + "if " + str(self.arg1) + self.op[4:] + str(self.arg2) + " goto " + self.result
            elif self.op == "function":
                return "function " + self.result
            elif self.op == "param":
                return "  param " + str(self.arg1)
            elif self.op == "call":
                return "  call " + str(self.arg1) + " " + str(self.arg2)
            elif self.op == "return":
                return "  return " + str(self.arg1)
            elif self.op[0] == '=' or (len(self.op) > 1 and self.op[1] == '='):
                return "  " + str(self.result) + self.op + str(self.arg1)
            else:
                return "  " + str(self.result) + " = " + str(self.arg1) + self.op + str(self.arg2)


class SynInfo:
    def __init__(self, name="", mold=None):
        self.code = []
        self.addr = 0
        self.mold = None
        self.width = 0
        self.name = name
        self.dim = []

class Semantic:
    def __init__(self, cfl_file_name):
        self.cfl = pickle.load(open(cfl_file_name, "rb"))
        self.stateStack = [self.cfl.initialState]
        self.symbolStack = [(SynInfo(), Element('"#"'))]
        self.tableStack = [SymbolTable()]
        self.offsetStack = [0]
        self.tempCount = 0
        self.labelCount = 0
    def isnum(self, elem):
        return type(elem) == int or type(elem) == float
    def newTemp(self, mold, width):
        varName = "(" + str(self.tempCount) + ")"
        self.enterSymbol(varName, mold, width)
        self.tempCount += 1
        return varName
    def getVar(self, varName, table=None):
        if table == None:
            table = self.tableStack[-1]
        if varName not in table:
            if ".." in table:
                return self.getVar(varName, table[".."])
            else:
                raise Exception("No definition of " + str(varName))
        else:
            return table[varName]
    def printSymbolTable(self, table):
        for item in table:
            if item == "..":
                continue
            if type(table[item]) == Symbol:
                print(item, table[item].mold, table[item].addr, table[item].width)
            else:
                print(item)
        for item in table:
            if item == "..":
                continue
            if type(table[item]) == SymbolTable:
                print("Table", item, ":")
                self.printSymbolTable(table[item])
    def enterProc(self, name, newtable):
        table = self.tableStack[-1]
        if name in table:
            raise Exception("Redefinition of " + name)
        table[name] = newtable
    def calc(self, op, arg1, arg2):
        if op == "+":
            return arg1 + arg2
        elif op == "-":
            return arg1 - arg2
        elif op == "*":
            return arg1 * arg2
        elif op == '/':
            if type(arg1) == float or type(arg2) == float:
                return arg1 / arg2
            else:
                return arg1 // arg2
        elif op == '%':
            if type(arg1) == float or type(arg2) == float:
                raise Exception("One of the operators of % is not integer!")
            else:
                return arg1 % arg2
    def enterSymbol(self, name, mold, width, dim=[]):
        table = self.tableStack[-1]
        if name in table:
            raise Exception("Redefinition of " + name)
        if width > 0:
            if self.offsetStack[-1] < 0:
                self.offsetStack[-1] = 4
            table[name] = Symbol(mold, self.offsetStack[-1], width, dim)
        else:
            table[name] = Symbol(mold, self.offsetStack[-1], -width, dim)
        self.offsetStack[-1] += width
    def addTable(self):
        self.tableStack.append({"..": self.tableStack[-1]})
        self.offsetStack.append(-8)
    def f0(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code + childInfo[1].code + childInfo[2].code
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
        rootInfo.code = [TriAddr("function", None, None, childInfo[1].name)] + childInfo[6].code + [TriAddr("endf", None, None, childInfo[1].name)]
    def f4(self, rootInfo, childInfo):
        rootInfo.mold = "int"
        rootInfo.width = 4
    def f10(self, rootInfo, childInfo):
        # [type] --> "void" {f10()}
        rootInfo.mold = "void"
        rootInfo.width = 0
    def f12(self, rootInfo, childInfo):
        # [args] --> "$" {f12()}
        pass
        # table = self.tableStack[-1]
        # self.enterSymbol(childInfo[1].name, childInfo[0].mold, childInfo[0].width)
    def f13(self, rootInfo, childInfo):
        # [args] --> [arg] {f13()}
        rootInfo.code += childInfo[0].code
        pass
    def f14(self, rootInfo, childInfo):
        # [arg] --> [type] "IDN" [arg] {f14()}
        self.enterSymbol(childInfo[1].name, childInfo[0].mold, -childInfo[0].width)
        pass
        # self.enterSymbol(childInfo[2].name, childInfo[1].mold, childInfo[1].width)
    def f15(self, rootInfo, childInfo):
        # [arg] --> [arg] "," [type] "IDN" {f15()}
        self.enterSymbol(childInfo[3].name, childInfo[2].mold, -childInfo[2].width)
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
        # [arr_init] --> [arr_init] "[" "INT10" "]"
        rootInfo.width = childInfo[0].width * childInfo[2].name # The name here is actually a number
        rootInfo.mold = "array"
        rootInfo.dim += childInfo[0].dim
        rootInfo.dim.append(childInfo[2].name)
        rootInfo.name = ""
    def f24(self, rootInfo, childInfo):
        # [arr_init] --> "$"
        rootInfo.width = 1
        rootInfo.dim = []
        rootInfo.name = ""
    def f25(self, rootInfo, childInfo):
        # [vars] --> [type] "IDN" [init]
        rootInfo.name = childInfo[1].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        if childInfo[2].name != "":
            self.enterSymbol(rootInfo.name, rootInfo.mold, rootInfo.width)
            rootInfo.code += childInfo[2].code
            rootInfo.code += [TriAddr(":=", childInfo[2].name, None, childInfo[1].name)]
        elif childInfo[2].mold == "array":
            self.enterSymbol(rootInfo.name, rootInfo.mold, max(rootInfo.width, rootInfo.width*childInfo[2].width), childInfo[2].dim)
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
        rootInfo.code += childInfo[0].code
    def f31(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
    def f32(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
    def f33(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
    def f36(self, rootInfo, childInfo):
        # [jump_stmt] --> "return" [isnull_expr] ";"
        rootInfo.code += childInfo[0].code
        rootInfo.code.append(TriAddr("return", childInfo[1].name, None, None))
    def f37(self, rootInfo, childInfo):
        # [iteration_stmt] --> "while" "(" [logical_expression2] ")" [block_stmt4]
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount)))
        rootInfo.code += childInfo[2].code
        rootInfo.code.append(TriAddr("goto==", childInfo[2].name, 0, "L"+str(self.labelCount+1)))
        rootInfo.code += childInfo[4].code
        rootInfo.code.append(TriAddr("goto", None, None, "L"+str(self.labelCount)))
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount+1)))
        self.labelCount += 2
    def f38(self, rootInfo, childInfo):
        # [iteration_stmt] --> "for" "(" [isnull_expr2] ";" [isnull_expr4] ";" [isnull_expr6] ")" [block_stmt8]
        rootInfo.code += childInfo[2].code
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount)))
        if childInfo[4].name != "":
            # empty
            rootInfo.code += childInfo[4].code
            rootInfo.code.append(TriAddr("goto==", 0, childInfo[4].name, "L"+str(self.labelCount+1)))
        rootInfo.code += childInfo[8].code
        rootInfo.code += childInfo[6].code
        rootInfo.code.append(TriAddr("goto", None, None, "L"+str(self.labelCount)))
        rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount+1)))
        self.labelCount += 2

    def f40(self, rootInfo, childInfo):
        # [branch_stmt] --> "if" "(" [logical_expression] ")" [block_stmt] [result]
        rootInfo.code += childInfo[2].code
        rootInfo.code.append(TriAddr("goto==", childInfo[2].name, 0, "L"+str(self.labelCount)))
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
        rootInfo.width = 4
        rootInfo.mold = "char"
    def f45(self, rootInfo, childInfo):
        # [bool_expression] --> [bool_expression] [lop] [expression]
        if childInfo[1].name == "&&":
            rootInfo.code += childInfo[0].code
            rootInfo.code.append(TriAddr("goto==", childInfo[0].name, 0, "L"+str(self.labelCount)))
            rootInfo.code += childInfo[2].code
            rootInfo.code.append(TriAddr("goto==", childInfo[2].name, 0, "L"+str(self.labelCount)))
            rootInfo.name = self.newTemp("char", 4)
            rootInfo.code.append(TriAddr("=", 1, None, rootInfo.name))
            rootInfo.code.append(TriAddr("goto", None, None, "L" + str(self.labelCount+1)))
            rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount)))
            rootInfo.code.append(TriAddr("=", 0, None, rootInfo.name))
            rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount+1)))
        else:
            rootInfo.code += childInfo[0].code
            rootInfo.code.append(TriAddr("goto>", childInfo[0].name, 0, "L"+str(self.labelCount)))
            rootInfo.code += childInfo[2].code
            rootInfo.code.append(TriAddr("goto>", childInfo[2].name, 0, "L"+str(self.labelCount)))
            rootInfo.name = self.newTemp("char", 4)
            rootInfo.code.append(TriAddr("=", 0, None, rootInfo.name))
            rootInfo.code.append(TriAddr("goto", None, None, "L" + str(self.labelCount+1)))
            rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount)))
            rootInfo.code.append(TriAddr("=", 1, None, rootInfo.name))
            rootInfo.code.append(TriAddr("label", None, None, "L"+str(self.labelCount+1)))
        self.labelCount += 2
    def f46(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = 4
        rootInfo.mold = "char"
    def f47(self, rootInfo, childInfo):
        rootInfo.name = "&&"
    def f54(self, rootInfo, childInfo):
        # [block_stmt] --> "{" [stmts] "}"
        rootInfo.code += childInfo[1].code
    def f55(self, rootInfo, childInfo):
        # [isnull_expr] --> [expression]
        rootInfo.name = childInfo[0].name
        rootInfo.code += childInfo[0].code
    def f56(self, rootInfo, childInfo):
        # [isnull_expr] --> "$"
        rootInfo.name = ""
    def f57(self, rootInfo, childInfo):
        # [expression] --> [value]
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
    def f58(self, rootInfo, childInfo):
        # [expression] --> [value] [compare_op] [value]
        rootInfo.code += childInfo[0].code + childInfo[2].code
        rootInfo.name = self.newTemp("char", 4)
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
        rootInfo.code.append(TriAddr(childInfo[1].name, childInfo[2].name, None, childInfo[0].name))
    def f61(self, rootInfo, childInfo):
        # [compare_op] --> ">"
        rootInfo.name = ">"
    def f63(self, rootInfo, childInfo):
        rootInfo.name = "<"
    def f67(self, rootInfo, childInfo):
        rootInfo.name = "="
    def f68(self, rootInfo, childInfo):
        rootInfo.name = "+="
    def f73(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
    def f74(self, rootInfo, childInfo):
        # [value] --> [value] "+" [item]
        if type(childInfo[0].name) == int and type(childInfo[2].name) == int:
            rootInfo.name = self.calc("+", childInfo[0].name, childInfo[2].name)
            rootInfo.mold = "int" if type(rootInfo.name) == int else "float"
            rootInfo.width = 4
        else:
            rootInfo.code += childInfo[0].code
            rootInfo.code += childInfo[2].code
            rootInfo.width = childInfo[0].width
            rootInfo.mold = childInfo[0].mold
            rootInfo.name = self.newTemp(rootInfo.mold, rootInfo.width)
            rootInfo.code.append(TriAddr("+", childInfo[0].name, childInfo[2].name, rootInfo.name))
    def f75(self, rootInfo, childInfo):
        # [value] --> [value] "-" [item]
        if isnum(childInfo[0].name) and isnum(childInfo[2].name):
            rootInfo.name = self.calc("-", childInfo[0].name, childInfo[2].name)
            rootInfo.mold = "int" if type(rootInfo.name) == int else "float"
            rootInfo.width = 4
        else:
            rootInfo.code += childInfo[0].code
            rootInfo.code += childInfo[2].code
            rootInfo.width = childInfo[0].width
            rootInfo.mold = childInfo[0].mold
            rootInfo.name = self.newTemp(rootInfo.mold, rootInfo.width)
            rootInfo.code.append(TriAddr("+", childInfo[0].name, childInfo[2].name, rootInfo.name))
    def f77(self, rootInfo, childInfo):
        rootInfo.code += childInfo[0].code
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
    def f78(self, rootInfo, childInfo):
        # [item] --> [item] "*" [factor]
        if self.isnum(childInfo[0].name) and self.isnum(childInfo[2].name):
            rootInfo.name = self.calc("*", childInfo[0].name, childInfo[2].name)
            rootInfo.mold = "int" if type(rootInfo.name) == int else "float"
            rootInfo.width = 4
        else:
            rootInfo.code += childInfo[0].code
            rootInfo.code += childInfo[2].code
            rootInfo.mold = childInfo[0].mold
            rootInfo.width = childInfo[0].width
            rootInfo.name = self.newTemp(rootInfo.mold, rootInfo.width)
            rootInfo.code.append(TriAddr("*", childInfo[0].name, childInfo[2].name, rootInfo.name))
    def f79(self, rootInfo, childInfo):
        # [item] --> [item] "/" [factor]
        if self.isnum(childInfo[0].name) and self.isnum(childInfo[2].name):
            rootInfo.name = self.calc("/", childInfo[0].name, childInfo[2].name)
            rootInfo.mold = "int" if type(rootInfo.name) == int else "float"
            rootInfo.width = 4
        else:
            rootInfo.code += childInfo[0].code
            rootInfo.code += childInfo[2].code
            rootInfo.mold = childInfo[0].mold
            rootInfo.width = childInfo[0].width
            rootInfo.name = self.newTemp(rootInfo.mold, rootInfo.width)
            rootInfo.code.append(TriAddr("/", childInfo[0].name, childInfo[2].name, rootInfo.name))
    def f80(self, rootInfo, childInfo):
        # [item] --> [item] "%" [factor]
        if self.isnum(childInfo[0].name) and self.isnum(childInfo[2].name):
            rootInfo.name = self.calc("%", childInfo[0].name, childInfo[2].name)
            rootInfo.mold = "int" if type(rootInfo.name) == int else "float"
            rootInfo.width = 4
        else:
            rootInfo.code += childInfo[0].code
            rootInfo.code += childInfo[2].code
            rootInfo.mold = childInfo[0].mold
            rootInfo.width = childInfo[0].width
            rootInfo.name = self.newTemp(rootInfo.mold, rootInfo.width)
            rootInfo.code.append(TriAddr("%", childInfo[0].name, childInfo[2].name, rootInfo.name))
    def f81(self, rootInfo, childInfo):
        # [not_null_es] --> [expression]
        rootInfo.code += childInfo[0].code
        rootInfo.code.append(TriAddr("param", childInfo[0].name, None, None))
        rootInfo.width = 1
    def f82(self, rootInfo, childInfo):
        # [factor] --> "(" [value] ")"
        rootInfo.code += childInfo[1].code
        rootInfo.width = childInfo[1].width
        rootInfo.mold = childInfo[1].mold
        rootInfo.name = childInfo[1].name
    def f83(self, rootInfo, childInfo):
        # [factor] --> "IDN" [call_func]
        if childInfo[1].name == "call":
            rootInfo.code += childInfo[1].code
            rootInfo.code.append(TriAddr("call", childInfo[0].name, childInfo[1].width, None))
        else:
            rootInfo.name = childInfo[0].name
            symbol = self.getVar(rootInfo.name)
            rootInfo.mold = symbol.mold
            rootInfo.width = symbol.width
    def f84(self, rootInfo, childInfo):
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.code += childInfo[0].code
    def f85(self, rootInfo, childInfo):
        # [call_func] --> "(" [es] ")"
        rootInfo.code += childInfo[1].code
        rootInfo.width = childInfo[1].width
        rootInfo.name = "call"
        pass
    def f86(self, rootInfo, childInfo):
        pass
    def f87(self, rootInfo, childInfo):
        # [es] --> [not_null_es]
        rootInfo.width = childInfo[0].width
        rootInfo.code += childInfo[0].code
    def f88(self, rootInfo, childInfo):
        # [not_null_es] --> [not_null_es] "," [expression]
        rootInfo.code += childInfo[0].code
        rootInfo.width += childInfo[0].width
        rootInfo.code += childInfo[2].code
        rootInfo.code.append(TriAddr("param", childInfo[2].name, None, None))
        rootInfo.width += 1
    def f89(self, rootInfo, childInfo):
        rootInfo.width = 0
    def f90(self, rootInfo, childInfo):
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.code += childInfo[0].code
    def f91(self, rootInfo, childInfo):
        # [const] --> "FLOAT" {f91()}
        rootInfo.name = childInfo[0].name
        rootInfo.width = 4
        rootInfo.mold = "float"
        rootInfo.code += childInfo[0].code
    def f94(self, rootInfo, childInfo):
        rootInfo.name = childInfo[0].name
        rootInfo.width = 4
        rootInfo.mold = "int"
        rootInfo.code += childInfo[0].code
    def f97(self, rootInfo, childInfo):
        rootInfo.code = childInfo[0].code
    def f98(self, rootInfo, childInfo):
        self.addTable()
    def f99(self, rootInfo, childInfo):
        # [factor] --> [arr_find]
        rootInfo.code += childInfo[0].code
        rootInfo.mold = "array"
        rootInfo.addr = childInfo[0].addr
        rootInfo.name = childInfo[0].addr + "[" + str(childInfo[0].name) + "]"
        if len(childInfo[0].dim) != 1:
            raise Exception("The dimention of array " + rootInfo.addr + " are too large!")
    def f100(self, rootInfo, childInfo):
        # [init] --> [arr_init]
        rootInfo.name = childInfo[0].name
        rootInfo.width = childInfo[0].width
        rootInfo.mold = childInfo[0].mold
        rootInfo.dim += childInfo[0].dim
    def f101(self, rootInfo, childInfo):
        # [arr_find] --> "IDN" "[" [expression] "]"
        rootInfo.code += childInfo[2].code
        rootInfo.mold = "array"
        rootInfo.addr = childInfo[0].name
        rootInfo.dim += self.getVar(rootInfo.addr).dim
        rootInfo.name = childInfo[2].name
    def f102(self, rootInfo, childInfo):
        # [arr_find] --> [arr_find] "[" [expression] "]"
        rootInfo.name = self.newTemp("int", 4)
        rootInfo.code += childInfo[0].code + childInfo[2].code
        rootInfo.addr = childInfo[0].addr
        rootInfo.dim = childInfo[0].dim[:]
        if len(rootInfo.dim) == 1:
            raise Exception("The dimention of array " + rootInfo.addr + " are too small!")
        rootInfo.code.append(TriAddr("*", childInfo[0].name, rootInfo.dim[0], rootInfo.name))
        rootInfo.code.append(TriAddr("+=", childInfo[2].name, None, rootInfo.name))
        rootInfo.dim = rootInfo.dim[1:]
    def onlineAnalyze(self, token):
        w = token.elem
        print("---------------------------")
        print(w)
        S = self.stateStack[-1]
        if w not in self.cfl.action[S]:
            print("Failed")
            raise Exception("Parse Failed! Error in " + str(token.row) + ":" + str(token.col) + str(token.info))
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

                # print("---")
                # print(synInfo.name, synInfo.mold, synInfo.addr, synInfo.dim)
                # for c in synInfo.code:
                #     print(c)
                # print("---")
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
                # print("Reduction:", rule)
        S = self.stateStack[-1]
        if self.cfl.action[S][w][0] == Action.Shift:
            self.symbolStack.append((w, SynInfo(token.info, token.elem.name[1:-1])))
            self.stateStack.append(self.cfl.action[S][w][1])
        # for i in range(len(self.stateStack)):
        #     # self.printClosure(self.stateStack[i])
        #     print(self.symbolStack[i])
        # print("---------------------------")
        if self.cfl.action[S][w][0] == Action.Acc:
            print("OK: Semantic Analysis Finished!")

if __name__ == "__main__":
    scanner = Scanner(open("test.cpp", "rb"))
    semantic = Semantic("cfl.dump")
    while True:
        token = scanner.scan()
        # print(token.elem, token.info, token.row, token.col)
        semantic.onlineAnalyze(token)
        if token.info == "":
            break
