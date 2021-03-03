#!/bin/bash

cd numConvert
g++ numConverter.cpp -o main

varb=(10 20 30 40)

for i in "${varb[@]}"
do
    ./main dec hex $i    
done
