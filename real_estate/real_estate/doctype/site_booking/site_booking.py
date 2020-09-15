# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SiteBooking(Document):
	def on_submit(self):
		site = frappe.get_doc('Sites', self.site)
		site.price = self.price
		if self.get_paid_amount == site.price:
			site.status = "Sold"	
		else:
			site.status = "Booked"
		site.save()
		if len(str(self.customer_mobile_number)) != 10:
			frappe.throw('Enter the correct mobile number')
		else:
			is_existing_customer = frappe.db.exists('Customer', {'mobile_number': self.customer_mobile_number})
			if not is_existing_customer:
				customer = frappe.new_doc('Customer')
				customer.customer_name = self.customer_name
				customer.mobile_number = self.customer_mobile_number
				customer.save()
		
		self.make_due_payment_entries()
	
	def get_paid_amount(self):
		amount = 0
		for payment in self.booking_payments:
			amount += payment.amount
		return amount

	def make_due_payment_entries(self):
		for payment_entry in self.booking_payments:
			due = frappe.new_doc('Due Payment')
			due.customer_mobile_number = self.customer_mobile_number
			due.booking_id = self.name
			due.paid_due_amount = payment_entry.amount
			due.payment_made_on = frappe.utils.data.now_datetime()
			due.save()
			due.submit()

