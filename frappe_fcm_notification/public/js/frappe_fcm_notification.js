// Frappe FCM Notification Main JavaScript

// Global FCM App Object
window.FCMApp = {
	// Initialize the app
	init: function() {
		this.setupEventListeners();
		this.loadDashboardStats();
	},
	
	// Setup event listeners
	setupEventListeners: function() {
		// Listen for notification events
		$(document).on('click', '.fcm-send-notification', function() {
			FCMApp.sendNotification($(this).data('notification-id'));
		});
		
		$(document).on('click', '.fcm-retry-notification', function() {
			FCMApp.retryNotification($(this).data('notification-id'));
		});
		
		$(document).on('click', '.fcm-cancel-notification', function() {
			FCMApp.cancelNotification($(this).data('notification-id'));
		});
	},
	
	// Load dashboard statistics
	loadDashboardStats: function() {
		if ($('.fcm-dashboard').length) {
			frappe.call({
				method: 'frappe_fcm_notification.api.fcm.get_dashboard_stats',
				callback: function(r) {
					if (r.message) {
						FCMApp.updateDashboardStats(r.message);
					}
				}
			});
		}
	},
	
	// Update dashboard statistics
	updateDashboardStats: function(stats) {
		$('.fcm-stat-sent .fcm-stat-number').text(stats.sent_count || 0);
		$('.fcm-stat-failed .fcm-stat-number').text(stats.failed_count || 0);
		$('.fcm-stat-active-tokens .fcm-stat-number').text(stats.active_tokens || 0);
		$('.fcm-stat-success-rate .fcm-stat-number').text((stats.success_rate || 0) + '%');
	},
	
	// Send notification
	sendNotification: function(notificationId) {
		frappe.call({
			method: 'frappe_fcm_notification.events.push_notification_events.send_notification',
			args: { docname: notificationId },
			callback: function(r) {
				if (r.exc) {
					frappe.show_alert({
						message: __('Error sending notification'),
						indicator: 'red'
					});
				} else {
					frappe.show_alert({
						message: __('Notification sent successfully'),
						indicator: 'green'
					});
					// Reload the page or update the UI
					setTimeout(function() {
						location.reload();
					}, 1000);
				}
			}
		});
	},
	
	// Retry failed notification
	retryNotification: function(notificationId) {
		frappe.call({
			method: 'frappe_fcm_notification.events.push_notification_events.retry_notification',
			args: { docname: notificationId },
			callback: function(r) {
				if (r.exc) {
					frappe.show_alert({
						message: __('Error retrying notification'),
						indicator: 'red'
					});
				} else {
					frappe.show_alert({
						message: __('Notification retry initiated'),
						indicator: 'green'
					});
					setTimeout(function() {
						location.reload();
					}, 1000);
				}
			}
		});
	},
	
	// Cancel scheduled notification
	cancelNotification: function(notificationId) {
		frappe.call({
			method: 'frappe_fcm_notification.events.push_notification_events.cancel_notification',
			args: { docname: notificationId },
			callback: function(r) {
				if (r.exc) {
					frappe.show_alert({
						message: __('Error cancelling notification'),
						indicator: 'red'
					});
				} else {
					frappe.show_alert({
						message: __('Notification cancelled successfully'),
						indicator: 'green'
					});
					setTimeout(function() {
						location.reload();
					}, 1000);
				}
			}
		});
	},
	
	// Test Firebase connection
	testFirebaseConnection: function() {
		frappe.call({
			method: 'frappe_fcm_notification.api.fcm.test_firebase_connection',
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
	},
	
	// Send test notification
	sendTestNotification: function(token) {
		if (!token) {
			frappe.show_alert({
				message: __('Please provide a valid FCM token'),
				indicator: 'red'
			});
			return;
		}
		
		frappe.call({
			method: 'frappe_fcm_notification.api.fcm.send_test_notification',
			args: { token: token },
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
	},
	
	// Save FCM token (for mobile apps)
	saveFCMToken: function(token, deviceType) {
		frappe.call({
			method: 'frappe_fcm_notification.api.fcm.save_fcm_token',
			args: {
				token: token,
				device_type: deviceType || 'Web'
			},
			callback: function(r) {
				if (r.message && r.message.success) {
					console.log('FCM token saved successfully');
				} else {
					console.error('Error saving FCM token:', r.message ? r.message.error : 'Unknown error');
				}
			}
		});
	},
	
	// Get user tokens
	getUserTokens: function() {
		frappe.call({
			method: 'frappe_fcm_notification.api.fcm.get_user_tokens',
			callback: function(r) {
				if (r.message && r.message.success) {
					return r.message.tokens;
				}
				return [];
			}
		});
	},
	
	// Delete FCM token
	deleteFCMToken: function(token) {
		frappe.call({
			method: 'frappe_fcm_notification.api.fcm.delete_fcm_token',
			args: { token: token },
			callback: function(r) {
				if (r.message && r.message.success) {
					console.log('FCM token deleted successfully');
				} else {
					console.error('Error deleting FCM token:', r.message ? r.message.error : 'Unknown error');
				}
			}
		});
	}
};

// Initialize when document is ready
$(document).ready(function() {
	FCMApp.init();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
	module.exports = FCMApp;
} 