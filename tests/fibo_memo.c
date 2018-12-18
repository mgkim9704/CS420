int main(void){
  int i, memo[21];
  for (i = 0; i < 21; i++)
    memo[i] = 0;
  return fibo(20, memo);
}

int fibo(int f, int *memo) {
  if (f <= 2) return 1;
  if (memo[f] != 0) return memo[f];
  return fibo(f-1, memo) + fibo(f-2, memo);
}
