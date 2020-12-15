# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

#from __future__ import unicode_literal
import frappe
from datetime import date

def execute(filters=None):
	details = []
	columns = []
	if(filters.project and filters.block and filters.sites):
		details = get_details(filters)
		columns = get_columns(filters)
		
	empty_row = []
	for i in range(len(columns)):
		empty_row.append('')
	details.append(empty_row)
	return columns, details
	
def get_details(filters):
	all_details = list(tuple())
	total = 0
	price = 0
	site_record = frappe.db.get_all("Site Booking",{"project":filters.project,"block":filters.block, "site":filters.sites},["serial","customer_name","customer_mobile_number", "block", "site", "price" ])
	if(site_record):
		price = site_record[0]["price"]
		due_record = frappe.db.get_all("Due Payment",{"serial": site_record[0]["serial"],"docstatus":1},["name", "paid_due_amount", "creation"])
		for record in due_record:
			details = []
			details.append(site_record[0]["serial"])
			details.append(site_record[0]["customer_name"])
			details.append(filters.project)
			details.append(site_record[0]["block"])
			details.append(site_record[0]["site"])
			details.append(record["paid_due_amount"])
			details.append(record["name"])
			details.append(record["creation"].date())
			details.append(site_record[0]["customer_mobile_number"])
			total = total + record["paid_due_amount"]
			all_details.append(details)
	details = []
	paid = total
	balance = price - paid
	details.append("")
	details.append("<b>Price</b>")
	details.append(price)
	details.append("")
	details.append("<b>Paid</b>")
	details.append(paid)
	details.append("")
	details.append("<b>Balance</b>")
	details.append(balance)
	details.append("")
	all_details.append(details)
	return all_details

def get_columns(filters):
	columns = [
		{
			"label": ("Serial"),
			"fieldname": "serial",
			"width": 100
		},
		{
			"label": ("Customer"),
			"fieldname": "customer",
			"width": 150
		},
		{
			"label": ("Projects"),
			"fieldname": "projects",
			"width": 150
		},
		{
			"label": ("Block"),
			"fieldname": "block",
			"width": 80
		},
		{
			"label": ("Sites"),
			"fieldname": "sites",
			"width": 120
		},
		{
			"label": ("Due payment"),
			"fieldname": "due_payment",
			"width": 100
		},
		{
			"label": ("Bill Number"),
			"fieldname": "bill_number",
			"width": 100
		},
		{
			"label": ("Bill Date"),
			"fieldname": "bill_date",
			"width": 100
		},
		{
			"label": ("Mobile"),
			"fieldname": "mobile",
			"width": 100
		}
	]
	return columns



	

					

		



