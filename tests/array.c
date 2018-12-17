int main(){
  int myarray[5], i, sum;

  for (i = 0; i < 5; i++) {
    myarray[i] = i * i;
  }

  sum = 0;
  for (i = 0; i < 5; i++) {
    sum = sum + myarray[i];
  }

  return sum;
}