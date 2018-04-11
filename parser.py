if __name__ == "__main__" :
    f = open("test_grammar.g", "r")
    while True:
        line = f.readline()
        if line == "\n" or line == "":
            break
        [L,R] = line[:-1].split('-->')
        print(L, R)
