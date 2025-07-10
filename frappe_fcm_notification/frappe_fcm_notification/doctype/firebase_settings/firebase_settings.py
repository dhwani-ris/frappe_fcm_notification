# -*- coding: utf-8 -*-

import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe.model.document import Document
from frappe import whitelist
import json

class FirebaseSettings(Document):
	def validate(self):
		"""Validate Firebase settings"""
		if self.service_account_json:
			self.validate_service_account_json()
		
		# if self.is_active:
		# 	self.validate_firebase_connection()
	
	def before_save(self):
		"""Set timestamps before saving"""
		if not self.created_date:
			self.created_date = now_datetime()
		self.last_updated = now_datetime()
	
	@frappe.whitelist()
	def validate_service_account_json(self):
		"""Validate the uploaded service account JSON file"""
		try:
			# Get the file content
			file_doc = frappe.get_doc("File", {"file_url": self.service_account_json})
			file_path = file_doc.get_full_path()
			print("file_pathdsdsd", file_path)
			with open(file_path, 'r') as f:
				json_content = json.load(f)
			
			# Check required fields
			required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
			for field in required_fields:
				if field not in json_content:
					frappe.throw(_(f"Invalid service account JSON: Missing required field '{field}'"))
			
			# Validate project ID matches
			if json_content.get('project_id') != self.project_id:
				frappe.throw(_("Project ID in JSON file doesn't match the Project ID field"))
				
		except Exception as e:
			frappe.throw(_(f"Error validating service account JSON: {str(e)}"))
	
	def validate_firebase_connection(self):
		"""Test Firebase connection"""
		try:
			from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
			result = get_firebase_client().test_connection()
			
			if not result.get("success"):
				frappe.throw(_(f"Firebase connection test failed: {result.get('error')}"))
				
		except Exception as e:
			frappe.throw(_(f"Error testing Firebase connection: {str(e)}"))
	
	@whitelist()
	def force_reinitialize(self):
		"""Force re-initialization of Firebase client"""
		try:
			from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
			client = get_firebase_client()
			result = client.force_reinitialize()
			return result
		except Exception as e:
			return {"success": False, "error": str(e)} 
		
@whitelist(allow_guest=True)
def send_test_notification(token):
	"""Send test notification to validate setup"""
	try:
		from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
		result = get_firebase_client().send_single_notification(
			token=token,
			title="Test Notification",
			body="This is a test notification from Firebase Settings",
			data={"type": "test", "source": "firebase_settings"}
		)
		print("Sending Test Notification", result)
		return result
	except Exception as e:
		return {"success": False, "error": str(e)}

@whitelist(allow_guest=True)
def test_connection():
	"""Test Firebase connection and return result"""
	try:
		from frappe_fcm_notification.frappe_fcm_notification.utils.firebase_client import get_firebase_client
		result = get_firebase_client().test_connection()
		return result
	except Exception as e:
		return {"success": False, "error": str(e)}