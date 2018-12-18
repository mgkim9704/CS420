void main(void) {
  int p,q,r,s;
  p=1;
  q=2;
  r=3;
  s=4;

  handle(&q, &r);
  printf("%d %d %d %d", p, q, r, s);
}

void handle(int *a, int *b) {
  (*a)++; (*b)--;
}
