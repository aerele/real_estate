// Copyright (c) 2016, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Outstanding"] = {
	"filters": [
		{
			"fieldname":"mobile",
			"label": __("Mobile"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1,	
			"width":1000
		},

		{
			"fieldname":"sites",
			"label": __("Sites"),
			"fieldtype": "Link",
			"options": "Site Booking",
			"reqd": 1,
			
			get_query: () => {
				var customer = frappe.query_report.get_filter_value('mobile');
				return {
					 filters: {
					 'customer_mobile_number': customer.split('-')[1]
					}
				} 
			}

		}
		
			
	]
};
