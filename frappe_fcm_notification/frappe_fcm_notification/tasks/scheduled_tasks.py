# -*- coding: utf-8 -*-

import frappe
from frappe.utils import now_datetime, add_days
from frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events import send_notification

def all():
	"""Run every minute"""
	pass

def daily():
	"""Run daily tasks"""
	cleanup_expired_tokens()

def hourly():
	"""Run hourly tasks"""
	pass

def process_scheduled_notifications():
	"""Process scheduled notifications (runs every 5 minutes)"""
	try:
		# Get scheduled notifications that are due
		scheduled_notifications = frappe.get_all(
			"Push Notification Manager",
			filters={
				"status": "Scheduled",
				"scheduled_datetime": ["<=", now_datetime()],
				"notification_type": "Scheduled"
			},
			fields=["name"]
		)
		
		for notification in scheduled_notifications:
			try:
				doc = frappe.get_doc("Push Notification Manager", notification.name)
				send_notification(doc)
				frappe.db.commit()
			except Exception as e:
				frappe.log_error(f"Error processing scheduled notification {notification.name}: {str(e)}")
				
	except Exception as e:
		frappe.log_error(f"Error in process_scheduled_notifications: {str(e)}")

def cleanup_expired_tokens():
	"""Clean up expired/invalid FCM tokens (runs daily)"""
	try:
		# Mark tokens as inactive if they haven't been updated in 30 days
		thirty_days_ago = add_days(now_datetime(), -30)
		
		expired_tokens = frappe.get_all(
			"User FCM Token",
			filters={
				"token_last_updated": ["<", thirty_days_ago],
				"is_token_active": 1
			},
			fields=["name"]
		)
		
		for token in expired_tokens:
			try:
				token_doc = frappe.get_doc("User FCM Token", token.name)
				token_doc.is_token_active = 0
				token_doc.save()
			except Exception as e:
				frappe.log_error(f"Error cleaning up token {token.name}: {str(e)}")
		
		frappe.db.commit()
		
		# Log cleanup summary
		if expired_tokens:
			frappe.logger().info(f"Cleaned up {len(expired_tokens)} expired FCM tokens")
			
	except Exception as e:
		frappe.log_error(f"Error in cleanup_expired_tokens: {str(e)}")

def retry_failed_notifications():
	"""Retry failed notifications (runs every 15 minutes)"""
	try:
		# Get failed notifications that can be retried
		failed_notifications = frappe.get_all(
			"Push Notification Manager",
			filters={
				"status": "Failed",
				"modified": [">=", add_days(now_datetime(), -1)]  # Only retry recent failures
			},
			fields=["name"]
		)
		
		for notification in failed_notifications:
			try:
				doc = frappe.get_doc("Push Notification Manager", notification.name)
				
				# Check if it's a scheduled notification that's still due
				if doc.notification_type == "Scheduled" and doc.scheduled_datetime <= now_datetime():
					send_notification(doc)
					frappe.db.commit()
					
			except Exception as e:
				frappe.log_error(f"Error retrying notification {notification.name}: {str(e)}")
				
	except Exception as e:
		frappe.log_error(f"Error in retry_failed_notifications: {str(e)}")

def validate_fcm_tokens():
	"""Validate FCM tokens and mark invalid ones as inactive"""
	try:
		from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
		
		# Get active tokens
		active_tokens = frappe.get_all(
			"User FCM Token",
			filters={"is_token_active": 1},
			fields=["name", "fcm_token"]
		)
		
		firebase_client = get_firebase_client()
		
		for token in active_tokens:
			try:
				is_valid = firebase_client.validate_token(token.fcm_token)
				if not is_valid:
					token_doc = frappe.get_doc("User FCM Token", token.name)
					token_doc.is_token_active = 0
					token_doc.save()
					frappe.logger().info(f"Marked invalid token {token.name} as inactive")
			except Exception as e:
				frappe.log_error(f"Error validating token {token.name}: {str(e)}")
		
		frappe.db.commit()
		
	except Exception as e:
		frappe.log_error(f"Error in validate_fcm_tokens: {str(e)}") 