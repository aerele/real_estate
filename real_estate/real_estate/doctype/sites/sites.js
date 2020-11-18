// Copyright (c) 2020, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sites', {
	real_estate_project : function(frm) {
		frappe.call({
			method: 'real_estate.real_estate.doctype.site_booking.site_booking.get_blocks',
			freeze: true,
			args: {
				project: frm.doc.real_estate_project,	
			},
			callback: function(r) {
				
				if(r.message) {
					if(r.message.length == 1){
						frm.set_value('block_name',"None")
					}
				}
					
				
			}
		});
	},
	
});
