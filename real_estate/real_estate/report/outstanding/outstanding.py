# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

#from __future__ import unicode_literal
import frappe

def execute(filters=None):
	details = []
	print(filters)
	if(filters.project and filters.block and filters.sites and not(filters.customer)):
		details = get_details(filters)
		columns, data = [{"fieldname": "Customer", "width" : 150},{"fieldname": "Mobile", "width" : 120},{"fieldname": "Projects", "width" : 100}, {"fieldname": "Sites", "width" : 50}, {"fieldname": "Booking Id", "width" : 250}, {"fieldname": "Due payment", "width" : 80}], details
		return columns, data
	if(not filters.project and not filters.block and not filters.sites and filters.customer):
		details = get_customer_details(filters)
		columns, data = [{"fieldname": "Customer", "width" : 150},{"fieldname": "Mobile", "width" : 120},{"fieldname": "Projects", "width" : 100}, {"fieldname": "Sites", "width" : 50}, {"fieldname": "Booking Id", "width" : 250}, {"fieldname": "Due payment", "width" : 80}], details
		return columns , data
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


	

					

		



