#include "scanner.hpp"
#include <stdlib.h>
#include <string.h>

using namespace std;

void Word::print() {
  printf("%d", code);
  if (code == STR) {
    char *str = (char*)data;
    printf("%s\n", str);
  } else if (code == CHR) {
    char *str = (char*)data;
    printf("%s\n", str);
  } else if (code == INT) {
    int *num = (int*)data;
    printf("%d\n", *num);
  } else if (code == FLT) {
    float *num = (float*)data;
    printf("%f\n", *num);
  } else if (code == BOL) {
    char *str = (char*)data;
    printf("%s\n", str);
  } else if (code == IDT) {
    char *str = (char*)data;
    printf("%s\n", str);
  } else if (code == SEP) {
    char *str = (char*)data;
    printf("%s\n", str);
  } else if (code == OPT) {
    char *str = (char*)data;
    printf("%s\n", str);
  } else if (code == KEY) {
    char *str = (char*)data;
    printf("%s\n", str);
  }
}

#define SZ 1000

void goBack(ifstream &file) {
  if (!file.eof())
    file.seekg(-1, ios_base::cur);
}

Word* stringScanner(ifstream &file) { // (' or ")...
  char firstChar;
  file>>firstChar;
  char *buf = new char[1000], *cur = buf;
  memset(buf, 0, sizeof(char)*SZ);
  *(cur++) = firstChar;

  char c;
  while (file >> c && c != firstChar) {
    *(cur++) = c;
  }
  *(cur++) = c;
  goBack(file);
  return new Word(firstChar=='\"'?STR:CHR, (void*)buf);
}

Word* macroScanner(ifstream &file) { // #..
  char c;
  char *buf = new char[1000], *cur = buf;
  memset(buf, 0, sizeof(char)*SZ);
  while (file >> c && c != ' ' && c != '\n') {
    *(cur++) = c;
  }2

  goBack(file);
  return new Word(STR, (void*)buf);
}

Word* fileScanner(ifstream &file) { // <file_name>
  char c;
  char *buf = new char[1000], *cur = buf;
  memset(buf, 0, sizeof(char)*SZ);
  while (file >> c && c != '>') {
    *(cur++) = c;
  }
  *(cur++) = c;
  goBack(file);
  return new Word(FIL, (void*)buf);
}

Word* numberScanner(ifstream &file) {
  char c;
  int integer = 0;
  double decimal = 0;
  bool float_flag = false;
  int cnt = 0;
  while (file>>c && (isdigit(c) || c=='.')) {
    if (c == '.') {
      float_flag = true;
    } else {
      if (float_flag) {
        cnt++;
        decimal = decimal * 10 + c - '0';
      } else {
        integer = integer * 10 + c - '0';
      }
    }
  }
  goBack(file);
  while (cnt) {
    cnt--;
    decimal /= 10;
  }
  if (float_flag) {
    return new Word(FLT, new float(integer+decimal));
  } else {
    return new Word(INT, new int(integer));
  }
}

Word* identifierScanner(ifstream &file) {
  char c;
  char buf[1000], *cur = buf;
  memset(buf, 0, sizeof(char)*SZ);
  while (file>>c && c != ' ' && c != '\n') {
    *(cur++) = c;
  }
  goBack(file);
  return new Word(IDT, (void*)buf);
}

Word* operatorScanner(ifstream &file) {
  char c;
  char s[2];
  char *buf = new char[10], *cur = buf;
  memset(buf, 0, sizeof(char)*10);
  while (true) {
    file >> c;
    s[0] = c;
    s[1] = 0;
    if (strstr("+-*/&^|", &c) == NULL)
      break;
    *(cur++) = c;
  }
  goBack(file);
  return new Word(OPT, (void*)buf);
}

Word* separatorScanner(ifstream &file) {
  char s[2];
  file>>s[0];
  s[1] = 0;
  return new Word(SEP, (void*)s);
}

Word* wordScanner(ifstream &file) {
  char firstChar;
  while (!file.eof() && file>>firstChar && (firstChar==' ' || firstChar=='\n'));
  if (file.eof())
    return NULL;


  file.seekg(-1, ios_base::cur);
  // printf("firstChar: %d\n", (int)firstChar);


  if (isdigit(firstChar))
    return numberScanner(file);
  switch(firstChar) {
  case ';':
  case ',':
  case ':':
  case '{':
  case '}':
    return separatorScanner(file);
    break;
  case '\"':
  case '\'':
    return stringScanner(file);
    break;
  case '<':
    return fileScanner(file);
    break;
  case '#':
    return macroScanner(file);
    break;
  case '+':
  case '-':
  case '*':
  case '/':
  case '&':
  case '|':
  case '^':
    return operatorScanner(file);
    break;
  default:
    return identifierScanner(file);
  }
  return NULL;
}
