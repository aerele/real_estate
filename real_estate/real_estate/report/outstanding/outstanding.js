// Copyright (c) 2016, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */
var  block_options = [];
frappe.query_reports["Outstanding"] = {
	
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
							let status = r.message
							let options = []
							for(let option of status){
								options.push({
									"value":option,
									"description":""
								})
							}
							var block = frappe.query_report.get_filter('block');
							block.df.options = options;
							block.refresh();
						}
					}
				});
			}
		},

		{
			"fieldname":"block",
			"label": __("Block"),
			"fieldtype": "MultiSelectList",
			
			 on_change: () => {
				console.log("inside block");
				var project = frappe.query_report.get_filter_value('project');
				var block = frappe.query_report.get_filter_value('block');
				console.log(block)
				frappe.call({
					method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites_report',
					freeze : true,
					args : {
					"project" : project,
					"block" : block
					},
					callback: function(r) {
						console.log(r.message)
						if(r.message) {
							let status = r.message
							let options = []
							for(let option of status){
								options.push({
									"value":option,
									"description":""
								})
							}
							var sites = frappe.query_report.get_filter('sites');
							sites.df.options = options;
							sites.refresh();
						}
					}
				});
			}

		},

		{
			
			"fieldname":"sites",
			"label": __("Sites"),
			"fieldtype": "MultiSelectList",
			"bold":1,

		},
		{
			
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options":"Customer",
			"bold":1,
			

		}
		
			
	],
	
}
