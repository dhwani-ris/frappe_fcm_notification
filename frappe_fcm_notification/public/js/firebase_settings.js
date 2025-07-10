// Firebase Settings JavaScript

frappe.ui.form.on('Firebase Settings', {
	refresh: function(frm) {
		// Add test connection button
		frm.add_custom_button(__('Test Connection'), function() {
			frm.call({
				method: 'test_connection',
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.show_alert({
							message: __('Firebase connection successful!'),
							indicator: 'green'
						});
					} else {
						frappe.show_alert({
							message: __('Firebase connection failed: ') + (r.message ? r.message.error : 'Unknown error'),
							indicator: 'red'
						});
					}
				}
			});
		}, __('Actions'));

		// Add test notification button
		frm.add_custom_button(__('Send Test Notification'), function() {
			frappe.prompt({
				fieldtype: 'Small Text',
				label: __('FCM Token'),
				description: __('Enter a valid FCM token to send a test notification'),
				reqd: 1,
				fieldname: 'fcm_token'
			}, function(values) {
				frm.call({
					method: 'send_test_notification',
					args: {
						token: values.fcm_token
					},
					callback: function(r) {
						if (r.message && r.message.success) {
							frappe.show_alert({
								message: __('Test notification sent successfully!'),
								indicator: 'green'
							});
							console.log("r", r)
						} else {
							frappe.show_alert({
								message: __('Test notification failed: ') + (r.message ? r.message.error : 'Unknown error'),
								indicator: 'red'
							});
						}
					}
				});
			}, __('Cancel'), __('Send Test'));
		}, __('Actions'));
	},

	service_account_json: function(frm) {
		// Validate JSON file when uploaded
		if (frm.doc.service_account_json) {
			frm.call({
				method: 'validate_service_account_json',
				callback: function(r) {
					if (r.exc) {
						frappe.show_alert({
							message: __('Invalid service account JSON file'),
							indicator: 'red'
						});
					}
				}
			});
		}
	}
}); 