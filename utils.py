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
        self.producers = []
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

class Table:
    pass
