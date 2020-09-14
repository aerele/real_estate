# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SiteBooking(Document):
	def before_save(self):
		self.balance_amount = self.price - self.paid_amount

	def on_submit(self):
		a = frappe.get_doc('Sites', self.site)
		a.price = self.price
		if self.balance_amount == 0:
			a.status = "Sold"	
		else:
			a.status = "Booked"
		a.save()

