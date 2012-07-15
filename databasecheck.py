#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select, insert

# TODO: figure out url to connect
engine = create_engine('sqlite:///:memory:', echo=True)
conn = engine.connect()
metadata = MetaData()

# returns a list of missing forms
# implies form_table exists
def form_check(form_list):
	form_query = form_table.select()
	results = conn.execute(form_query)

	# collect hashes to chech against
	hashes = []
	for row in results:
		hashes.append(str(row.Hash))

	hashes = set(hashes)

	missing_forms = []

	for form in form_list:
		if form_list[form].Hash not in hashes:
			missing_forms.append(str(form_list[form].Hash))

	return missing_forms


# inserts new form records
# form_table is Python lable for 'forms' table in database
def insert_missing_forms(missing_form):
	# map form elements
	DateCreated, DateUpdated, Description, Email, EndDate, 
	EntryLimit, Hash, IsPublic, Language, LinkEntries, 
	LinkEntriesCount, LinkFields, Name, RedirectMessage, 
	StartDate, Url = missing_form.DateCreated, 
	missing_form.DateUpdated, missing_form.Description, 
	missing_form.Email, missing_form.EndDate,
	missing_form.EntryLimit, missing_form.Hash, missing_form.IsPublic,
	missing_form.Language, missing_form.LinkEntries, 
	missing_form.LinkEntriesCount, missing_form.LinkFields,
	missing_form.Name, missing_form.RedirectMessage, 
	missing_form.StartDate, missing_form.Url

	# insert form record into form table in MySQL
	form_table = select([form_table])
	form_table.insert().values(DateCreated=DateCreated, DateUpdated=DateUpdated, 
		Description=Description, Email=Email, EndDate=EndDate, 
		EntryLimit=EntryLimit, Hash=Hash, IsPublic=IsPublic, 
		Language=Language, LinkEntries=LinkEntries, 
		LinkEntriesCount=LinkEntries, LinkFields=LinkFields, 
		Name=Name, RedirectMessage=RedirectMessage, 
		StartDate=StartDate, Url=Url)

	update_table = conn.execute(form_table)


# Update question list table
# Implies question table is already created
def update_question_list(question):
	question_table = select([questions])

	# auto increments primary key
	question_table.insert().values(question_text=question) 

	update_question_table = conn.execute(question_table)


# Update answer table
# Implies answer table is already created
def SurveyAnswers(answer):
	answer_table = select([answers])

	#auto increments primary key
	answer_table.insert().values(answer_text=answer, date_completed=
		date_completed, )

	update_answer_table = conn.execute(answer_table)





