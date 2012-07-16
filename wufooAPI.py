#!/usr/bin/env python

import sys
from pyfoo import PyfooAPI
from databasecheck import form_check, insert_missing_forms
from databasecheck import update_question_list, update_answer_list, question_check
from sqlalchemy.exc import ResourceClosedError

# TODO: Add ability to take in command line arguments if only wanting to 
# update a specific form via its hash (rather than look thru every form
# available)
# TODO: I'm not sure I'm handling errors correctly.  I'm intending to build
# the error list for the try/excepts, but it's repetitive. Must find a better
# solution

# put answers into database
def answers(api):
	pass


# puts question(s) into database
def questions(api):
	# check if database has current list of forms
	form_list = api.forms # list of all forms
	missing_forms = form_check(form_list) # list of forms not in db

	# add to list of all forms in database
	for form in missing_forms:
		try:
			insert_missing_forms(form)

		except ResourceClosedError:
			print "Could not connect to database. Try establishing the \
			connection again."

		# TODO: add more exceptions & how to handle them

	# build question list from all for all forms
	question_list = build_question_list(form_list)	

	# check to see if questions are already in db
	missing_list = []
	for question in question_list:
		try:
			missing_q = question_check(question['questiontext'])
			if missing_q not None:
				missing_list.append(missing_q)

		except ResourceClosedError:
			print "Could not connect to database. Try establishing the \
			connection again."

	# add question list to db
	for question in missing_list:
		try:
			update_question_list(question)

		except ResourceClosedError:
			print "Could not connect to database. Try establishing the \
			connection again."

		# TODO: add more exceptions & how to handle them



def main():
	# connect to WuFoo
	account = 'cs50'
	api_key = '55I0-G74M-IHAK-L8JJ'

	api = PyfooAPI(account, api_key)

	# if given a hash, only update/insert specified survey
	if len(sys.argv) > 0:
		hash_list = []
		for i in range(len(sys.argv)):
			hash_list.append(sys.argv[i])

		# TODO: complete arg processing

	# if no hashes, find and process Qs & As from forms
	else:
		questions(api)
		answers(api)



if __name__ == '__main__':
	main()
