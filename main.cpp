#include <fstream>
#include "scanner.hpp"

using namespace std;

int main()
{
  ifstream file("input.cpp", fstream::in);
  while (true) {
    Word *nextWord = wordScanner(file);
    if (nextWord == NULL)
      break;
    nextWord->print();
  }
  return 0;
}
