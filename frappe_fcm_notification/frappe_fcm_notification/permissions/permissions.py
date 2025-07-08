# -*- coding: utf-8 -*-

import frappe

def get_firebase_settings_permission_query_conditions(user):
	"""Permission query conditions for Firebase Settings"""
	if not user:
		user = frappe.session.user
	
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	return "`tabFirebase Settings`.name = ''"  # No access for non-system managers

def has_firebase_settings_permission(doc, ptype, user):
	"""Check if user has permission for Firebase Settings"""
	if not user:
		user = frappe.session.user
	
	if "System Manager" in frappe.get_roles(user):
		return True
	
	return False

def get_push_notification_permission_query_conditions(user):
	"""Permission query conditions for Push Notification Manager"""
	if not user:
		user = frappe.session.user
	
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Allow users to see their own notifications
	return f"`tabPush Notification Manager`.created_by = '{user}'"

def has_push_notification_permission(doc, ptype, user):
	"""Check if user has permission for Push Notification Manager"""
	if not user:
		user = frappe.session.user
	
	if "System Manager" in frappe.get_roles(user):
		return True
	
	# Users can only access their own notifications
	if doc.created_by == user:
		return True
	
	return False 