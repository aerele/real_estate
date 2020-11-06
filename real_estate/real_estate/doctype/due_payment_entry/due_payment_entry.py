# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DuePaymentEntry(Document):
	def validate(self):
		total = get_total(self.booking_id,self.due_amount)
		self.balance = self.price - total
	
	def on_submit(self):
		due = frappe.new_doc("Due Payment")
		due.customer_mobile_number = self.customer_mobile_number
		due.booking_id = self.booking_id
		due.paid_due_amount = self.due_amount
		due.payment_made_on = self.date
		due.save()
		due.submit()
	pass

def get_total(booking_id,amount):
		initial = float(amount)
		due_record = frappe.db.get_all("Due Payment",{"booking_id":booking_id},["paid_due_amount"])
		print(due_record)
		for record in due_record:
			initial += record["paid_due_amount"]
		return initial

@frappe.whitelist()
def get_customer_details(project,block,site):
		customer_data = frappe.db.get_value("Site Booking",{"project" : project,"block" : block, "site" : site},["customer_name","customer_mobile_number","price","payment_deadline","name"]) 
		return customer_data