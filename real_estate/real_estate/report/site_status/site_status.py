# Copyright (c) 2013, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, _dict

def execute(filters=None):
	if (filters.project and filters.block):
		details = get_status(filters)
		data = details
		columns = [
			{
				"label": _("Project"),
				"fieldname": "Project",
				"width": 150
			},
			{
				"label": _("Block"),
				"fieldname": "Block",
				"width": 80
			},
			{
				"label": _("Sites"),
				"fieldname": "Sites",
				"width": 120
			},
			{
				"label": _("Status"),
				"fieldname": "Status",
				"width": 80
			}
		]
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
