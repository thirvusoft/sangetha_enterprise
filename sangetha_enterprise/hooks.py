app_name = "sangetha_enterprise"
app_title = "Sangeetha Enterprise"
app_publisher = "Thirvusoft Private Limited"
app_description = "Retail application"
app_email = "thirvusoft@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sangetha_enterprise/css/sangetha_enterprise.css"
# app_include_js = "/assets/sangetha_enterprise/js/sangetha_enterprise.js"

# include js, css files in header of web template
# web_include_css = "/assets/sangetha_enterprise/css/sangetha_enterprise.css"
# web_include_js = "/assets/sangetha_enterprise/js/sangetha_enterprise.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sangetha_enterprise/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Opportunity" : "/sangeetha_enterprise/utils/js/opportunity.js",
'Sales Invoice':"/sangeetha_enterprise/utils/js/sales_invoice.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sangetha_enterprise/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
    "methods" : [
      "sangetha_enterprise.sangeetha_enterprise.utils.py.print_format.get_invoice_item_and_tax_details",
       "frappe.utils.data.money_in_words"
    ]
}

# Installation
# ------------

# before_install = "sangetha_enterprise.install.before_install"
# after_install = "sangetha_enterprise.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sangetha_enterprise.uninstall.before_uninstall"
# after_uninstall = "sangetha_enterprise.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sangetha_enterprise.utils.before_app_install"
# after_app_install = "sangetha_enterprise.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sangetha_enterprise.utils.before_app_uninstall"
# after_app_uninstall = "sangetha_enterprise.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sangetha_enterprise.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Sales Invoice": "sangetha_enterprise.sangeetha_enterprise.utils.py.sales_invoice.CustomSalesInvoice"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"validate": "sangetha_enterprise.sangeetha_enterprise.utils.py.sales_invoice.validate"
	},
  # "Purchase Order":{
  #     "on_submit": "sangetha_enterprise.sangeetha_enterprise.utils.py.purchase_order.on_submit"
  # },
  # "Sales Order":{
  #     "on_submit":"sangetha_enterprise.sangeetha_enterprise.utils.py.sales_order.on_submit"
  # }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"sangetha_enterprise.tasks.all"
#	],
#	"daily": [
#		"sangetha_enterprise.tasks.daily"
#	],
#	"hourly": [
#		"sangetha_enterprise.tasks.hourly"
#	],
#	"weekly": [
#		"sangetha_enterprise.tasks.weekly"
#	],
#	"monthly": [
#		"sangetha_enterprise.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "sangetha_enterprise.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "sangetha_enterprise.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "sangetha_enterprise.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sangetha_enterprise.utils.before_request"]
# after_request = ["sangetha_enterprise.utils.after_request"]

# Job Events
# ----------
# before_job = ["sangetha_enterprise.utils.before_job"]
# after_job = ["sangetha_enterprise.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"sangetha_enterprise.auth.validate"
# ]
