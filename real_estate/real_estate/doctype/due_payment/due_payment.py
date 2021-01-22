# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class DuePayment(Document):
	def validate(self):
		if (self.payment_made_on == None):
			self.payment_made_on = frappe.utils.data.now_datetime()
		if (self.balance == None):
			total = get_total(self.booking_id)
			past_balance = (self.price - total)
			self.balance = past_balance - self.paid_due_amount
		pass




def get_total(booking_id):
		due_record = frappe.db.get_all("Due Payment",{"booking_id":booking_id,"docstatus":1},["paid_due_amount"])
		total = 0
		for record in due_record:
			total += record["paid_due_amount"]
		return total

@frappe.whitelist()
def get_customer_details(project,block,site):
		customer_data = frappe.db.get_value("Site Booking",{"project" : project,"block" : block, "site" : site},["serial","name","customer_name","customer_mobile_number","price","payment_deadline"]) 
		return customer_data

@frappe.whitelist()
def make_entry(serial,customer_name,mobile_no,paid_amount):
	
	due = frappe.new_doc('Due Payment')
	due.customer_name = frappe.db.get_value('Site Booking',{'serial' : serial},['customer_name'])
	site_price = frappe.db.get_value('Site Booking',{'serial' : serial},['price'])
	booking_no = frappe.db.get_value('Site Booking',{'serial': serial},['name'])
	due.price = site_price
	total = get_total(booking_no)
	due.balance = (site_price - total) - float(paid_amount)
	due.customer_mobile_number = frappe.db.get_value('Site Booking',{'serial' : serial},['customer_mobile_number'])
	due.booking_id = booking_no
	due.serial = serial
	due.paid_due_amount = paid_amount
	due.deadline = frappe.db.get_value('Site Booking',{'serial':serial},['payment_deadline'])
	due.payment_made_on = frappe.utils.data.now_datetime()
	due.save()
	due.submit()
	return due.name

@frappe.whitelist()
def get_alluser(api):
	user = frappe.db.get_value("User",{"api_key":api},["name"])
	time = frappe.utils.nowdate()
	all_due = frappe.db.get_all('Due Payment',{'payment_made_on': ['>=',time],'modified_by': user ,"docstatus" : 1},['serial','booking_id','name','customer_name','customer_mobile_number','paid_due_amount'])
	for due in all_due:
		due['paid_due_amount'] = int(due['paid_due_amount'])
	for due in all_due:
		due["project"] = frappe.db.get_value("Site Booking",{"serial" : due.serial},["project"])
		due["block"] = frappe.db.get_value("Site Booking",{"serial" : due.serial},["block"])
		due["site"] = frappe.db.get_value("Site Booking",{"serial" : due.serial},["site"])
	return all_due 

@frappe.whitelist()
def delete_due(user_id):
	user_id = str(user_id)
	currect_record =  frappe.get_doc("Due Payment",{'name':str(user_id)})
	currect_record.cancel()
	return 'success'

@frappe.whitelist()
def validate(serial,customer_name,mobile_no,project,site,block):
	if frappe.db.exists("Site Booking",{"serial":serial,"customer_name":customer_name,"project":project,"block":block,"site":site,"customer_mobile_number":mobile_no}): 
		return True
	return False

@frappe.whitelist()
def user_validation():
	return "success"

@frappe.whitelist()
def find_due(due_key):
	book_id = frappe.db.get_value("Due Payment",{"name":due_key},["booking_id"])
	site_record = frappe.db.get_value("Site Booking",{"name":book_id},["name","customer_name","customer_mobile_number"])
	return site_record