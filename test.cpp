void func(int a, int b) {
}

int main() {
  int a = 10, b = 10, tmp;
  int arr[10];
  if (a < b) {
    tmp = b;
    b = a;
    a = b;
  }
  func(a, b);
  return 0;
}
