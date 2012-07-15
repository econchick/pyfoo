#!/usr/bin/env python

import sys
from pyfoo import PyfooAPI
from databasecheck import form_check, insert_missing_forms
from databasecheck import SurveyForm, SurveyQuestions
from sqlalchemy.exc import ResourceClosedError

# TODO: Add ability to take in command line arguments if only wanting to 
# update a specific form via its hash (rather than look thru every form
# available)

def main():
	# connect to WuFoo
	account = 'cs50'
	api_key = '55I0-G74M-IHAK-L8JJ'
	
	api = PyfooAPI(account, api_key)

	# if given a hash, only update/insert specified survey
	if len(sys.argv) > 0:
		hash_list = sys.argv




	else:
		# check if database has current list of forms
		form_list = api.forms
		missing_forms = form_check(form_list)


		# add to list of all forms in database
		for form in missing_forms:
			try:
				insert_missing_forms(form)

			except ResourceClosedError:
				print "Could not connect to database. Try establishing the \
				connection again."

		# create tables for new forms
		for form in missing_forms:
			try:
				SurveyForm = missing_forms[form]

			except ResourceClosedError:
				print "Could not connect to database. Try establishing the \
				connection again."

		# TODO: if some missing, create tables, grab forms & (update) entries

			# grab most recent WuFoo form
			recent_form = api.forms[-1]

			# grab latest entries
			recent_entries = recent_form.get_entries()


if __name__ == '__main__':
	main()
