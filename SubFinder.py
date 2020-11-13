#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import gethostbyname, gaierror
from sys import argv, exit
from os import listdir, getcwd


def Helper():
	print("""
	Usage: SubFinder [-h] [-w <wordlist>] <url.fr> | (url1.fr,url2.com,etc)  
		Description:
			A simple script to find subdomain and ip of... domain x)
			The result is exported in 'subdomain_<url>.txt'
			To try multiple url in same time enter the url like (u1.fr,u2.com,etc)
		Options:
			-h 		Show this message
			-w <wordlist> 	Wordlist file to test subdomain (default=wordlist.txt)

	""")


def ReadWordlist(wlf):
	"""
		Function to read the wordlist file
		:param wlf:		Wordlist file to read
		:return: 		List of subdomain
	"""
	# Test if wordlist present in current directory
	if wlf in listdir(getcwd()):
		# open file and record subdomain in list
		with open(wlf, 'r') as sdl:
			lstsub = [ sub for sub in sdl.readlines() ]

		return lstsub

	else:
		print('\t\t[!] No wordlist found in this directory !!')
		exit(1)


def ExportResult(results, burl):
	"""
		Function to Export the result of the function SubFinder
		:param results:		List of subdomain and IP find
		:param burl:		Base url to named the exported file
	"""

	outputfile = 'subdomain_%s.txt' %(burl)
	with open(outputfile, 'a') as of:
		for r in results:
			of.write('%s\n' %(r))

	print('\t[v] Results Rexported in: %s\\%s' %(getcwd(), outputfile))
	print()


def SubFinder(lstsub, url):
	"""
		Function to test if a subdomain exist for a particular domain
		:param lstsub:		List of subdomain to test
		:param url:			The base url
	"""
	# if www present then remove it
	if url.find('www') != 1:
		url = url.replace('www.', '')

	# if http:// present then remove it
	if url.find('http://') != -1:
		url = url.replace('http://', '')		

	# if https:// present then remove it
	if url.find('https://') != -1:
		url = url.replace('https://', '')		

	# add in list the first string use for the export
	lstResp = ['\t[+] Base URL: %s  -- IP: %s' %(url, gethostbyname(url))]
	print(lstResp[0])

	# init index
	i = 1
	# iter in all subdomain
	for sub in lstsub:
		try:
			# Format the string like: 'SubDomain.url.fr'
			tocheck = '%s.%s' %(sub[:-1], url)
			# call gethostby name to record the IP of subdomain (if exist)
			response = '\t\t[%s] URL: %s ---- IP: %s'  %(i, tocheck, gethostbyname(tocheck))
			print(response)

			# if exist add the result in the list
			lstResp.append(response)

			i += 1

		except(gaierror):
			continue

	print('\t[+] Total subdomain find: %s' %(i-1))
	# Call export function at the end
	ExportResult(lstResp, url)



if __name__ == '__main__':
	print("""
	Welcome to...		
	   _____       __    _______           __         
	  / ___/__  __/ /_  / ____(_)___  ____/ /__  _____
	  \__ \/ / / / __ \/ /_  / / __ \/ __  / _ \/ ___/
	 ___/ / /_/ / /_/ / __/ / / / / / /_/ /  __/ /    
	/____/\__,_/_.___/_/   /_/_/ /_/\__,_/\___/_/    
					Developed by Icenuke.

	""")

	try:
		# init wordlist name
		wordlist = 'wordlist.txt'

		# check the length of argument, if not equal or sup of 2
		# go to else and call helper
		if len(argv) >= 2:
			try:
				# if help arg present call helper
				if '-h' in argv:
					Helper()

				# if wordlist arg present then add the nom wordlist name
				if '-w' in argv:
					wordlist = argv[argv.index('-w')+1]

				# go read and record the list of subdomain to try
				lsts = ReadWordlist(wordlist)

				# test to know if multi domain is present
				if argv[-1].find('(') != -1:
					# format the arg with multi domain
					lstU = argv[-1].replace('(', '').replace(')', '').split(',')

					# iter in all domain
					for Url in lstU:
						# add threading here soon ?
						# call the function subfinder with list of subdomain and the domain to try
						SubFinder(lsts, Url)

				# if no multi domain present then go to try the subdomain for the domain
				else:
					SubFinder(lsts, argv[-1])

			except Exception as e:
				Helper()
				print('\t[!] %s' %(e))

		else:
			Helper()

	except Exception as e:
		Helper()
		print('\t[!] %s' %(e))
