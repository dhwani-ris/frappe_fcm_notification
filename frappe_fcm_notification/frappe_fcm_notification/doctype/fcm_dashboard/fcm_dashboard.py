# -*- coding: utf-8 -*-

import frappe
from frappe import _

def get_context(context):
	"""Get context for the FCM Dashboard page"""
	context.title = _("FCM Dashboard")
	context.no_cache = 1
	
	# Get statistics
	context.stats = get_fcm_statistics()
	
	# Get recent notifications
	context.recent_notifications = get_recent_notifications()
	
	# Get active tokens count
	context.active_tokens = get_active_tokens_count()
	
	# Get Firebase status
	context.firebase_status = get_firebase_status()

def get_fcm_statistics():
	"""Get FCM statistics"""
	stats = {}
	
	# Total notifications
	stats['total_notifications'] = frappe.db.count('Push Notification Manager')
	
	# Sent notifications
	stats['sent_notifications'] = frappe.db.count('Push Notification Manager', {'status': 'Sent'})
	
	# Failed notifications
	stats['failed_notifications'] = frappe.db.count('Push Notification Manager', {'status': 'Failed'})
	
	# Scheduled notifications
	stats['scheduled_notifications'] = frappe.db.count('Push Notification Manager', {'status': 'Scheduled'})
	
	# Draft notifications
	stats['draft_notifications'] = frappe.db.count('Push Notification Manager', {'status': 'Draft'})
	
	# Success rate
	total_sent = stats['sent_notifications'] + stats['failed_notifications']
	stats['success_rate'] = round((stats['sent_notifications'] / total_sent * 100) if total_sent > 0 else 0, 2)
	
	return stats

def get_recent_notifications():
	"""Get recent notifications"""
	return frappe.get_all(
		'Push Notification Manager',
		fields=['name', 'notification_title', 'status', 'sent_count', 'failed_count', 'created', 'sent_date'],
		order_by='creation desc',
		limit=10
	)

def get_active_tokens_count():
	"""Get count of active FCM tokens"""
	return frappe.db.count('User FCM Token', {'is_token_active': 1})

def get_firebase_status():
	"""Get Firebase connection status"""
	try:
		firebase_settings = frappe.get_single('Firebase Settings')
		return {
			'is_active': firebase_settings.is_active,
			'project_name': firebase_settings.project_name,
			'project_id': firebase_settings.project_id,
			'has_credentials': bool(firebase_settings.service_account_json)
		}
	except:
		return {
			'is_active': False,
			'project_name': None,
			'project_id': None,
			'has_credentials': False
		} 