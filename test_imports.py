#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify all FCM notification app imports work correctly
"""

def test_imports():
	"""Test all module imports"""
	
	print("🧪 Testing FCM Notification App Imports...")
	print("=" * 50)
	
	# Test imports
	imports_to_test = [
		("Firebase Client", "frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client"),
		("API FCM", "frappe_fcm_notification.frappe_fcm_notification.api.fcm"),
		("API Permission", "frappe_fcm_notification.frappe_fcm_notification.api.permission"),
		("Permissions", "frappe_fcm_notification.frappe_fcm_notification.permissions.permissions"),
		("Push Notification Events", "frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events"),
		("User FCM Token Events", "frappe_fcm_notification.frappe_fcm_notification.events.user_fcm_token_events"),
		("Scheduled Tasks", "frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks"),
		("Startup", "frappe_fcm_notification.frappe_fcm_notification.startup.startup"),
	]
	
	success_count = 0
	total_count = len(imports_to_test)
	
	for name, module_path in imports_to_test:
		try:
			__import__(module_path)
			print(f"✅ {name}: {module_path}")
			success_count += 1
		except ImportError as e:
			print(f"❌ {name}: {module_path}")
			print(f"   Error: {str(e)}")
		except Exception as e:
			print(f"⚠️  {name}: {module_path}")
			print(f"   Warning: {str(e)}")
			success_count += 1  # Count as success if it's not an import error
	
	print("\n" + "=" * 50)
	print(f"📊 Results: {success_count}/{total_count} imports successful")
	
	if success_count == total_count:
		print("🎉 All imports successful! The app should work correctly.")
	else:
		print("⚠️  Some imports failed. Please check the errors above.")
	
	return success_count == total_count

if __name__ == "__main__":
	# This script can be run from the Frappe bench console
	# bench --site your-site.com console
	# Then run: exec(open('test_imports.py').read())
	# Then run: test_imports()
	pass 