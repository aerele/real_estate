# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, _dict

def execute(filters=None):
	columns = []
	data = []
	if (filters.project and filters.block):
		details = get_status(filters)
		data = details
		columns = [
			{
				"label": _("Project"),
				"fieldname": "project",
				"width": 150
			},
			{
				"label": _("Block"),
				"fieldname": "block",
				"width": 80
			},
			{
				"label": _("Sites"),
				"fieldname": "sites",
				"width": 120
			},
			{
				"label": _("Status"),
				"fieldname": "status",
				"width": 80
			},
			{
				"label": _("Booking Id"),
				"fieldname": "bookind_id",
				"fieldtype": "Link",
				"options": "Site Booking",
				"width": 100
			},
			{
				"label": _("Serial"),
				"fieldname": "serial",
				"width": 100
			},
			{
				"label": _("Customer Name"),
				"fieldname": "customer_name",
				"width": 100
			},
			{
				"label": _("Price"),
				"fieldname": "price",
				"width": 100
			},
			{
				"label": _("Paid Amount"),
				"fieldname": "paid_amount",
				"width": 100
			},
			{
				"label": _("Outstanding"),
				"fieldname": "balance",
				"width": 100
			},
			
		]
	return columns, data

def get_paid_amount(serial):
	amount = 0
	all_amount = frappe.db.get_list("Due Payment",{"serial":serial},["paid_due_amount"])
	for paid in all_amount:
		amount += paid["paid_due_amount"]
	return amount


def get_status(filters):
	all_details = list(tuple())
	blocks = filters.block
	for block in blocks:
		site_status = frappe.db.get_list("Sites",{"real_estate_project":filters.project, "block_name":block },["site_name","status"])
		for status in site_status:
			details = []
			details.append(filters.project)
			details.append(block)
			details.append(status["site_name"])
			details.append(status["status"])
			booking_id, serial , customer_name , price , paid, balance = "", "", "", "", "", ""
			if status["status"] != "Open":
				if frappe.db.exists("Site Booking",{"project":filters.project, "block":block,"site": status["site_name"], "docstatus": 1},["serial"]):
					site_booking_details = frappe.db.get_value("Site Booking",{"project":filters.project, "block":block,"site": status["site_name"]},["name", "serial", "customer_name", "price"])
					booking_id, serial, customer_name, price = site_booking_details[0], site_booking_details[1], site_booking_details[2], site_booking_details[3]
					paid = get_paid_amount(serial)
					balance =  price - paid
			details.append(booking_id)
			details.append(serial)
			details.append(customer_name)
			details.append(price)
			details.append(paid)
			details.append(balance)
			all_details.append(details)
	return all_details
