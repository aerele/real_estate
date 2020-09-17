# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

#from __future__ import unicode_literal
import frappe

def execute(filters=None):
	details = get_details(filters)
	columns, data = ['Projects', 'Sites', 'Booking Id', 'Due payment'], details
	return columns, data
def get_details(filters):
	all_details = list(tuple())
	due_records = frappe.db.get_all('Due Payment', {'booking_id': filters.sites , 'customer_mobile_number': filters.mobile.split('-')[1] }, ['paid_due_amount'])
	required = filters.sites.split('-')
	project = required[2]
	site = required[3]
	site = site + '-' + required[4]
	for due in due_records:
		row = []
		row.append(project)
		row.append(site)
		row.append(filters.sites)
		row.append(due['paid_due_amount'])
		all_details.append(row)
	return all_details

					

		



