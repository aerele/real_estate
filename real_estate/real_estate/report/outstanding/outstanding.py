# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

#from __future__ import unicode_literal
import frappe

def execute(filters=None):
	details = []
	if(filters.project and filters.block and filters.sites and not(filters.customer)):
		details = get_details(filters)
		columns, data = ["Customer","Mobile","Projects", "Sites", "Booking Id", "Due payment"], details
		return columns, data
	elif(filters.customer):
		print("enter the cystinre")
		details = get_customer_details(filters)
		columns, data = ["Customer","Mobile","Projects", "Sites", "Booking Id", "Due payment"], details
		return columns , data
	columns, data = ["Customer","Mobile","Projects", "Sites", "Booking Id", "Due payment"], []
	return columns, data
def get_details(filters):
	all_details = list(tuple())
	site_record = frappe.db.get_all("Site Booking",{"project":filters.project,"block":filters.block,"site":filters.site},["customer_name","customer_mobile_number","name"])
	due_record = frappe.db.get_all("Due Payment",{"booking_id": site_record[0]["name"]},["paid_due_amount"])
	for record in due_record:
		details = []
		details.append(site_record[0]["customer_name"])
		details.append(site_record[0]["customer_mobile_number"])
		details.append(filters.project)
		details.append(filters.sites)
		details.append(site_record[0]["name"])
		details.append(record["paid_due_amount"])
		all_details.append(details)
	return all_details
def get_customer_details(filters):
	all_details = list(tuple())
	site_record =  frappe.db.get_all("Site Booking",{"customer_name":filters.customer.split("-")[0],"customer_mobile_number":filters.customer.split("-")[1]},["name"])
	print(site_record)
	for site in site_record:
		details = []
		due_record =  frappe.db.get_all("Due Payment",{"booking_id":site["name"]},["paid_due_amount"])
		for record in due_record:
			details.append(filters.customer.split("-")[0])
			details.append(filters.customer.split("-")[1])
			details.append(site["name"].split("-")[0])
			details.append(site["name"].split("-")[2]+"-"+site["name"].split("-")[3])
			details.append(site["name"])
			details.append(record["paid_due_amount"])
			all_details.append(details)
	print(all_details)
	return all_details


	

					

		



