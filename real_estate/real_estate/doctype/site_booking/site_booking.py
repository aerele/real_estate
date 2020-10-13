# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SiteBooking(Document):
	def on_submit(self):
		site_key =  frappe.get_value('Sites',{'real_estate_project' :self.project,'block_name':self.block,'site_name': self.site},['name'])
		print(site_key)
		site = frappe.get_doc('Sites',site_key)
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
			due.payment_made_on = payment_entry.date
			due.save()
			due.submit()
@frappe.whitelist()
def get_site(site_name):
	print(site_name)
	site_name =  str(site_name)
	a=frappe.db.get_all('Site Booking',{'name' : site_name},['customer_name','customer_mobile_number'])
	print(a)
	return a
@frappe.whitelist()
def get_blocks(project):
	block = []
	print('checkin get')
	a = frappe.db.get_list('Sites',{'real_estate_project':project},['block_name'])
	for temp in a:
		block.append(temp['block_name'])
	print(block)
	return sorted(set(block))

@frappe.whitelist()
def get_blocks_report(project):
	block = []
	print('checkin get')
	# print(filters)
	a = frappe.db.get_list('Sites',{'real_estate_project':project},['block_name'])
	for temp in a:
		block.append(temp['block_name'])
	print(block)
	return sorted(set(block))

@frappe.whitelist()
def get_sites(project,block):
	sites = []
	a = frappe.db.get_list('Sites',{'real_estate_project':project,"block_name" : block},['site_name'])
	for temp in a:
		sites.append(temp['site_name'])
	return sorted(set(sites))

@frappe.whitelist()
def new_try(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select block_name from `tabSites` where real_estate_project='{0}'""".format(filters['project']))
	


