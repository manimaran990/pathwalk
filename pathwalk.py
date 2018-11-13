#!/usr/bin/python3
import os, sys
import string, re

#to check the text contains only punctuations
def check_all_punctuation(text):
	puncs = set(string.punctuation)
	return all(i in puncs for i in text)


#to check the text contains only digits
def check_all_digits(text):
	digits = set(string.digits)
	return all(i in digits for i in text)	


#contains both puncts and digits
def contains_both(text):
	punc_pattern = re.compile("[{}]".format(re.escape(string.punctuation)))
	dig_pattern = re.compile("[\d]")
	str_pattern = re.compile("[A-Za-z]")

	return len(punc_pattern.findall(text)) > 0 and len(dig_pattern.findall(text)) > 0 and len(str_pattern.findall(text)) == 0
	


#main function stars here
if __name__ == '__main__':
	root_dir = input("Enter directory to traverse: ")
	targ_dir = input("Enter target directory : ").strip()

	#check if the root dir exist
	if not os.path.isdir(root_dir):
		print("{} is not a directory ".format(root_dir))
	else:
		fnames = []
		for root, dirs, files in os.walk('.'):
			for f in files:
				fnames.append(os.path.join(os.path.abspath(root), f))


	#make target directory
	if not os.path.isdir(targ_dir):
		print("{} is not a directory ".format(targ_dir))		
		mkdir = input("Do you want to create it: (y/n) ")
		if mkdir.lower() == 'y':
			try:
				os.mkdir(targ_dir)
			except:
				print("Invalid path. Try Again")
				sys.exit()				

	selection = int(input('''1. Move punctuation files alone,\n2. Move digits files alone,\n3. Move files contains both digits and punctuations\n'''))

	if selection not in [1,2,3]:
		print("Invalid selection")
		sys.exit(0)

	#traverse all files one by one and do the checks
	fil_fnames = [f for f in fnames if f[:-3] not in ['pyc']]	
	for file in fil_fnames:
		#print("Filename "+os.path.basename(file))
		with open(file, 'rb') as f:
			text = ''.join(f.read().decode('utf-8').strip().split('\n'))			
			#print(text)
			if contains_both(text) and selection == 3:				
				print("Moving : {} ==> {}".format(file, os.path.join(targ_dir, os.path.basename(file))))
				os.rename(file, os.path.join(targ_dir, os.path.basename(file)))
			elif check_all_punctuation(text) and selection == 1:				
				print("Moving : {} ==> {}".format(file, os.path.join(targ_dir, os.path.basename(file))))
				os.rename(file, os.path.join(targ_dir, os.path.basename(file)))
			elif check_all_digits(text) and selection == 2:				
				print("Moving : {} ==> {}".format(file, os.path.join(targ_dir, os.path.basename(file))))
				os.rename(file, os.path.join(targ_dir, os.path.basename(file)))
