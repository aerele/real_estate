# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if (filters.project and filters.block):
		details = get_status(filters)
		columns, data = ["Project","Block","Sites","Status"], details
		return columns, data
	columns, data = [], []
	return columns, data
def get_status(filters):
	all_details = list(tuple())
	site_status = frappe.db.get_list("Sites",{"real_estate_project":filters.project, "block_name":filters.block },["site_name","status"])
	for status in site_status:
		details = []
		details.append(filters.project)
		details.append(filters.block)
		details.append(status["site_name"])
		details.append(status["status"])
		all_details.append(details)
	return all_details
