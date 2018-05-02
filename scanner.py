# -*- coding: utf-8 -*-

from utils import Code, Element, keywords, Token

class Scanner:
    def __init__(self, file):
        self.file = file
    def goback(self):
        self.file.seek(-1, 1)
    def getc(self):
        return str(self.file.read(1), encoding='utf-8')

    def scanIdentifier(self):
        s = ""
        while True:
            c = self.getc()
            if c == '':
                break
            if not (c.isdigit() or c.isalpha() or c == '_'):
                self.goback()
                break
            s += c
        if s in keywords:
            return Token(Element('"' + s + '"'), s)
        else:
            return Token(Element('"IDN"'), s)


    def scanInteger(self):
        number = 0
        while True:
            c = self.getc()
            if c.isdigit():
                number = number * 10 + int(c)
            else:
                self.goback()
                break
        return Token(Element('"INT10"'), number)

    def scanSymbol(self):
        symbol = ""
        while True:
            c = self.getc()
            if c == '':
                break
            if c not in "!,+-*/%=(){}[];<>|^&:\"":
                self.goback()
                break
            if (symbol+c) in Code.__dict__:
                symbol += c
            else:
                self.goback()
                break
            print("symbol 1:", symbol)
        print("symbol:", symbol)
        return Token(Element('"' + symbol + '"'), symbol)

    def scan(self):
        while True:
            c = self.getc()
            if c == "":
                return Token(Element('"#"'), "")
            if c == " ":
                continue
            if c in "!,+-*/%=(){}[];<>|^&:\"":
                self.goback()
                return self.scanSymbol()
            elif c.isdigit():
                self.goback()
                return self.scanInteger()
            elif c.isalpha() or c == '_':
                self.goback()
                return self.scanIdentifier()


if __name__ == "__main__":
    f = open("test.cpp", "rb")
    scanner = Scanner(f)
    while True:
        token = scanner.scan()
        print(token.elem, token.info)
        if token.info == "":
            break
