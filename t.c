int avg(int count, int *value) {
  int i, total;
  total = 0;
  for (i = 0; i < count; i++) {
    total = total + value[i];
  }

  return (total / count);
}
