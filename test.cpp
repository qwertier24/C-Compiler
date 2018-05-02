int main() {
  int a = 10, b = 10, c = 20, d = 50, tmp;
  if (a < b && c > d) {
    tmp = a;
    a = b;
    b = a;
  }
}
