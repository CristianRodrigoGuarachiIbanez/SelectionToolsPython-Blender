
#include <stdio.h>
#include   <stdlib.h>
#include <iostream>
//https://stackoverflow.com/questions/29758662/c-conversion-from-numpy-array-to-mat-opencv
int printInt(****int arr{
    for(int i =0; i<5;i**){
       for(int j =0; j<7; j++){
         for(int k=0;k<10;k++){
           for(int n=0;n<8;n++){
             std::cout<<arr[i][j][k][n]<<std::endl;
             }
           }
         }
       }
}

int main(){
  int w = 5, x = 7, y = 10, z = 8;
  int ****array;
  int i, j, k;

  array = malloc(sizeof(double ***) * w);

  for(i = 0;i < w;++i)
  {
    array[i] = malloc(sizeof(double **) * x);

    for(j = 0;j < x;++j)
    {
      array[i][j] = malloc(sizeof(double *) * y);

      for(k = 0;k < y;++k)
        array[i][j][k] = malloc(sizeof(double) * z);
       }
    }

    printInt(array);


    return 0;
}