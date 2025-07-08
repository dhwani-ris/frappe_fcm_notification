# -*- coding: utf-8 -*-

import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe.model.document import Document
from frappe import whitelist

class UserFCMToken(Document):
	def validate(self):
		"""Validate FCM token"""
		self.validate_token_uniqueness()
		self.validate_user_exists()
	
	def before_save(self):
		"""Set timestamps before saving"""
		if not self.token_created_date:
			self.token_created_date = now_datetime()
		self.token_last_updated = now_datetime()
	
	def validate_token_uniqueness(self):
		"""Ensure no duplicate active tokens for the same user"""
		if self.is_token_active:
			existing_token = frappe.db.exists("User FCM Token", {
				"fcm_token": self.fcm_token,
				"user": self.user,
				"is_token_active": 1,
				"name": ["!=", self.name]
			})
			
			if existing_token:
				frappe.throw(_("This FCM token is already active for this user"))
	
	def validate_user_exists(self):
		"""Validate that the user exists"""
		if not frappe.db.exists("User", self.user):
			frappe.throw(_("User {0} does not exist").format(self.user))
	
	@whitelist()
	def refresh_token(self):
		"""Refresh the token timestamp"""
		self.token_last_updated = now_datetime()
		self.save()
	
	@whitelist()
	def deactivate_token(self):
		"""Deactivate the token"""
		self.is_token_active = 0
		self.save()
	
	@whitelist()
	def activate_token(self):
		"""Activate the token"""
		self.is_token_active = 1
		self.save() 