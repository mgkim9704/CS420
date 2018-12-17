int fact(int x) {
  if (x <= 1) {
    return x;
  } 
  return x * fact(x-1);
}

int main() {
  int i;
  for (i = 0; i < 5; i++)
    printf("%d! = %d", i, fact(i));

  return 0;
}