#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frappe FCM Notification Installation Verification Script
This script verifies that all components are properly installed.
"""

import frappe

def verify_installation():
	"""Verify that the FCM notification app is properly installed"""
	
	print("🔍 Verifying Frappe FCM Notification Installation...")
	print("=" * 50)
	
	# Check if DocTypes exist
	doctypes_to_check = [
		"Firebase Settings",
		"User FCM Token", 
		"Push Notification Manager",
		"Push Notification Target Role",
		"Push Notification Target User"
	]
	
	print("\n📋 Checking DocTypes:")
	for doctype in doctypes_to_check:
		if frappe.db.exists("DocType", doctype):
			print(f"✅ {doctype}")
		else:
			print(f"❌ {doctype} - MISSING")
	
	# Check if modules are importable
	print("\n📦 Checking Module Imports:")
	modules_to_check = [
		"frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client",
		"frappe_fcm_notification.frappe_fcm_notification.api.fcm",
		"frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events",
		"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks"
	]
	
	for module in modules_to_check:
		try:
			__import__(module)
			print(f"✅ {module}")
		except ImportError as e:
			print(f"❌ {module} - {str(e)}")
	
	# Check if Firebase Settings document exists
	print("\n⚙️  Checking Firebase Settings:")
	try:
		if frappe.db.exists("Firebase Settings", "Firebase Settings"):
			settings = frappe.get_doc("Firebase Settings", "Firebase Settings")
			print(f"✅ Firebase Settings document exists")
			print(f"   - Project Name: {settings.project_name}")
			print(f"   - Is Active: {settings.is_active}")
		else:
			print("❌ Firebase Settings document not found")
	except Exception as e:
		print(f"❌ Error accessing Firebase Settings: {str(e)}")
	
	# Check permissions
	print("\n🔐 Checking Permissions:")
	roles_to_check = ["System Manager", "FCM Admin", "FCM Manager", "FCM User"]
	for role in roles_to_check:
		if frappe.db.exists("Role", role):
			print(f"✅ Role: {role}")
		else:
			print(f"⚠️  Role: {role} - Not found (will be created during setup)")
	
	# Check scheduled tasks
	print("\n⏰ Checking Scheduled Tasks:")
	scheduler_events = frappe.get_hooks().get("scheduler_events", {})
	if "cron" in scheduler_events:
		cron_tasks = scheduler_events["cron"]
		fcm_tasks = [
			"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.process_scheduled_notifications",
			"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.cleanup_expired_tokens",
			"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.retry_failed_notifications"
		]
		for task in fcm_tasks:
			if any(task in str(cron_tasks.values())):
				print(f"✅ {task}")
			else:
				print(f"❌ {task} - Not found in scheduler")
	else:
		print("❌ No cron tasks found in scheduler_events")
	
	print("\n" + "=" * 50)
	print("🎉 Verification Complete!")
	print("\nIf you see any ❌ errors above, please:")
	print("1. Run: bench migrate")
	print("2. Run: bench clear-cache")
	print("3. Restart your Frappe server")
	print("4. Run this verification script again")

if __name__ == "__main__":
	# This script can be run from the Frappe bench console
	# bench --site your-site.com console
	# Then run: exec(open('verify_installation.py').read())
	# Then run: verify_installation()
	pass 