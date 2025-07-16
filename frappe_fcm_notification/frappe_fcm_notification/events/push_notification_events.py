# -*- coding: utf-8 -*-

import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
import json
def on_update(doc, method):
	"""Handle on_update event for Push Notification Manager"""
	pass

def on_submit(doc, method):
	"""Handle on_submit event for Push Notification Manager"""
	if doc.notification_type == "Immediate":
		send_notification(doc)
	else:
		# Mark as scheduled
		doc.status = "Scheduled"
		doc.save()

def on_cancel(doc, method):
	"""Handle on_cancel event for Push Notification Manager"""
	if doc.status == "Scheduled":
		doc.status = "Cancelled"
		doc.save()

def send_notification(doc, data=None):
	"""Send the notification"""
	try:
		if data is None:
			data = {}
		elif isinstance(data, dict):
			pass
		elif isinstance(data, str):
			try:
				data = json.loads(data)
			except json.JSONDecodeError:
				frappe.throw(_("Data string is not valid JSON"))
		else:
			frappe.throw(_("Data must be a dictionary or JSON string"))



		# Get target users
		filters = data.pop("filters", [])
		target_users = get_target_users(doc, filters)
		
		if not target_users:
			frappe.throw(_("No target users found for this notification"))
		
		# Get FCM tokens for target users
		tokens = get_fcm_tokens_for_users(target_users)
		
		if not tokens:
			frappe.throw(_("No active FCM tokens found for target users"))
	

		# Send notification
		firebase_client = get_firebase_client()
		if len(tokens) == 1:
			result = firebase_client.send_single_notification(
				token=tokens[0],
				title=doc.notification_title,
				body=doc.notification_body,
				data=data,
				image_url=doc.image_url,
			)
		else:
			result = firebase_client.send_multicast_notification(
				tokens=tokens,
				title=doc.notification_title,
				body=doc.notification_body,
				data=data,
				image_url=doc.image_url,
			)
			print("Result", result)
			print("Data", data)

		

		# Update notification status
		if result.get("success"):
			doc.status = "Sent"
			doc.sent_count = result.get("success_count", len(tokens))
			doc.failed_count = result.get("failure_count", 0)
			doc.sent_date = now_datetime()
		else:
			doc.status = "Failed"
			doc.error_log = result.get("error", "Unknown error")
		
		doc.save()
		
		# Create Frappe notification record
		create_frappe_notification(doc, target_users, result)
		
	except Exception as e:
		doc.status = "Failed"
		doc.error_log = str(e)
		doc.save()
		frappe.log_error(f"Error sending notification {doc.name}: {str(e)}")

def get_target_users(doc, filters=None):
	"""Get target users based on notification settings"""
	users = []
	
	if doc.target_type == "All Users":
		users = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
	
	elif doc.target_type == "By Role":
		role_users = []
		for role_row in doc.target_roles:
			role_users.extend(frappe.get_all(
				"Has Role",
				filters={"role": role_row.role, "parenttype": "User"},
				pluck="parent"
			))
		
		users = list(set(role_users))
		if users:
			filters.append(("name", "in", users))
			users = frappe.get_all("User", filters=filters, pluck="name")
		
		print("Users", users)
		
	
	elif doc.target_type == "Specific Users":
		users = [user_row.user for user_row in doc.target_users]
	
	elif doc.target_type == "Custom Filter":
		# Parse custom filter JSON and apply
		try:
			filter_data = frappe.parse_json(doc.custom_filter)
			users = frappe.get_all("User", filters=filter_data, pluck="name")
		except Exception as e:
			frappe.throw(f"Invalid custom filter: {str(e)}")
	
	return users

def get_fcm_tokens_for_users(users):
	"""Get active FCM tokens for given users"""
	tokens = frappe.get_all(
		"User FCM Token",
		filters={
			"user": ["in", users],
			"is_token_active": 1
		},
		pluck="fcm_token"
	)
	return tokens

def create_frappe_notification(doc, target_users, result):
	"""Create Frappe notification record"""
	try:
		for user in target_users:
			# Create notification log entry directly in database
			notification_log = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": doc.notification_title,
				"for_user": user,
				"type": "Alert",
				"email_content": doc.notification_body,
				"document_type": "Push Notification Manager",
				"document_name": doc.name,
				"read": 0,
				"from_user": doc.modified_by or doc.owner,
			})
			notification_log.insert(ignore_permissions=True)
			
			# Trigger realtime notification
			frappe.publish_realtime("notification", after_commit=True, user=user)
		
		frappe.db.commit()
		
	except Exception as e:
		frappe.log_error(f"Error creating Frappe notification: {str(e)}") 