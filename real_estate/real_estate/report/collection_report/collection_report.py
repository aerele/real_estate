# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if filters.from_date and filters.to_date and filters.project and filters.block and filters.sites:
		report_data = get_data_with_site(filters)
		columns, data = ['Customer Name', 'Mobile Number', 'Project', 'Site', 'Booking Id', 'Payment', 'Date'], report_data
		return columns, data
	elif filters.from_date and filters.to_date and filters.user:
		report_data = get_data_with_user(filters)
		columns, data = ['Customer Name', 'Mobile Number', 'Project', 'Site', 'Booking Id', 'Payment', 'Date'], report_data
		return columns, data
	elif filters.from_date and filters.to_date:
		report_data = get_data(filters)
		columns, data = ['Customer Name', 'Mobile Number', 'Project', 'Site', 'Booking Id', 'Payment', 'Date'], report_data
		return columns, data
	else:
		return [],[]
def get_data(filters):
	records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>', filters.from_date], 'payment_made_on': ['<', filters.to_date] }, ['customer_mobile_number', 'booking_id', 'paid_due_amount', 'payment_made_on'])
	data = list(tuple())
	for record in records:
		row_details = []
		customer = frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
		row_details.append(customer)
		row_details.append(record.customer_mobile_number)
		row_details.append(record.booking_id.split('-')[0])
		row_details.append(record.booking_id.split('-')[2]+'-'+record.booking_id.split('-')[3])
		row_details.append(record.booking_id)
		row_details.append(record.paid_due_amount)
		row_details.append(record.payment_made_on.date())
		data.append(row_details)
	return data
def get_data_with_site(filters):
	

	data = list(tuple())
	for site in filters.sites:
		booking_id = frappe.db.get_value('Site Booking',{'project':filters.project , 'site':site },['name'])
		records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=', filters.from_date], 'payment_made_on': ['<=', filters.to_date] , 'booking_id': booking_id }, ['customer_mobile_number','paid_due_amount', 'payment_made_on'])
		print(records)
		for record in records:
			row_details = []
			customer = frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
			row_details.append(customer)
			row_details.append(record.customer_mobile_number)
			row_details.append(filters.project)
			row_details.append(site)
			row_details.append(booking_id)
			row_details.append(record.paid_due_amount)
			row_details.append(record.payment_made_on.date())
			data.append(row_details)
	return data
def get_data_with_user(filters):
	records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=', filters.from_date], 'payment_made_on': ['<=', filters.to_date] }, ['customer_mobile_number', 'booking_id', 'paid_due_amount', 'payment_made_on'])
	data = list(tuple())
	for record in records:
		row_details = []
		customer=frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
		row_details.append(customer)
		row_details.append(record.customer_mobile_number)
		row_details.append(record.booking_id.split('-')[0])
		row_details.append(record.booking_id.split('-')[2]+'-'+record.booking_id.split('-')[3])
		row_details.append(record.booking_id)
		row_details.append(record.paid_due_amount)
		row_details.append(record.payment_made_on.date())
		data.append(row_details)
	return data
