#!/usr/bin/python3
'''
	Version: 1.4
	Last mod date: 18/11/2015 4:30PM
	Author: manimaran G
	Desc:	Without multiprocessing
'''
import os, sys
import string, re
import shutil, time

#constants
PUNC_PATTERN = re.compile("[{}]".format(re.escape(string.punctuation)))
STR_PATTERN = re.compile("[A-Za-z]")
DIGIT_PATTERN = re.compile("[\d]")

#read the file object by chunk
def read_in_chunks(f, size=128):
    while True:
        chunk = f.read(size)
        if not chunk:
            break
        yield chunk

#contains what function
def check_content(args):	
	filename, tocheck, targ_dir = args[0], int(args[1]), args[2]
	print("Reading {}.. ".format(filename))
	punc_flag = False
	dig_flag = False

	with open(filename, encoding='ISO-8859-1') as file:
		for chunk in read_in_chunks(file):
			chunk = re.sub(r'\s+', '', chunk)
			if len(STR_PATTERN.findall(chunk)) > 0:
				return False #means it contains alphapet so skip the file
			elif tocheck == 1 and len(DIGIT_PATTERN.findall(chunk)) > 0:
				return False
			elif tocheck == 2 and len(PUNC_PATTERN.findall(chunk)) > 0:
				return False
			else:
				if len(PUNC_PATTERN.findall(chunk)) > 0:
					punc_flag = True
				if len(DIGIT_PATTERN.findall(chunk)) > 0:
					dig_flag = True
		if tocheck == 1:			
			if punc_flag and not dig_flag:		
				print("Moving : {} ==> {}".format(filename, targ_dir))
				shutil.move(filename, targ_dir)
		elif tocheck == 2:
			if dig_flag and not punc_flag:
				print("Moving : {} ==> {}".format(filename, targ_dir))
				shutil.move(filename, targ_dir)
		elif tocheck == 3 and (dig_flag and punc_flag):
			print("Moving : {} ==> {}".format(filename, targ_dir))
			shutil.move(filename, targ_dir)

#main function stars here
if __name__ == '__main__':

	root_dir = input("Enter directory to traverse: ")
	targ_dir = input("Enter target directory : ").strip()


	#check if the root dir exist
	if not os.path.isdir(root_dir):
		print("{} is not a directory ".format(root_dir))
	else:
		fnames = []
		for root, dirs, files in os.walk(root_dir):
			for f in files:
				fnames.append(os.path.join(os.path.abspath(root), f))

	start_time = time.time()

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
	fil_fnames = [ f for f in fnames if os.path.splitext(f)[1] not in ['pyc', 'py', 'git']]	

	try:
	
		for file in fil_fnames:			
			targ_path = os.path.join(targ_dir, os.path.basename(file))
			#print("Filename "+os.path.basename(file))					
			#print(text)						
			if selection == 1:				
				check_content((file, 1, targ_path))
			elif selection == 2:
				check_content((file, 2, targ_path))
			elif selection == 3:
				check_content((file, 3, targ_path))
	
		print("--- {:.2f} seconds ---".format((time.time() - start_time)))

	except Exception as e:
		print(e)
