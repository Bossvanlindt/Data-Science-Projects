#!/bin/bash

len=$(cat $1 | wc -l)

if [[ $len -lt 10000 ]]
then
	echo Input file is smaller than 10,000 lines. Use a file with a minimum of 10,000 lines.
	exit 1
fi

echo $len
head -n 1 $1
tail -n 10000 $1 | grep '[pP][oO][tT][uU][sS]' | wc -l
head -n 200 $1 | tail -n 100 | grep -w fake | wc -l