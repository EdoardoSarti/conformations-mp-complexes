#!/bin/bash

pdbs=$(ls ~/data | cut -c1-4)


for pdb1 in $pdbs
do
	for pdb2 in $pdbs
	do
		grep "^.....$pdb2" "/home/manpreet/data/${pdb1}-out-values.txt" >> ~/clustering/new_data_file.txt
	done
done


