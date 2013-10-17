import os, sys

path=input('input path:\n')
toFind=input('input chars to find:\n')
toReplace=input('input chars to replace:\n')

for fname in os.listdir(path):
	os.replace(fname, fname.replace(toFind, toReplace) )
	