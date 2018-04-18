void func(int a, int b) {
    printf("%d is greater than %d\n", a, b);
}

int main() {
    int a = 10, b = 10;
    if (a < b) {
        int tmp = b;
        b = a;
        a = b;
    }
    func(a, b);
    return 0;
}
