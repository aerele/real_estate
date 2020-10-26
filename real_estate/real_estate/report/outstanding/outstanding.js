// Copyright (c) 2016, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Outstanding"] = {
	"filters": [
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 1,	
		},

		{
			"fieldname":"block",
			"label": __("Block"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 1,
			get_query :() => {
				var project = frappe.query_report.get_filter_value('project');
				console.log("Inside get_blocks");
				return {
					freeze : true,
					query : 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks_report',
					filters : {
						"project" : project,
					}
				}
			},

		},

		{
			"fieldname":"sites",
			"label": __("Sites"),
			"fieldtype": "Link",
			"options": "Site Booking",
			"reqd": 1,
			

		}
		
			
	]
};
