# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, _dict

def execute(filters=None):
	details = get_data(filters)
	data = details
	columns = [
		{
			"label": _("Bookind ID"),
			"fieldname": "Booking_id",
			"width": 250
		},
		{
			"label": _("Project"),
			"fieldname": "Project",
			"width": 150
		},
		{
			"label": _("Block"),
			"fieldname": "Block",
			"width": 80
		},
		{
			"label": _("Site"),
			"fieldname": "Site",
			"width": 80
		},
		{
			"label": _("Customer Name"),
			"fieldname": "Customer Name",
			"width": 150
		},
		{
			"label": _("Mobile Number"),
			"fieldname": "Mobile number",
			"width": 120
		},
		{
			"label": _("Price"),
			"fieldname": "Price",
			"width": 80
		},
		{
			"label": _("Due Amount"),
			"fieldname": "Due Amount",
			"width": 100
		},
		{
			"label": _("Balance"),
			"fieldname": "Balance",
			"width": 80
		},
		{
			"label": _("Starting Date"),
			"fieldname": "Starting Date",
			"width": 120
		},
		{
			"label": _("Weeks"),
			"fieldname": "Weeks",
			"width": 80
		},
		{
			"label": _("Deadline"),
			"fieldname": "Deadline",
			"width": 90
		}
	]
	return columns, data

def get_data(filters):
	all_details = list(tuple())
	site_booking_record = frappe.db.get_list("Site Booking",{"project":filters.project,"docstatus" : 1},["name","project","block","site","customer_name","customer_mobile_number","price","starting_date","number_of_weeks","payment_deadline"],order_by="modified asc")
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
	return all_details

def get_due(name):
	due_record = frappe.db.get_all("Due Payment",{"booking_id":name},["paid_due_amount"])
	amount = 0 
	for record in due_record:
		amount += record["paid_due_amount"]
	return amount
	
		

