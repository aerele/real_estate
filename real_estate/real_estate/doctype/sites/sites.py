# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Sites(Document):
	def on_cancel(self):
		if self.status == 'Sold':
			frappe.throw('Can\'t deleted the site')

