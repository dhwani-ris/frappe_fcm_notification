// Push Notification Manager JavaScript

frappe.ui.form.on('Push Notification Manager', {
	refresh: function(frm) {
		// Add custom buttons based on status
		if (frm.doc.status === 'Draft') {
			frm.add_custom_button(__('Send Now'), function() {
				frm.call({
					method: 'send_notification',
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					callback: function(r) {
						if (r.exc) {
							frappe.show_alert({
								message: __('Error sending notification'),
								indicator: 'red'
							});
						} else {
							frm.reload_doc();
						}
					}
				});
			}, __('Actions'));
		}

		if (frm.doc.status === 'Failed') {
			frm.add_custom_button(__('Retry'), function() {
				frm.call({
					method: 'retry_failed_notification',
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					callback: function(r) {
						if (r.exc) {
							frappe.show_alert({
								message: __('Error retrying notification'),
								indicator: 'red'
							});
						} else {
							frm.reload_doc();
						}
					}
				});
			}, __('Actions'));
		}

		if (frm.doc.status === 'Scheduled') {
			frm.add_custom_button(__('Cancel'), function() {
				frm.call({
					method: 'cancel_scheduled_notification',
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					callback: function(r) {
						if (r.exc) {
							frappe.show_alert({
								message: __('Error cancelling notification'),
								indicator: 'red'
							});
						} else {
							frm.reload_doc();
						}
					}
				});
			}, __('Actions'));
		}

		// Add delivery stats button
		if (frm.doc.status === 'Sent' || frm.doc.status === 'Failed') {
			frm.add_custom_button(__('View Stats'), function() {
				frm.call({
					method: 'get_delivery_stats',
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							let stats = r.message;
							frappe.msgprint({
								title: __('Delivery Statistics'),
								message: __(`
									<div class="row">
										<div class="col-md-3">
											<div class="text-center">
												<h4>${stats.sent_count}</h4>
												<p>Sent</p>
											</div>
										</div>
										<div class="col-md-3">
											<div class="text-center">
												<h4>${stats.failed_count}</h4>
												<p>Failed</p>
											</div>
										</div>
										<div class="col-md-3">
											<div class="text-center">
												<h4>${stats.total_count}</h4>
												<p>Total</p>
											</div>
										</div>
										<div class="col-md-3">
											<div class="text-center">
												<h4>${stats.success_rate}%</h4>
												<p>Success Rate</p>
											</div>
										</div>
									</div>
								`),
								indicator: stats.success_rate > 80 ? 'green' : 'orange'
							});
						}
					}
				});
			}, __('Actions'));
		}
	},

	target_type: function(frm) {
		// Show/hide fields based on target type
		frm.toggle_display('target_roles', frm.doc.target_type === 'By Role');
		frm.toggle_display('target_users', frm.doc.target_type === 'Specific Users');
		frm.toggle_display('custom_filter', frm.doc.target_type === 'Custom Filter');
	},

	notification_type: function(frm) {
		// Show/hide scheduled datetime field
		frm.toggle_display('scheduled_datetime', frm.doc.notification_type === 'Scheduled');
	},

	scheduled_datetime: function(frm) {
		// Validate scheduled datetime
		if (frm.doc.scheduled_datetime && frm.doc.notification_type === 'Scheduled') {
			let scheduled = new Date(frm.doc.scheduled_datetime);
			let now = new Date();
			
			if (scheduled <= now) {
				frappe.show_alert({
					message: __('Scheduled DateTime must be in the future'),
					indicator: 'red'
				});
			}
		}
	}
});

// Child table events for target roles
frappe.ui.form.on('Push Notification Target Role', {
	target_roles_add: function(frm, cdt, cdn) {
		// Auto-fetch roles
		frm.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'Role',
				fields: ['name'],
				limit: 100
			},
			callback: function(r) {
				if (r.message) {
					let roles = r.message.map(role => role.name);
					// You can populate a dropdown or suggest roles here
				}
			}
		});
	}
});

// Child table events for target users
frappe.ui.form.on('Push Notification Target User', {
	target_users_add: function(frm, cdt, cdn) {
		// Auto-fetch users
		frm.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'User',
				filters: { enabled: 1 },
				fields: ['name', 'full_name'],
				limit: 100
			},
			callback: function(r) {
				if (r.message) {
					let users = r.message;
					// You can populate a dropdown or suggest users here
				}
			}
		});
	}
}); 