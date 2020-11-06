// Copyright (c) 2020, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Due Payment', {
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
						frm.set_df_property("block",'read_only',0)
						frm.set_df_property('block','options',r.message)
					}
					else{
						frm.set_df_property('block','options',"None")
						frm.set_value('block',"None")
						frm.set_df_property("block",'read_only',1)
						frappe.call({
							method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites_due_entry',
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
			method : 'real_estate.real_estate.doctype.site_booking.site_booking.get_sites_due_entry',
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
	}, 
	site : function(frm) {
		frappe.call({
			method : 'real_estate.real_estate.doctype.due_payment.due_payment.get_customer_details',
			freeze : true,
			args : {
				project: frm.doc.project,
				block : frm.doc.block,
				site : frm.doc.site
			},
			callback : function(r){
				if(r.message){
					
					frm.set_value("customer_name",r.message[0]);
					frm.set_value("customer_mobile_number",r.message[1]);
					frm.set_value("price",r.message[2]);
					frm.set_value("deadline",r.message[3]);
					frm.set_value("booking_id",r.message[4]);
				}
			}
		})

	}
});
