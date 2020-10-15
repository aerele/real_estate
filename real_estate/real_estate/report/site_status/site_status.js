// Copyright (c) 2016, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Site Status"] = {
	"filters": [
		{	
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"bold":1,
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
							var block = frappe.query_report.get_filter('block');
							block.df.options = r.message;
							block.refresh();
						}
					}
				});
			}
		},
		{
			"fieldname":"block",
			"label": __("Block"),
			"fieldtype": "Select",
			"bold":1,
		}


	]
};
