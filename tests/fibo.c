int fibo(int f) {
  if (f <= 2) return 1;
  return fibo(f-1) + fibo(f-2);
}

int main(void) {
  return fibo(20);
}