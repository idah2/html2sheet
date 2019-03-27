#!/usr/bin/env python

'''
    File name: doc2sheet.py
    Author: Daniel Story
    Date created: 3/8/2019
    Date last modified: 3/8/2019
    Python Version: 2.7, 3
'''

import sys, pandas
from bs4 import BeautifulSoup

filename=str(sys.argv[1])
rows = []

def main():
	with open(filename, "r") as file:

		html = file.read()
		soup = BeautifulSoup(html, "html.parser")
		table = soup.find()
		title = soup.find("title").text.split(":")
		inst = title[0].strip()
		data = soup.find("tbody")
		children = data.findChildren("tr" , recursive=False)
		for child in children:
			pol = child.findChild("td" , recursive=False)
			if "," in str(pol.text):
				p1 = str(pol.text).split(',')
				last = p1[0].strip()
				p2 = p1[1].split("(")
				first = p2[0].strip()
				if "-" in p2[1]:
					p3 = p2[1].split("-")
					party = p3[0].strip()
					state = p3[1].strip(")")
				else:
					state = ""
					party = p2[1].strip(")")
			else:
				last = pol.text
				first = ""
				state = ""
				party = ""
				print("Problem with " + pol.text + "in file " + filename)
			cham = pol.findNext("td" , recursive=False)
			amount = cham.findNext("td" , recursive=False)
			#print(first + " " + last + " | " + party + " | " + state + " | " + cham.text.strip() + " | " + ammount.text.strip())
			newdict = dict()
			newdict.update({'first_name': first, 'last_name': last, 'party': party, 'state': state, 'chamber': cham.text.strip(), 'amount': amount.text.strip(), 'contributing_institution': inst })
			rows.append(newdict)

	# save all rows to file
	newdf = pandas.DataFrame(rows)
	#outputfile = inst.replace(" ", "-") + "_2018.csv"
	with open('output.csv', 'a') as f:
		newdf.to_csv(f, columns=["first_name", "last_name", "party", "state", "chamber", "amount", "contributing_institution"], index=False, mode='a', header=f.tell()==0, encoding='utf-8')
		print("Done.")

if __name__ == '__main__':
  main()