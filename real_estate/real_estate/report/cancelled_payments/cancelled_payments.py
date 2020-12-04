# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date, datetime

def execute(filters=None):
	columns, data = [], []
	if filters.from_date and filters.to_date:
		columns = get_columns(filters)
		data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{
			"label": ("Serial"),
			"fieldname": "serial",
			"width": 100
		},
		{
			"label": ("Bill Number"),
			"fieldname": "bill_number",
			"width": 100
		},
		{
			"label": ("User"),
			"fieldname": "user",
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

def get_data(filters):
	data = list(tuple())
	start_time = datetime.min.time()
	end_time = datetime.max.time()
	start_date = datetime.strptime(filters.from_date, "%Y-%m-%d").date()
	end_date = datetime.strptime(filters.to_date,"%Y-%m-%d").date()
	_fromdate = datetime.combine(start_date,start_time)
	_todate = datetime.combine(end_date,end_time)
	records = frappe.db.get_all('Due Payment',[['payment_made_on', '>=', _fromdate], ['payment_made_on', '<=', _todate],["docstatus","=",2],["owner" ,'=', filters.user]], ['serial', 'name', 'owner', 'customer_mobile_number', 'booking_id', 'paid_due_amount', 'payment_made_on'])
	for record in records:
		row_details = []
		customer = frappe.db.get_value('Customer',{'mobile_number': record.customer_mobile_number}, ['customer_name'])
		row_details.append(record.serial)
		row_details.append(record.name)
		row_details.append(record.owner)
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