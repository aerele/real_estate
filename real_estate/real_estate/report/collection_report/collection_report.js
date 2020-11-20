// Copyright (c) 2016, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */
var flag;
frappe.query_reports["collection report"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date"
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.now_date(true)
		},
		{
			fieldname:"user",
			label: __("User"),
			fieldtype: "Link",
			options: "User",

		},
		{
			fieldname:"project",
			label: __("Project"),
			fieldtype: "Link",
			options : "Project",
			bold : 1,
			on_change: () => {
				var project = frappe.query_report.get_filter_value('project');
				frappe.call({
					method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks_report',
					freeze : true,
					args : {
					"project" : project,
					},
					callback: function(r) {
						if(r.message.length > 1) {
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
							flag = true;
						}
						else{
							frappe.query_report.set_filter_value('block',r.message);
						var project = frappe.query_report.get_filter_value('project');
						frappe.call({
							method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites_report',
							freeze : true,
							args : {
							"project" : project,
							"block" : "None"
							},
							callback: function(r) {
								if(r.message) {
									let status = r.message
									let options = []
									for(let option of status){
										options.push({
											"value":option,
											"description":""
										})
									}
									flag = false;
									var sites = frappe.query_report.get_filter('sites');
									sites.df.options = options;
									sites.refresh();
								}
							}
						});

						}
					}
				});
			}
		},
		{
			fieldname:"block",
			label: __("Block"),
			fieldtype: "MultiSelectList",
			bold : 1,
			on_change: () => {
				if (flag == true){
				   var project = frappe.query_report.get_filter_value('project');
				   var block = frappe.query_report.get_filter_value('block');
				   frappe.call({
					   method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites_report',
					   freeze : true,
					   args : {
					   "project" : project,
					   "block" : block
					   },
					   callback: function(r) {
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
				flag = true;
				
			   
		   }
		},
		{
			fieldname:"sites",
			label: __("Sites"),
			fieldtype: "MultiSelectList",
			bold : 1
		},


	]
};
