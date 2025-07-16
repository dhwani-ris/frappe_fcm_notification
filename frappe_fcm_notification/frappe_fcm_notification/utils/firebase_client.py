# -*- coding: utf-8 -*-

import json
import frappe
from frappe import _
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError
import logging

logger = logging.getLogger(__name__)

class FirebaseClient:
	"""Firebase FCM Client for sending push notifications"""
	
	def __init__(self):
		self.app = None
		self._initialize_firebase()
	
	def _initialize_firebase(self):
		"""Initialize Firebase Admin SDK with service account credentials"""
		try:
			# Get Firebase settings
			firebase_settings = frappe.get_single("Firebase Settings")
			
			if not firebase_settings.is_active:
				logger.warning("Firebase is not active. Please activate it in Firebase Settings.")
				return
			
			if not firebase_settings.service_account_json:
				logger.warning("Service account JSON file is not uploaded. Please upload it in Firebase Settings.")
				return
			
			# Get the file content
			file_doc = frappe.get_doc("File", {"file_url": firebase_settings.service_account_json})
			file_path = file_doc.get_full_path()
			print("file_pathdssdsdsdsdsds", file_path)
			logger.info(f"Service account JSON file path: {file_path}")
			logger.info(f"File URL: {firebase_settings.service_account_json}")
			
			# Check if file exists
			import os
			if not os.path.exists(file_path):
				logger.error(f"Service account JSON file not found at: {file_path}")
				# Try alternative path construction
				site_path = frappe.utils.get_site_path()
				alternative_path = os.path.join(site_path, "public", "files", os.path.basename(firebase_settings.service_account_json))
				logger.info(f"Trying alternative path: {alternative_path}")
				
				if os.path.exists(alternative_path):
					file_path = alternative_path
					logger.info(f"Using alternative path: {file_path}")
				else:
					logger.error(f"Alternative path also not found: {alternative_path}")
					return
			
			# Initialize Firebase Admin SDK
			cred = credentials.Certificate(file_path)
			
			# Check if app is already initialized
			try:
				self.app = firebase_admin.get_app()
			except ValueError:
				self.app = firebase_admin.initialize_app(cred)
				
		except Exception as e:
			logger.error(f"Firebase initialization failed: {str(e)}")
			# Don't raise exception during initialization, just log it
	
	def __del__(self):
		"""Cleanup Firebase app on deletion"""
		try:
			if self.app:
				firebase_admin.delete_app(self.app)
		except:
			pass
	
	def send_single_notification(self, token, title, body, data=None, image_url=None):
		"""Send notification to a single device"""
		try:
			if not self.app:
				return {"success": False, "error": "Firebase not initialized. Please check Firebase Settings."}
			
			message = messaging.Message(
				notification=messaging.Notification(
					title=title,
					body=body,
					image=image_url
				),
				data=data or {},
				token=token,
			)
			
			response = messaging.send(message)
			return {"success": True, "message_id": response}
			
		except messaging.UnregisteredError:
			# Token is invalid, mark it as inactive
			self._mark_token_inactive(token)
			return {"success": False, "error": "Token is invalid or expired"}
			
		except messaging.QuotaExceededError:
			return {"success": False, "error": "Quota exceeded"}
			
		except messaging.ThirdPartyAuthError:
			return {"success": False, "error": "Authentication error"}
			
		except Exception as e:
			logger.error(f"Error sending notification: {str(e)}")
			return {"success": False, "error": str(e)}
	
	def send_multicast_notification(self, tokens, title, body, data=None, image_url=None):
		"""Send notification to multiple devices"""
		try:
			print("Data", data)
			message = messaging.MulticastMessage(
				notification=messaging.Notification(
					title=title,
					body=body,
					image=image_url
				),
				data=data or {},
				tokens=tokens,
			)
			
			response = messaging.send_each_for_multicast(message)
			
			# Handle invalid tokens
			if response.failure_count > 0:
				for idx, result in enumerate(response.responses):
					if not result.success:
						if isinstance(result.exception, messaging.UnregisteredError):
							self._mark_token_inactive(tokens[idx])
			
			return {
				"success": True,
				"success_count": response.success_count,
				"failure_count": response.failure_count,
				"responses": response.responses
			}
			
		except Exception as e:
			logger.error(f"Error sending multicast notification: {str(e)}")
			return {"success": False, "error": str(e)}
	
	def send_topic_notification(self, topic, title, body, data=None, image_url=None):
		"""Send notification to a topic"""
		try:
			message = messaging.Message(
				notification=messaging.Notification(
					title=title,
					body=body,
					image=image_url
				),
				data=data or {},
				topic=topic,
			)
			
			response = messaging.send(message)
			return {"success": True, "message_id": response}
			
		except Exception as e:
			logger.error(f"Error sending topic notification: {str(e)}")
			return {"success": False, "error": str(e)}
	
	def validate_token(self, token):
		"""Validate if a token is still valid"""
		try:
			# Try to send a test message
			message = messaging.Message(
				notification=messaging.Notification(
					title="Test",
					body="Test"
				),
				token=token,
			)
			
			messaging.send(message)
			return True
			
		except messaging.UnregisteredError:
			return False
			
		except Exception:
			return False
	
	def _mark_token_inactive(self, token):
		"""Mark a token as inactive when it's invalid"""
		try:
			token_doc = frappe.get_doc("User FCM Token", {"fcm_token": token})
			token_doc.is_token_active = 0
			token_doc.save()
			frappe.db.commit()
		except Exception as e:
			logger.error(f"Error marking token inactive: {str(e)}")
	
	def test_connection(self):
		"""Test Firebase connection"""
		try:
			if not self.app:
				# Try to re-initialize
				self._initialize_firebase()
				if not self.app:
					return {"success": False, "error": "Firebase not initialized. Please check Firebase Settings."}
			
			# Try to get project info
			project_id = self.app.project_id
			return {"success": True, "project_id": project_id}
		except Exception as e:
			return {"success": False, "error": str(e)}
	
	def force_reinitialize(self):
		"""Force re-initialization of Firebase"""
		try:
			# Delete existing app if any
			if self.app:
				firebase_admin.delete_app(self.app)
				self.app = None
			
			# Re-initialize
			self._initialize_firebase()
			return {"success": True if self.app else False, "error": None if self.app else "Failed to re-initialize"}
		except Exception as e:
			return {"success": False, "error": str(e)}

def get_firebase_client():
	"""Get Firebase client instance"""
	client = FirebaseClient()
	# Force re-initialization if not properly initialized
	if not client.app:
		client._initialize_firebase()
	return client 