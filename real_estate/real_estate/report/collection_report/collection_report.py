# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	report_data = get_data(filters)
	columns, data = ['Customer Name', 'Mobile Number', 'Project', 'Site', 'Booking Id', 'Payment', 'Date'], report_data
	return columns, data
def get_data(filters):
	records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=', 'from_date'], 'payment_made_on': ['<=', 'to_date'] }, ['customer_mobile_number', 'booking_id', 'paid_due_amount', 'payment_made_on'])
	data = list(tuple())
	for record in records:
		row_details = []
		customer=frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
		row_details.append(customer)
		row_details.append(record.customer_mobile_number)
		row_details.append(record.booking_id.split('-')[2])
		row_details.append(record.booking_id.split('-')[3]+'-'+record.booking_id.split('-')[4])
		row_details.append(record.booking_id)
		row_details.append(record.paid_due_amount)
		row_details.append(record.payment_made_on)
		data.append(row_details)
	return data