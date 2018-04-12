from enum import Enum

Code = Enum('Code', ('Variable', 'integer', '*', '=', '#',
                     'e', '{', '}', '+', '-', '/', "identifier",
                     'string', 'int', 'float', '"', '(', ')', 'for',
                     'if', 'return'))
keywords = {"int", "float", "for", "if", "return"}

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
        Scanner.goback(file)
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
            return Token(Element('"identifier"'), s)


    def scanInteger(file):
        Scanner.goback(file)
        number = 0
        while True:
            c = Scanner.getc(file)
            if c.isdigit():
                number = number * 10 + int(c)
            else:
                Scanner.goback(file)
                break
        return Token(Element('"integer"'), number)

    def scan(file):
        while True:
            c = Scanner.getc(file)
            if c == "":
                return Token(Element('"#"'), "")
            if c == " ":
                continue
            if c in "+-*/=(){};<>|^&":
                return Token(Element('"' + c + '"'), c)
            elif c.isdigit():
                return Scanner.scanInteger(file)
            elif c.isalpha() or c == '_':
                return Scanner.scanIdentifier(file)


if __name__ == "__main__":
    f = open("test_file.g", "rb")
    while True:
        token = Scanner.scan(f)
        print(token.elem, token.info)
        if token.info == "":
            break
