# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if filters.from_date and filters.to_date and  filters.project and filters.block and filters.sites:
		report_data = get_data_with_site(filters)
		columns = get_columns(filters)
		return columns, report_data
	elif filters.from_date and filters.to_date and filters.user:
		report_data = get_data_with_user(filters)
		columns = get_columns(filters)
		return columns, report_data
	elif filters.from_date and filters.to_date:
		report_data = get_data(filters)
		columns = get_columns(filters)
		return columns, report_data
	else:
		return [],[]

def get_data(filters):
	records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=', '2020-11-22 00:00:00.000000'], 'payment_made_on': ['<=', '2020-11-23 00:00:00.000000'] }, ['serial','customer_mobile_number', 'booking_id', 'paid_due_amount', 'payment_made_on'])
	data = list(tuple())
	for record in records:
		row_details = []
		customer = frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
		row_details.append(record.serial)
		row_details.append(customer)
		row_details.append(record.customer_mobile_number)
		booking_detail = record.booking_id.split('-')
		row_details.append(booking_detail[0])
		row_details.append(booking_detail[1])
		site_name = frappe.db.get_value("Site Booking",{"name" : record.booking_id},["site"])
		row_details.append(site_name)
		row_details.append(record.booking_id)
		row_details.append(record.paid_due_amount)
		# row_details.append(record.payment_made_on.date())
		data.append(row_details)
	return data

def get_data_with_site(filters):
	data = list(tuple())
	for site in filters.sites:
		booking_id = frappe.db.get_value('Site Booking',{'project':filters.project , 'site':site },['name'])
		if(booking_id):
			records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=', '2020-11-22 00:00:00.000000'], 'payment_made_on': ['<=', '2020-11-23 00:00:00.000000']  , 'booking_id': booking_id }, ["serial",'customer_mobile_number','paid_due_amount', 'payment_made_on'])
			for record in records:
				row_details = []
				customer = frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
				row_details.append(record.serial)
				row_details.append(customer)
				row_details.append(record.customer_mobile_number)
				row_details.append(filters.project)
				block_name = frappe.db.get_value("Site Booking",{"name" : booking_id},["block"])
				row_details.append(block_name)
				row_details.append(site)
				row_details.append(booking_id)
				row_details.append(record.paid_due_amount)
				row_details.append(record.payment_made_on.date())
				data.append(row_details)
	return data

def get_data_with_user(filters):
	records = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=', '2020-11-22 00:00:00.000000'], 'payment_made_on': ['<=', '2020-11-23 00:00:00.000000'] , "owner" : filters.user }, ['customer_mobile_number', 'booking_id', 'paid_due_amount', 'payment_made_on'])
	data = list(tuple())
	for record in records:
		row_details = []
		customer=frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
		row_details.append(customer)
		row_details.append(record.customer_mobile_number)
		booking_detail = record.booking_id.split('-')
		row_details.append(booking_detail[0])
		row_details.append(booking_detail[1])
		site_name = frappe.db.get_value("Site Booking",{"name" : record.booking_id},["site"])
		row_details.append(site_name)
		row_details.append(record.booking_id)
		row_details.append(record.paid_due_amount)
		row_details.append(record.payment_made_on.date())
		data.append(row_details)
	return data

def get_columns(filters):
	columns = [
		{
			"label": ("Serial"),
			"fieldname": "serial",
			"width": 100
		},
		{
			"label": ("Customer Name"),
			"fieldname": "customer_name",
			"width": 120
		},
		{
			"label": ("Mobile Number"),
			"fieldname": "mobile_number",
			"width": 120
		},
		{
			"label": ("Project"),
			"fieldname": "project",
			"width": 150
		},
		{
			"label": ("Block"),
			"fieldname": "block",
			"width": 70
		},
		{
			"label": ("Site"),
			"fieldname": "site",
			"width": 100
		},
		{
			"label": ("Bookind ID"),
			"fieldname": "Booking_id",
			"width": 250
		},
		{
			"label": ("Payment"),
			"fieldname": "payment",
			"width": 100
		},
		{
			"label": ("Date"),
			"fieldname": "date",
			"width": 80
		}
	]
	return columns