# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	details = get_data(filters)
	columns, data = [{"fieldname":"Booking_id","width" : 200},{"fieldname":"Project","width" : 150},{"fieldname":"Block","width" : 150},{"fieldname":"Site","width" : 150},{"fieldname":"Customer Name","width" : 150},{"fieldname":"Mobile number","width" : 150},{"fieldname":"Price","width" : 150},{"fieldname":"Due Amount","width" : 150},{"fieldname":"Balance","width" : 150},{"fieldname":"Starting Date","width" : 150},{"fieldname":"Weeks","width" : 150},{"fieldname":"Deadline","width" : 150}], details
	return columns, data

def get_data(filters):
	all_details = list(tuple())
	site_booking_record = frappe.db.get_all("Site Booking",{"project":filters.project,"docstatus" : 1},["name","project","block","site","customer_name","customer_mobile_number","price","starting_date","number_of_weeks","payment_deadline","modified"])
	for record in site_booking_record:
		details = []
		details.append(record["name"])
		details.append(record["project"])
		details.append(record["block"])
		details.append(record["site"])
		details.append(record["customer_name"])
		details.append(record["customer_mobile_number"])
		details.append(record["price"])
		due_amount = get_due(record["name"])
		balance = record["price"] - due_amount
		details.append(due_amount)
		details.append(balance)
		details.append(record["starting_date"])
		details.append(record["number_of_weeks"])
		details.append(record["payment_deadline"])
		all_details.append(details)
	return (sorted(all_details, key = lambda x: x[10]))

def get_due(name):
	due_record = frappe.db.get_all("Due Payment",{"booking_id":name},["paid_due_amount"])
	amount = 0 
	for record in due_record:
		amount += record["paid_due_amount"]
	return amount
	
		

