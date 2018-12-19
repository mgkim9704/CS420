int sum(int num) {
  if (num > 0) {
    num = num + sum(num - 1);
  }
  return num;
}

int main(void) {
  int result;
  result = sum(10);
  printf("%d\n", result);
}