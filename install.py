#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frappe FCM Notification Installation Script
This script helps with the initial setup of the FCM notification app.
"""

import frappe
import json
from frappe.utils import now_datetime

def install():
	"""Install the FCM notification app"""
	
	# Create Firebase Settings if it doesn't exist
	if not frappe.db.exists("Firebase Settings", "Firebase Settings"):
		firebase_settings = frappe.get_doc({
			"doctype": "Firebase Settings",
			"project_name": "Your Firebase Project",
			"project_id": "your-project-id",
			"is_active": 0,  # Disabled by default for security
			"created_date": now_datetime(),
			"last_updated": now_datetime()
		})
		firebase_settings.insert()
		frappe.db.commit()
		print("✅ Firebase Settings created")
	else:
		print("ℹ️  Firebase Settings already exists")
	
	# Create default roles if they don't exist
	create_default_roles()
	
	# Set up permissions
	setup_permissions()
	
	# Create sample notification templates
	create_sample_templates()
	
	print("\n🎉 Frappe FCM Notification installation completed!")
	print("\nNext steps:")
	print("1. Go to Firebase Settings and upload your service account JSON")
	print("2. Test the Firebase connection")
	print("3. Start sending notifications!")

def create_default_roles():
	"""Create default roles for FCM notifications"""
	roles = [
		"FCM User",
		"FCM Manager",
		"FCM Admin"
	]
	
	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			role = frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1
			})
			role.insert()
			print(f"✅ Created role: {role_name}")
		else:
			print(f"ℹ️  Role already exists: {role_name}")

def setup_permissions():
	"""Set up default permissions"""
	
	# FCM User permissions
	fcm_user_perms = [
		{
			"doctype": "Push Notification Manager",
			"role": "FCM User",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0
		},
		{
			"doctype": "User FCM Token",
			"role": "FCM User",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 1,
			"submit": 0,
			"cancel": 0,
			"amend": 0
		}
	]
	
	# FCM Manager permissions
	fcm_manager_perms = [
		{
			"doctype": "Push Notification Manager",
			"role": "FCM Manager",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1
		},
		{
			"doctype": "User FCM Token",
			"role": "FCM Manager",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 1,
			"submit": 0,
			"cancel": 0,
			"amend": 0
		}
	]
	
	# FCM Admin permissions (full access)
	fcm_admin_perms = [
		{
			"doctype": "Firebase Settings",
			"role": "FCM Admin",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 1,
			"submit": 0,
			"cancel": 0,
			"amend": 0
		},
		{
			"doctype": "Push Notification Manager",
			"role": "FCM Admin",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1
		},
		{
			"doctype": "User FCM Token",
			"role": "FCM Admin",
			"create": 1,
			"read": 1,
			"write": 1,
			"delete": 1,
			"submit": 0,
			"cancel": 0,
			"amend": 0
		}
	]
	
	# Create permissions
	all_perms = fcm_user_perms + fcm_manager_perms + fcm_admin_perms
	
	for perm in all_perms:
		if not frappe.db.exists("Custom DocPerm", {
			"parent": perm["doctype"],
			"role": perm["role"]
		}):
			docperm = frappe.get_doc({
				"doctype": "Custom DocPerm",
				"parent": perm["doctype"],
				"role": perm["role"],
				"create": perm.get("create", 0),
				"read": perm.get("read", 0),
				"write": perm.get("write", 0),
				"delete": perm.get("delete", 0),
				"submit": perm.get("submit", 0),
				"cancel": perm.get("cancel", 0),
				"amend": perm.get("amend", 0)
			})
			docperm.insert()
	
	frappe.db.commit()
	print("✅ Permissions set up successfully")

def create_sample_templates():
	"""Create sample notification templates"""
	
	sample_notifications = [
		{
			"title": "Welcome to Our App!",
			"body": "Thank you for joining us. We're excited to have you on board!",
			"target_type": "All Users",
			"notification_type": "Immediate"
		},
		{
			"title": "System Maintenance",
			"body": "We'll be performing system maintenance tonight from 2-4 AM. Please save your work.",
			"target_type": "All Users",
			"notification_type": "Scheduled"
		},
		{
			"title": "New Feature Available",
			"body": "Check out our latest feature that will make your work easier!",
			"target_type": "By Role",
			"notification_type": "Immediate"
		}
	]
	
	for i, notification in enumerate(sample_notifications):
		doc_name = f"SAMPLE-{i+1:03d}"
		if not frappe.db.exists("Push Notification Manager", doc_name):
			doc = frappe.get_doc({
				"doctype": "Push Notification Manager",
				"notification_title": notification["title"],
				"notification_body": notification["body"],
				"target_type": notification["target_type"],
				"notification_type": notification["notification_type"],
				"status": "Draft"
			})
			doc.insert()
			print(f"✅ Created sample notification: {notification['title']}")
		else:
			print(f"ℹ️  Sample notification already exists: {notification['title']}")

def uninstall():
	"""Uninstall the FCM notification app"""
	
	# Delete all FCM related documents
	doctypes_to_clean = [
		"Push Notification Manager",
		"User FCM Token",
		"Firebase Settings"
	]
	
	for doctype in doctypes_to_clean:
		docs = frappe.get_all(doctype, pluck="name")
		for doc_name in docs:
			try:
				frappe.delete_doc(doctype, doc_name, force=1)
			except:
				pass
	
	# Delete custom roles
	roles_to_delete = ["FCM User", "FCM Manager", "FCM Admin"]
	for role_name in roles_to_delete:
		if frappe.db.exists("Role", role_name):
			try:
				frappe.delete_doc("Role", role_name, force=1)
			except:
				pass
	
	frappe.db.commit()
	print("🗑️  FCM notification app uninstalled")

if __name__ == "__main__":
	# This script can be run from the Frappe bench console
	# bench --site your-site.com console
	# Then run: exec(open('install.py').read())
	# Then run: install()
	pass 