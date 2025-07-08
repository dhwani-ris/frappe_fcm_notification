# -*- coding: utf-8 -*-

import frappe
from frappe import _
from frappe.utils import now_datetime
from frappe.model.document import Document
from frappe import whitelist

class PushNotificationManager(Document):
	def validate(self):
		"""Validate notification settings"""
		self.validate_scheduled_datetime()
		self.validate_target_settings()
	
	def before_save(self):
		"""Set created_by before saving"""
		if not self.created_by:
			self.created_by = frappe.session.user
	
	def validate_scheduled_datetime(self):
		"""Validate scheduled datetime for scheduled notifications"""
		if self.notification_type == "Scheduled":
			if not self.scheduled_datetime:
				frappe.throw(_("Scheduled DateTime is required for scheduled notifications"))
			
			if self.scheduled_datetime <= now_datetime():
				frappe.throw(_("Scheduled DateTime must be in the future"))
	
	def validate_target_settings(self):
		"""Validate target settings based on target type"""
		if self.target_type == "By Role":
			if not self.target_roles:
				frappe.throw(_("Please select at least one role"))
		
		elif self.target_type == "Specific Users":
			if not self.target_users:
				frappe.throw(_("Please select at least one user"))
		
		elif self.target_type == "Custom Filter":
			if not self.custom_filter:
				frappe.throw(_("Please provide a custom filter"))
	
	@whitelist()
	def send_notification(self):
		"""Send the notification"""
		from frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events import send_notification
		send_notification(self)
	
	@whitelist()
	def get_target_users(self):
		"""Get target users based on notification settings"""
		from frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events import get_target_users
		return get_target_users(self)
	
	@whitelist()
	def get_delivery_stats(self):
		"""Get delivery statistics"""
		return {
			"sent_count": self.sent_count or 0,
			"failed_count": self.failed_count or 0,
			"total_count": (self.sent_count or 0) + (self.failed_count or 0),
			"success_rate": self.get_success_rate()
		}
	
	def get_success_rate(self):
		"""Calculate success rate"""
		total = (self.sent_count or 0) + (self.failed_count or 0)
		if total == 0:
			return 0
		return round((self.sent_count or 0) / total * 100, 2)
	
	@whitelist()
	def retry_failed_notification(self):
		"""Retry sending failed notification"""
		if self.status == "Failed":
			self.status = "Draft"
			self.error_log = ""
			self.save()
			self.send_notification()
		else:
			frappe.throw(_("Only failed notifications can be retried"))
	
	@whitelist()
	def cancel_scheduled_notification(self):
		"""Cancel scheduled notification"""
		if self.status == "Scheduled":
			self.status = "Cancelled"
			self.save()
		else:
			frappe.throw(_("Only scheduled notifications can be cancelled")) 