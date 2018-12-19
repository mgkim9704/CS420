int main(void) {
  int i, j, k;
  j = 3; k = 3;
  for (i = 0; i < 4; i++) {
    int k; k = 8;
    j++;
  }

  { int j; j = 0; }

  printf("%d %d\n", j, k);
  return j + k;
}
