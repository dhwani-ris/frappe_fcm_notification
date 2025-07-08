# -*- coding: utf-8 -*-

import frappe

def on_session_creation():
	"""Initialize Firebase on session creation"""
	try:
		# Check if Firebase settings exist and are active
		if frappe.db.exists("Firebase Settings", "Firebase Settings"):
			firebase_settings = frappe.get_single("Firebase Settings")
			if firebase_settings.is_active:
				# Initialize Firebase client
				from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
				get_firebase_client()
	except Exception as e:
		frappe.log_error(f"Error initializing Firebase on session creation: {str(e)}") 