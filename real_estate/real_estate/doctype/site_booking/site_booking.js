// Copyright (c) 2020, Aerele Technologies Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Booking', {
	onload: function(frm) {
		frm.set_query("site", function() {
			return {
				filters: {
					"real_estate_project": frm.doc.project,
					"status": 'Open'
				}
			}
		});
	}
});