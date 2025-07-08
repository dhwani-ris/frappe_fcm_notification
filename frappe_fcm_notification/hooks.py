app_name = "frappe_fcm_notification"
app_title = "Frappe FCM Notification"
app_publisher = "Dhwani RIS"
app_description = "Send Firebase Cloud Messaging Notifications from your Frappe Site"
app_email = "bhushan.barbuddhe@dhwaniris.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "frappe_fcm_notification",
		"logo": "/assets/frappe_fcm_notification/logo.png",
		"title": "Frappe FCM Notification",
		"route": "/frappe_fcm_notification",
		"has_permission": "frappe_fcm_notification.frappe_fcm_notification.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/frappe_fcm_notification/css/frappe_fcm_notification.css"
app_include_js = "/assets/frappe_fcm_notification/js/frappe_fcm_notification.js"

# include js, css files in header of web template
web_include_css = "/assets/frappe_fcm_notification/css/frappe_fcm_notification.css"
web_include_js = "/assets/frappe_fcm_notification/js/frappe_fcm_notification.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_fcm_notification/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Firebase Settings": "public/js/firebase_settings.js",
	"Push Notification Manager": "public/js/push_notification_manager.js",
	"User FCM Token": "public/js/user_fcm_token.js"
}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "frappe_fcm_notification/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "frappe_fcm_notification.utils.jinja_methods",
# 	"filters": "frappe_fcm_notification.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappe_fcm_notification.install.before_install"
# after_install = "frappe_fcm_notification.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_fcm_notification.uninstall.before_uninstall"
# after_uninstall = "frappe_fcm_notification.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "frappe_fcm_notification.utils.before_app_install"
# after_app_install = "frappe_fcm_notification.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "frappe_fcm_notification.utils.before_app_uninstall"
# after_app_uninstall = "frappe_fcm_notification.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_fcm_notification.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Firebase Settings": "frappe_fcm_notification.frappe_fcm_notification.permissions.permissions.get_firebase_settings_permission_query_conditions",
	"Push Notification Manager": "frappe_fcm_notification.frappe_fcm_notification.permissions.permissions.get_push_notification_permission_query_conditions",
}

has_permission = {
	"Firebase Settings": "frappe_fcm_notification.frappe_fcm_notification.permissions.permissions.has_firebase_settings_permission",
	"Push Notification Manager": "frappe_fcm_notification.frappe_fcm_notification.permissions.permissions.has_push_notification_permission",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Push Notification Manager": {
		"on_update": "frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events.on_update",
		"on_submit": "frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events.on_submit",
		"on_cancel": "frappe_fcm_notification.frappe_fcm_notification.events.push_notification_events.on_cancel",
	},
	"User FCM Token": {
		"on_update": "frappe_fcm_notification.frappe_fcm_notification.events.user_fcm_token_events.on_update",
		"on_trash": "frappe_fcm_notification.frappe_fcm_notification.events.user_fcm_token_events.on_trash",
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.all"
	],
	"daily": [
		"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.daily"
	],
	"hourly": [
		"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.hourly"
	],
	"cron": {
		"*/5 * * * *": [
			"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.process_scheduled_notifications"
		],
		"0 2 * * *": [
			"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.cleanup_expired_tokens"
		],
		"*/15 * * * *": [
			"frappe_fcm_notification.frappe_fcm_notification.tasks.scheduled_tasks.retry_failed_notifications"
		],
	},
}

# Testing
# -------

# before_tests = "frappe_fcm_notification.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_fcm_notification.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_fcm_notification.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["frappe_fcm_notification.utils.before_request"]
# after_request = ["frappe_fcm_notification.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_fcm_notification.utils.before_job"]
# after_job = ["frappe_fcm_notification.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "User FCM Token",
		"filter_by": "user",
		"redact_fields": ["fcm_token"],
		"partial": 1,
	},
	{
		"doctype": "Push Notification Manager",
		"filter_by": "created_by",
		"partial": 1,
	},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"frappe_fcm_notification.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# API Whitelist
# -------------

# Whitelist API methods
override_whitelisted_methods = {
	"frappe_fcm_notification.frappe_fcm_notification.api.fcm.save_fcm_token": "frappe_fcm_notification.frappe_fcm_notification.api.fcm.save_fcm_token",
	"frappe_fcm_notification.frappe_fcm_notification.api.fcm.test_firebase_connection": "frappe_fcm_notification.frappe_fcm_notification.api.fcm.test_firebase_connection",
	"frappe_fcm_notification.frappe_fcm_notification.api.fcm.send_test_notification": "frappe_fcm_notification.frappe_fcm_notification.api.fcm.send_test_notification",
}

# Startup hooks
# -------------
on_session_creation = "frappe_fcm_notification.frappe_fcm_notification.startup.startup.on_session_creation"

