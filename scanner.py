# -*- coding: utf-8 -*-

from utils import Code, Element, keywords

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
            if c not in "!,+-*/%=(){}[];<>|^&:\"":
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
            if c in "!,+-*/%=(){}[];<>|^&:\"":
                Scanner.goback(file)
                return Scanner.scanSymbol(file)
            elif c.isdigit():
                Scanner.goback(file)
                return Scanner.scanInteger(file)
            elif c.isalpha() or c == '_':
                Scanner.goback(file)
                return Scanner.scanIdentifier(file)


if __name__ == "__main__":
    f = open("test.cpp", "rb")
    while True:
        token = Scanner.scan(f)
        print(token.elem, token.info)
        if token.info == "":
            break
