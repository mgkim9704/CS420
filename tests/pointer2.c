int main(void){
  float arr[15];
  init(arr);
  return cool(arr);
}

void init(float *p) {
  int arr;
  float *q;
  for (arr = 0; arr < 7; arr++) {
    q = p + arr; 
    *q = 6-arr;
  }
}

float cool(float *q) {
  float some;
  some = 0;
  for(;*q++;) some = some + *q / 8; 
  return some;
}