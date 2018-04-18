from enum import Enum

Code = Enum('Code', ('Variable',
                     'INT10', 'INT8', 'INT16', 'FLOAT', 'CHAR', 'STR',
                     'IDN',
                     'int', 'char', 'float', 'void',
                     '(', ')', '*', '=', '+', '-', '/', '%',
                     '!', '&&', '||',
                     '>', '>=', '<', '<=', '==', '!=', '+=', '-=', '*=', '/=', '%=',
                     '$', '#',
                     '{', '}', ';', ',', '[', ']', ':',
                     '"', 'for', "continue", "break", 'if', 'return', 'else', 'switch', 'case', 'while', 'do', 'default'))
keywords = {"int", 'char', "float", 'void', 'for', "continue", "break", 'if', 'return', 'else', 'switch', 'case', 'while', 'do', 'default'}

class Element:
    def __init__(self, name):
        self.name = name
        if name[0] == '[':
            self.code = Code.Variable
        elif name[0] == '"':
            if name[1:-1] not in Code.__dict__:
                raise Exception("Not recognized element:", name)
            for code in Code:
                if code.name == name[1:-1]:
                    self.code = code
    def __str__(self):
        return str(self.name)
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name



class Token:
    def __init__(self, elem, info):
        self.elem = elem
        self.info = info

class Scanner:
    def goback(file):
        file.seek(-1, 1)
    def getc(file):
        return str(file.read(1), encoding='utf-8')

    def scanIdentifier(file):
        s = ""
        while True:
            c = Scanner.getc(file)
            if c == '':
                break
            if not (c.isdigit() or c.isalpha() or c == '_'):
                Scanner.goback(file)
                break
            s += c
        if s in keywords:
            return Token(Element('"' + s + '"'), s)
        else:
            return Token(Element('"IDN"'), s)


    def scanInteger(file):
        number = 0
        while True:
            c = Scanner.getc(file)
            if c.isdigit():
                number = number * 10 + int(c)
            else:
                Scanner.goback(file)
                break
        return Token(Element('"INT10"'), number)

    def scanSymbol(file):
        symbol = ""
        while True:
            c = Scanner.getc(file)
            if c == '':
                break
            if c not in "!,+-*/%=(){};<>|^&:\"":
                Scanner.goback(file)
                break
            if (symbol+c) in Code.__dict__:
                symbol += c
            else:
                Scanner.goback(file)
                break
        return Token(Element('"' + symbol + '"'), symbol)

    def scan(file):
        while True:
            c = Scanner.getc(file)
            if c == "":
                return Token(Element('"#"'), "")
            if c == " ":
                continue
            if c in "+-*/=(){};<>|^&":
                Scanner.goback(file)
                return Scanner.scanSymbol(file)
            elif c.isdigit():
                Scanner.goback(file)
                return Scanner.scanInteger(file)
            elif c.isalpha() or c == '_':
                Scanner.goback(file)
                return Scanner.scanIdentifier(file)


if __name__ == "__main__":
    f = open("test_cpp.cpp", "rb")
    while True:
        token = Scanner.scan(f)
        print(token.elem, token.info)
        if token.info == "":
            break
