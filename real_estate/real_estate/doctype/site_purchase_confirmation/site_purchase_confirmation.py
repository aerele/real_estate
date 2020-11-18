# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SitePurchaseConfirmation(Document):
	pass



@frappe.whitelist()
def get_site_status(project,block,site):
	site_status = frappe.db.get_value("Sites",{"real_estate_project" : project,"block_name": block , "site_name" : site},["status"])
	return site_status

@frappe.whitelist()
def set_site_status(project,block,site):
	site_doc = frappe.get_doc("Sites",{"real_estate_project" : project,"block_name": block , "site_name" : site})
	site_doc.status = "Sold"
	site_doc.save()
	return "success"