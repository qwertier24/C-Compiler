#ifndef SCANNER_HPP_INCLUDED
#define SCANNER_HPP_INCLUDED
#include <stdio.h>
#include <fstream>
#define STR 0 // 字符串常量
#define CHR 1 // 字符常量
#define INT 2 // 整数常量
#define FLT 3 // 浮点数常量
#define BOL 4 // 布尔常量
#define IDT 5 // 标识符
#define SEP 6 // 分界符
#define OPT 7 // 运算符
#define KEY 8 // 关键字
#define INC 9 // 宏定义
#define FIL 10 // 文件

// 变量

struct Word {
  int code;
  void* data;
  void print();
  Word(int code, void* data) : code(code), data(data) {
  }
};

Word* wordScanner(std::ifstream &file);

#endif // SCANNER_HPP_INCLUDED
