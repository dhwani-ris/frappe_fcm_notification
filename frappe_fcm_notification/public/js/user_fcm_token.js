// User FCM Token JavaScript

frappe.ui.form.on('User FCM Token', {
	refresh: function(frm) {
		// Add refresh token button
		frm.add_custom_button(__('Refresh Token'), function() {
			frm.call({
				method: 'refresh_token',
				callback: function(r) {
					if (r.exc) {
						frappe.show_alert({
							message: __('Error refreshing token'),
							indicator: 'red'
						});
					} else {
						frappe.show_alert({
							message: __('Token refreshed successfully'),
							indicator: 'green'
						});
						frm.reload_doc();
					}
				}
			});
		}, __('Actions'));

		// Add activate/deactivate button
		if (frm.doc.is_token_active) {
			frm.add_custom_button(__('Deactivate'), function() {
				frm.call({
					method: 'deactivate_token',
					callback: function(r) {
						if (r.exc) {
							frappe.show_alert({
								message: __('Error deactivating token'),
								indicator: 'red'
							});
						} else {
							frappe.show_alert({
								message: __('Token deactivated successfully'),
								indicator: 'green'
							});
							frm.reload_doc();
						}
					}
				});
			}, __('Actions'));
		} else {
			frm.add_custom_button(__('Activate'), function() {
				frm.call({
					method: 'activate_token',
					callback: function(r) {
						if (r.exc) {
							frappe.show_alert({
								message: __('Error activating token'),
								indicator: 'red'
							});
						} else {
							frappe.show_alert({
								message: __('Token activated successfully'),
								indicator: 'green'
							});
							frm.reload_doc();
						}
					}
				});
			}, __('Actions'));
		}

		// Add test notification button
		frm.add_custom_button(__('Send Test Notification'), function() {
			frm.call({
				method: 'frappe_fcm_notification.api.fcm.send_test_notification',
				args: {
					token: frm.doc.fcm_token
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.show_alert({
							message: __('Test notification sent successfully!'),
							indicator: 'green'
						});
					} else {
						frappe.show_alert({
							message: __('Test notification failed: ') + (r.message ? r.message.error : 'Unknown error'),
							indicator: 'red'
						});
					}
				}
			});
		}, __('Actions'));
	},

	user: function(frm) {
		// Validate user when changed
		if (frm.doc.user) {
			frm.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'User',
					filters: { name: frm.doc.user },
					fieldname: ['enabled', 'full_name']
				},
				callback: function(r) {
					if (r.message) {
						if (!r.message.enabled) {
							frappe.show_alert({
								message: __('Selected user is disabled'),
								indicator: 'orange'
							});
						}
					}
				}
			});
		}
	},

	fcm_token: function(frm) {
		// Validate token format (basic validation)
		if (frm.doc.fcm_token) {
			if (frm.doc.fcm_token.length < 100) {
				frappe.show_alert({
					message: __('FCM token seems too short. Please verify the token.'),
					indicator: 'orange'
				});
			}
		}
	}
}); 