# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Sites(Document):
	def validate(self):
		if self.block_name == "None":
			pass
		else:
			blocks = []
			block_doc = frappe.get_doc("Project",self.real_estate_project)
			for block_data in block_doc.block_record:
				blocks.append(block_data.block_name)
			if self.block_name not in  blocks:
				frappe.throw("Enter Correct Block Name")


	def on_cancel(self):
		frappe.throw('Can\'t deleted the site')
		if self.status == 'Sold':
			frappe.throw('Can\'t deleted the site')

