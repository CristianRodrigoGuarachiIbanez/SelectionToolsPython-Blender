
#include <stdio.h>
#include   <stdlib.h>
#include <iostream>
//https://stackoverflow.com/questions/29758662/c-conversion-from-numpy-array-to-mat-opencv#
void populate(int*****arr){
    for(int i =0; i<5;i++){
       for(int o=0;o<2;o++){
       for(int j =0; j<7; j++){
         for(int k=0;k<10;k++){
           for(int n=0;n<8;n++){
            arr[i][o][j][k][n] =2;
             }
           }
         }
       }
    }
}

void printInt(int*****arr){
    int counter = 0;
    for(int i =0; i<5;i++){
       for(int o=0;o<2;o++){
       for(int j =0; j<7; j++){
         for(int k=0;k<10;k++){
           for(int n=0;n<8;n++){
            counter++;
            //std::cout<<counter<<std::endl;
            std::cout<<counter<< ":" <<arr[i][o][j][k][n]<<std::endl;
             }
           }
         }
       }
    }
}

int main(){
  int w = 5, im=2, x = 7, y = 10, z = 8;
  int *****array;
  int i, j, k;

  array = (int *****)malloc(sizeof(double ****) * w);
 
  for(i = 0;i < w;++i)
  {
    array[i] = (int****)malloc(sizeof(double***)*im);  
    for(int n=0;n<im;n++){  
         array[i][n] = (int***)malloc(sizeof(double **) * x);

    for(j = 0;j < x;++j)
    {
      array[i][n][j] = (int**)malloc(sizeof(double *) * y);

      for(k = 0;k < y;++k)
        array[i][n][j][k] = (int*)malloc(sizeof(double) * z);
       }
    }
  }
    populate(array);
    printInt(array);

    return 0;
}
