// Copyright (c) 2020, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Booking', {

	onload: function(frm) {
		frm.set_query("site", function() {
			return {
				filters: {
					"real_estate_project": frm.doc.project,
					"status": 'Open',
					"block_name" : frm.doc.block
				}
			}
		});
	},

	project : function(frm) {
		frappe.call({
			method: 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks',
			freeze: true,
			args: {
				project: frm.doc.project,	
			},
			callback: function(r) {
				
				if(r.message) {
					if(r.message.length > 1){
						frm.set_df_property('block','options',r.message)
					}
					else{
						frm.set_df_property('block','options',"None")
						frm.set_value('block',"None")
						frm.set_df_property("block",'read_only',1)
						frappe.call({
							method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites',
							freeze : true,
							args : {
								project: frm.doc.project,
								block : "None"
							},
							callback : function(r){
								if(r.message) {
									frm.set_df_property('site','options',r.message)
								}
							}
						})

					}
				}
			}
		});	
	},
	block : function(frm) {
		frappe.call({
			method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites',
			freeze : true,
			args : {
				project: frm.doc.project,
				block : frm.doc.block
			},
			callback : function(r){
				if(r.message) {
					frm.set_df_property('site','options',r.message)
				}
			}
		})
	}
});