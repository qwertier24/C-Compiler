from scanner import Scanner
from CFL import ContextFreeLanguage

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
    cfl.addRule("[S_p]", "[S]")
    cfl.addStarter("[S_p]")
    cfl.addEnder('"#"')

    cfl.init()

    testFile = open("test.cpp", "rb")
    flag = True
    while True:
        token = Scanner.scan(testFile)
        cfl.onlineParse(token, flag)
        flag = False
        if token.info == "":
            break
