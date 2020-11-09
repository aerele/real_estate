# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

#from __future__ import unicode_literal
import frappe

def execute(filters=None):
	details = []
	if(filters.project and filters.block and filters.sites and not(filters.customer)):
		details = get_details(filters)
		columns = get_columns(filters)
		return columns, details
	if(not filters.project and not filters.block and not filters.sites and filters.customer):
		details = get_customer_details(filters)
		columns = get_columns(filters)
		return columns , details
	return [],[]
	
def get_details(filters):
	all_details = list(tuple())
	for site in filters.sites:
		site_record = frappe.db.get_all("Site Booking",{"project":filters.project,"site":site},["customer_name","customer_mobile_number","name"])
		if(site_record):
			due_record = frappe.db.get_all("Due Payment",{"booking_id": site_record[0]["name"]},["paid_due_amount"])
			for record in due_record:
				details = []
				details.append(site_record[0]["customer_name"])
				details.append(site_record[0]["customer_mobile_number"])
				details.append(filters.project)
				details.append(site)
				details.append(site_record[0]["name"])
				details.append(record["paid_due_amount"])
				all_details.append(details)
	return all_details

def get_customer_details(filters):
	all_details = list(tuple())
	site_record =  frappe.db.get_all("Site Booking",{"customer_name":filters.customer.split("-")[0],"customer_mobile_number":filters.customer.split("-")[1]},["name"])
	for site in site_record:
		name_array = site["name"].split("-")
		details = []
		due_record =  frappe.db.get_all("Due Payment",{"booking_id":site["name"]},["paid_due_amount"])
		for record in due_record:
			details.append(filters.customer.split("-")[0])
			details.append(filters.customer.split("-")[1])
			details.append(name_array[0])
			details.append(name_array[2])
			details.append(site["name"])
			details.append(record["paid_due_amount"])
			all_details.append(details)
	return all_details
def get_columns(filters):
	columns = [
		{
			"label": ("Customer"),
			"fieldname": "customer",
			"width": 150
		},
		{
			"label": ("Mobile"),
			"fieldname": "mobile",
			"width": 100
		},
		{
			"label": ("Projects"),
			"fieldname": "projects",
			"width": 150
		},
		{
			"label": ("Sites"),
			"fieldname": "sites",
			"width": 80
		},
		{
			"label": ("Booking Id"),
			"fieldname": "booking_id",
			"width": 250
		},
		{
			"label": ("Due payment"),
			"fieldname": "due_payment",
			"width": 80
		}
	]
	return columns



	

					

		



