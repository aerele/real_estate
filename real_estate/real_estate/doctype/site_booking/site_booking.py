# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime 
from datetime import date, timedelta
from frappe.model.naming import make_autoname
from frappe.model.document import Document


class SiteBooking(Document):
	def autoname(self):
		if self.enable_mutiplesite == 1:
			new_site = []
			for site in self.sites:
				new_site.append(site.sites)
			new_site_name = ",".join(new_site)
			self.site = str(new_site_name)
		self.serial = make_autoname("YY.#####")

	def on_cancel(self):
		if self.enable_mutiplesite == 1:
			split_site = self.site.split(",")
			for _site in split_site:
				site_doc = frappe.new_doc("Sites")
				site_doc.real_estate_project = self.project
				site_doc.block_name =  self.block
				site_doc.site_name =  str(_site)
				site_doc.save()
			frappe.db.delete("Sites",{"real_estate_project" : self.project,'block_name':self.block,'site_name': self.site})
		else:
			site_key =  frappe.get_value('Sites',{'real_estate_project' :self.project,'block_name':self.block,'site_name': self.site},['name'])
			site = frappe.get_doc('Sites',site_key)
			site.price = ""
			site.status = "Open"
			site.save()

	def validate(self):
		if(self.starting_date and self.number_of_weeks):
			self.payment_deadline =  (datetime.datetime.strptime(str(self.starting_date ), "%Y-%m-%d") + datetime.timedelta(days = int(self.number_of_weeks)*7)).strftime("%d-%m-%Y")
	
	def on_submit(self):
		if self.enable_mutiplesite == 1 :
			new_site = []
			for site in self.sites:
				new_site.append(site.sites)
			new_site_name = ",".join(new_site)
			site_doc = frappe.new_doc("Sites")
			site_doc.real_estate_project = self.project
			site_doc.block_name =  self.block
			site_doc.site_name =  str(new_site_name)
			site_doc.save()
			for _site in new_site:
				frappe.db.delete("Sites",{"real_estate_project" : self.project,'block_name':self.block,'site_name': _site})

		
		
		site_key =  frappe.get_value('Sites',{'real_estate_project' :self.project,'block_name':self.block,'site_name': self.site},['name'])
		site = frappe.get_doc('Sites',site_key)
		site.price = self.price
		site.status = "Agreement"
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
			due.serial = self.serial
			due.customer_name = self.customer_name
			due.price = self.price
			due.customer_mobile_number = self.customer_mobile_number
			due.booking_id = self.name
			due.paid_due_amount = payment_entry.amount
			due.payment_made_on = payment_entry.date
			due.deadline = self.payment_deadline
			due.save()
			due.submit()


@frappe.whitelist()
def set_detail_to_app(site_name):
	a = frappe.db.get_value('Site Booking',{'serial' : site_name },["customer_name","customer_mobile_number"])
	return a


@frappe.whitelist()
def get_sites_due_entry(project,block):
	site = []
	a = frappe.db.get_all('Sites',{'real_estate_project' : project,"block_name":block ,"status" :"Agreement"},["site_name"])
	for data in a:
		site.append(data["site_name"])
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
	if (block == "None"):
		a = frappe.db.get_list('Sites',{'real_estate_project':project,"block_name" : "None"},['site_name'])
		for temp in a:
			sites.append(temp['site_name'])
	else:
		for data in block:
			a = frappe.db.get_list('Sites',{'real_estate_project':project,"block_name" : str(data)},['site_name'])
			for temp in a:
				sites.append(temp['site_name'])
	return sorted(set(sites))


@frappe.whitelist()
def set_serial():
	site_bookings = frappe.db.get_all("Site Booking")
	for booking_id in site_bookings:
		booking_doc = frappe.get_doc("Site Booking", booking_id['name'])
		if not booking_doc.serial and not booking_doc.docstaus == 2:
			booking_doc.serial = make_autoname("YY.#####")
			booking_doc.save()
	return "success"

@frappe.whitelist()
def set_serial_due_payment():
	due_payment = frappe.db.get_all("Due Payment")
	for booking_id in due_payment:
		due_booking_doc = frappe.get_doc("Due Payment", booking_id['name'])
		if not due_booking_doc.serial and  not booking_doc.docstaus == 2:
			get_serial = frappe.db.get_value("Site Booking",{ "name" :due_booking_doc.booking_id},["serial"])
			due_booking_doc.serial = get_serial
			due_booking_doc.save()
		if not due_booking_doc.customer_name and  not booking_doc.docstaus == 2:
			get_customer = frappe.db.get_value("Site Booking",{"name" : due_booking_doc.booking_id},["customer_name"])
			due_booking_doc.customer_name = get_customer
			due_booking_doc.save()
		if not due_booking_doc.price and  not booking_doc.docstaus == 2:
			get_price = frappe.db.get_value("Site Booking",{"name" : due_booking_doc.price},["price"])
			due_booking_doc.price = get_price
			due_booking_doc.save()
	return "success"

			



