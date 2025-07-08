# -*- coding: utf-8 -*-

import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client

@frappe.whitelist()
def save_fcm_token(token, device_type="Web", user=None):
	"""Save FCM token for a user (whitelisted API for mobile apps)"""
	try:
		if not token:
			return {"success": False, "error": "Token is required"}
		
		if not user:
			user = frappe.session.user
		
		# Check if token already exists
		existing_token = frappe.db.exists("User FCM Token", {
			"fcm_token": token,
			"user": user
		})
		
		if existing_token:
			# Update existing token
			token_doc = frappe.get_doc("User FCM Token", existing_token)
			token_doc.token_last_updated = now_datetime()
			token_doc.device_type = device_type
			token_doc.is_token_active = 1
			token_doc.save()
		else:
			# Create new token
			token_doc = frappe.get_doc({
				"doctype": "User FCM Token",
				"user": user,
				"fcm_token": token,
				"device_type": device_type,
				"token_created_date": now_datetime(),
				"token_last_updated": now_datetime(),
				"is_token_active": 1
			})
			token_doc.insert()
		
		frappe.db.commit()
		return {"success": True, "message": "Token saved successfully"}
		
	except Exception as e:
		frappe.log_error(f"Error saving FCM token: {str(e)}")
		return {"success": False, "error": str(e)}

@frappe.whitelist()
def test_firebase_connection():
	"""Test Firebase connection (whitelisted API)"""
	try:
		firebase_client = get_firebase_client()
		result = firebase_client.test_connection()
		return result
	except Exception as e:
		frappe.log_error(f"Firebase connection test failed: {str(e)}")
		return {"success": False, "error": str(e)}

@frappe.whitelist()
def send_test_notification(token):
	"""Send test notification to a specific token (whitelisted API)"""
	try:
		if not token:
			return {"success": False, "error": "Token is required"}
		
		firebase_client = get_firebase_client()
		result = firebase_client.send_single_notification(
			token=token,
			title="Test Notification",
			body="This is a test notification from Frappe FCM",
			data={"type": "test", "timestamp": str(now_datetime())}
		)
		return result
	except Exception as e:
		frappe.log_error(f"Test notification failed: {str(e)}")
		return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_user_tokens(user=None):
	"""Get active FCM tokens for a user"""
	try:
		if not user:
			user = frappe.session.user
		
		tokens = frappe.get_all(
			"User FCM Token",
			filters={"user": user, "is_token_active": 1},
			fields=["fcm_token", "device_type", "token_created_date"]
		)
		
		return {"success": True, "tokens": tokens}
	except Exception as e:
		frappe.log_error(f"Error getting user tokens: {str(e)}")
		return {"success": False, "error": str(e)}

@frappe.whitelist()
def delete_fcm_token(token):
	"""Delete FCM token (whitelisted API)"""
	try:
		if not token:
			return {"success": False, "error": "Token is required"}
		
		user = frappe.session.user
		
		# Find and delete the token
		token_doc = frappe.get_doc("User FCM Token", {
			"fcm_token": token,
			"user": user
		})
		
		if token_doc:
			token_doc.delete()
			frappe.db.commit()
			return {"success": True, "message": "Token deleted successfully"}
		else:
			return {"success": False, "error": "Token not found"}
			
	except Exception as e:
		frappe.log_error(f"Error deleting FCM token: {str(e)}")
		return {"success": False, "error": str(e)} 