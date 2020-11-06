# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime 
from datetime import date, timedelta
from frappe.model.document import Document

class SiteBooking(Document):
	def on_cancel(self):
		site_key =  frappe.get_value('Sites',{'real_estate_project' :self.project,'block_name':self.block,'site_name': self.site},['name'])
		site = frappe.get_doc('Sites',site_key)
		site.price = ""
		site.status = "Open"
		site.save()

	def validate(self):
		if(self.starting_date and self.number_of_weeks):
			self.payment_deadline =  (datetime.datetime.strptime(str(self.starting_date ), "%Y-%m-%d") + datetime.timedelta(days = int(self.number_of_weeks)*7)).strftime("%d-%m-%Y")

	def on_submit(self):
		site_key =  frappe.get_value('Sites',{'real_estate_project' :self.project,'block_name':self.block,'site_name': self.site},['name'])
		site = frappe.get_doc('Sites',site_key)
		site.price = self.price
		if self.get_paid_amount() >= site.price:
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
def set_detail_to_app(site_name):
	a = frappe.db.get_value('Site Booking',{'name' : site_name },["customer_name","customer_mobile_number"])
	return a


@frappe.whitelist()
def get_sites_due_entry(project,block):
	site = []
	print(project,block)
	a = frappe.db.get_all('Sites',{'real_estate_project' : project,"block_name":block ,"status" :"Booked"},["site_name"])
	for data in a:
		site.append(data["site_name"])
	print(site)
	return sorted(set(site))


@frappe.whitelist()
def get_sites(project,block):
	site = []
	a = frappe.db.get_all('Sites',{'real_estate_project' : project,"block_name":block ,"status" :"Open"},["site_name"])
	for data in a:
		site.append(data["site_name"])
	return sorted(set(site))

	
@frappe.whitelist()
def get_blocks(project):
	block = []
	a = frappe.db.get_list('Sites',{'real_estate_project':project},['block_name'])
	for temp in a:
		block.append(temp['block_name'])
	return sorted(set(block))

@frappe.whitelist()
def get_blocks_report(project):
	block = []
	a = frappe.db.get_list('Sites',{'real_estate_project':project},['block_name'])
	for temp in a:
		block.append(temp['block_name'])
	return sorted(set(block))

@frappe.whitelist()
def get_sites_report(project,block):
	sites = []
	for data in block:
		a = frappe.db.get_list('Sites',{'real_estate_project':project,"block_name" : str(data)},['site_name'])
		for temp in a:
			sites.append(temp['site_name'])
	return sorted(set(sites))

@frappe.whitelist
def set_serial():
		site_bookings = frappe.db.get_all("Site Booking")
		for booking_id in site_bookings:
			booking_doc = frappe.get_doc("Site Booking", booking_id)
			if not booking_doc.serial:
				booking_doc.serial = make_autoname("YY.#####")
				booking_doc.save()
				
			

			



