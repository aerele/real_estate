// Copyright (c) 2020, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Due Payment', {
	onload: function(frm) {
		frm.set_query("booking_id", function() {
			return {
				filters: {
					"customer_mobile_number": frm.doc.customer_mobile_number
				}
			}
		});
	}
});
