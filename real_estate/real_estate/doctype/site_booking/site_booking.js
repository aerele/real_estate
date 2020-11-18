// Copyright (c) 2020, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

var site_array = [];
frappe.ui.form.on('Site Booking', {
	
	onload: function(frm) {
		
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
									site_array = r.message
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
					site_array = r.message
					frm.set_df_property('site','options',r.message)


					
				}
			}
		})
	},
	enable_mutiplesite : function(frm) {
		if(frm.doc.enable_mutiplesite == 1){
			frm.set_df_property("site","hidden",1),
			frm.set_df_property("sites","hidden",0),
			frappe.call({
				method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites',
				freeze : true,
				args : {
					project: frm.doc.project,
					block : frm.doc.block
				},
				callback : function(r){
					if(r.message) {
						site_array = r.message
						frappe.meta.get_docfield("Multi Site Table", "sites", frm.doc.name).options = r.message
	
					}
				}
			});

		}
		else{
			frm.set_df_property("site","hidden",0),
			frm.set_df_property("sites","hidden",1),
			frm.set_df_property('site','options',site_array)


		}
		

	},
});