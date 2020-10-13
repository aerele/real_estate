// Copyright (c) 2016, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */
var block_options = [];
frappe.query_reports["Outstanding"] = {
	"filters": [
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			on_change: () => {
				var project = frappe.query_report.get_filter_value('project');
				frappe.call({
				method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks_report',
				freeze : true,
				args : {
				"project" : project,
				},
				callback: function(r) {
					console.log(r.message)
					
				if(r.message) {
					frappe.query_report.set_filter_value('block',r.message)
					
					block_options = r.message
				}
				}
			});
			}
		},

		{
			"fieldname":"block",
			"label": __("Block"),
			"fieldtype": "Select",
			options:block_options
			// "options": ['asdjkf','sjdaf','asdknf'],
			// get_query :() => {
			// 	var project = frappe.query_report.get_filter_value('project');
			// 	console.log("Inside get_blocks");
			// 	return {
			// 		freeze : true,
			// 		query : 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks_report',
			// 		filters : {
			// 			"project" : project,
			// 		}
			// 	}
			// },

		},

		{
			"fieldname":"sites",
			"label": __("Sites"),
			"fieldtype": "Link",
			"options": "Site Booking",
			

		}
		
			
	]
};
// get_query :() => {
// 	var project = frappe.query_report.get_filter_value('project');
// 	console.log("Inside get_blocks");
// 	frappe.call({
// 	  query : 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks_report',
// 	  freeze : true,
// 	  filters : {
// 		"project" : project,
// 	  }
// 	  callback: function(r) {
// 		if(r.message) {
// 		  frm.set_df_property('block','options',r.message)
// 		}
// 	  }
// 	});
//   },