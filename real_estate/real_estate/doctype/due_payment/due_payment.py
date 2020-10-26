# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class DuePayment(Document):
	def validate(self):
		self.payment_made_on = frappe.utils.data.now_datetime()


@frappe.whitelist()
def make_entry(booking_no,mobile_no,paid_amount):
	due=frappe.new_doc('Due Payment')
	due.customer_mobile_number = mobile_no
	due.booking_id = booking_no
	due.paid_due_amount = paid_amount
	due.payment_made_on = frappe.utils.data.now_datetime()
	print('checking')
	due.save()
	due.submit()

@frappe.whitelist()
def get_alluser():
	time = frappe.utils.nowdate()
	print(time)
	a = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=',time] },['booking_id','name','customer_mobile_number','paid_due_amount'])
	print(a)
	return a 

@frappe.whitelist()
def delete_due(user_id):
	print(user_id)
	user_id = str(user_id)

	# frappe.db.sql(f"delete from `tabDue Payment` where name = {user_id}")
	frappe.db.delete('Due Payment',{'name' : str(user_id)})
	# ad=frappe.db.sql(f"""DELETE FROM `tabDue Payment` WHERE name = {user_id}""")
	#c=frappe.db.get_all('Due Payment',{'name' : user_id})
	a=frappe.db.count('Due Payment')
	print(a)
	return 'success'

@frappe.whitelist()
def user_validation():
	return "success"