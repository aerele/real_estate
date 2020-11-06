# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class DuePayment(Document):
	def validate(self):
		total = get_total(self.booking_id,self.paid_due_amount)
		self.balance = self.price - total



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

@frappe.whitelist()
def make_entry(booking_no,mobile_no,paid_amount):
	due = frappe.new_doc('Due Payment')
	due.customer_mobile_number = mobile_no
	due.booking_id = booking_no
	due.paid_due_amount = paid_amount
	due.payment_made_on = frappe.utils.data.now_datetime()
	due.save()
	due.submit()

@frappe.whitelist()
def get_alluser(api):
	user = frappe.db.get_value("User",{"api_key":api},["name"])
	time = frappe.utils.nowdate()
	a = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=',time],'modified_by': user },['booking_id','name','customer_mobile_number','paid_due_amount'])
	return a 

@frappe.whitelist()
def delete_due(user_id):
	user_id = str(user_id)
	frappe.db.delete('Due Payment',{'name' : str(user_id)})
	a = frappe.db.count('Due Payment')
	return 'success'

@frappe.whitelist()
def user_validation():
	return "success"

@frappe.whitelist()
def find_due(due_key):
	book_id = frappe.db.get_value("Due Payment",{"name":due_key},["booking_id"])
	site_record = frappe.db.get_value("Site Booking",{"name":book_id},["name","customer_name","customer_mobile_number"])
	return site_record