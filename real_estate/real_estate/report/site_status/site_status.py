# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if (filters.project and filters.block):
		details = get_status(filters)
		columns, data = [{"fieldname" : "Project", "width" : 150},{"fieldname" : "Block", "width" : 80},{"fieldname" : "Sites", "width" : 50},{"fieldname" : "Status", "width" : 80}], details
		return columns, data
	return [], []
	
def get_status(filters):
	all_details = list(tuple())
	block = filters.block
	for site in block:
		site_status = frappe.db.get_list("Sites",{"real_estate_project":filters.project, "block_name":site },["site_name","status"])
		for status in site_status:
			details = []
			details.append(filters.project)
			details.append(site)
			details.append(status["site_name"])
			details.append(status["status"])
			all_details.append(details)
	return all_details
