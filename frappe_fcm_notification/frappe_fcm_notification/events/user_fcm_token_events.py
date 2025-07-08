# -*- coding: utf-8 -*-

import frappe
from frappe.utils import now_datetime

def on_update(doc, method):
	"""Handle on_update event for User FCM Token"""
	# Update last updated timestamp
	doc.token_last_updated = now_datetime()
	
	# If token is marked as inactive, log it
	if not doc.is_token_active:
		frappe.logger().info(f"FCM token {doc.name} marked as inactive for user {doc.user}")

def on_trash(doc, method):
	"""Handle on_trash event for User FCM Token"""
	frappe.logger().info(f"FCM token {doc.name} deleted for user {doc.user}") 