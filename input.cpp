#include <stdio.h>

int main() {
  FILE *fin = fopen("input.txt", "r");
  int n;
  fscanf(fin, "%d", &n);
  int sum = 0;
  for (int i = 0; i < n; i++) {
    int t;
    fscanf(fin, "%d", &t);
    sum += t;
  }
  printf("%f\n", sum/(double)n);
  return 0;
}
