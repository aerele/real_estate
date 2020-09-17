# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DuePayment(Document):
	def validate(self):
		self.payment_made_on = frappe.utils.data.now_date()
