#!/bin/bash
args=$(cat "/c/Users/Cheha/Desktop/PremiereBlippr/args.txt")
echo $args
python "/c/Users/Cheha/Desktop/PremiereBlippr/DetectBlips.py" $args
read -p "Press Enter to continue..."