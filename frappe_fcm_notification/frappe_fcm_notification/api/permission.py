# -*- coding: utf-8 -*-

import frappe

def has_app_permission():
	"""Check if user has permission to access the FCM app"""
	return frappe.has_permission("Firebase Settings", "read")

def has_firebase_settings_permission():
	"""Check if user has permission to access Firebase Settings"""
	return frappe.has_permission("Firebase Settings", "read")

def has_push_notification_permission():
	"""Check if user has permission to access Push Notification Manager"""
	return frappe.has_permission("Push Notification Manager", "read") 