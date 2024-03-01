import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice,validate_inter_company_party,update_linked_doc
from frappe.utils import add_days, cint
from erpnext.accounts.deferred_revenue import validate_service_stop_date
from erpnext.selling.doctype.customer.customer import get_credit_limit,get_customer_outstanding
from frappe.utils import cint, cstr, flt
from erpnext.setup.doctype.company.company import update_company_current_month_sales
from frappe import _, msgprint, throw
from frappe.utils.user import get_users_with_role
from frappe.utils import cint, cstr, flt, get_formatted_email, today

@frappe.whitelist()
def get_margin_rate(item_code,rate):
	highest_rate = frappe.get_value('Item Price',{'item_code':item_code},'price_list_rate',order_by='price_list_rate desc') or 0
	lowest_rate = frappe.get_value('Item Price',{'item_code':item_code},'price_list_rate',order_by='price_list_rate asc') or 0
	if float(rate):
		if highest_rate:
			highest_margin = ((float(rate) - highest_rate)/highest_rate) * 100
		else:
			highest_margin = 0
		if lowest_rate:
			lowest_margin = ((float(rate) - lowest_rate )/lowest_rate) * 100
		else:
			lowest_margin = 0

	else:
		highest_margin = 0
		lowest_margin = 0
	return {"custom_highest_margin_rate":highest_rate,"custom_lowest_margin_rate":lowest_rate,'custom_highest_margin':highest_margin,'custom_lowest_margin':lowest_margin}

def validate(doc,event):
	for i in doc.items:
		update_row = get_margin_rate(i.item_code,i.rate)
		i.update(update_row)


class CustomSalesInvoice(SalesInvoice):
	def validate(self):
		super(SalesInvoice, self).validate()
		self.check_credit_limit()

		self.validate_auto_set_posting_time()

		if not self.is_pos:
			self.so_dn_required()

		self.set_tax_withholding()

		self.validate_proj_cust()
		self.validate_pos_return()
		self.validate_with_previous_doc()
		self.validate_uom_is_integer("stock_uom", "stock_qty")
		self.validate_uom_is_integer("uom", "qty")
		self.check_sales_order_on_hold_or_close("sales_order")
		self.validate_debit_to_acc()
		self.clear_unallocated_advances("Sales Invoice Advance", "advances")
		self.add_remarks()
		self.validate_fixed_asset()
		self.set_income_account_for_fixed_assets()
		self.validate_item_cost_centers()
		self.check_conversion_rate()
		self.validate_accounts()

		validate_inter_company_party(
			self.doctype, self.customer, self.company, self.inter_company_invoice_reference
		)

		if cint(self.is_pos):
			self.validate_pos()

		if cint(self.update_stock):
			self.validate_dropship_item()
			self.validate_warehouse()
			self.update_current_stock()
			self.validate_delivery_note()

		# validate service stop date to lie in between start and end date
		validate_service_stop_date(self)

		if not self.is_opening:
			self.is_opening = "No"

		if self.redeem_loyalty_points:
			lp = frappe.get_doc("Loyalty Program", self.loyalty_program)
			self.loyalty_redemption_account = (
				lp.expense_account if not self.loyalty_redemption_account else self.loyalty_redemption_account
			)
			self.loyalty_redemption_cost_center = (
				lp.cost_center
				if not self.loyalty_redemption_cost_center
				else self.loyalty_redemption_cost_center
			)

		self.set_against_income_account()
		self.validate_time_sheets_are_submitted()
		self.validate_multiple_billing("Delivery Note", "dn_detail", "amount")
		if not self.is_return:
			self.validate_serial_numbers()
		else:
			self.timesheets = []
		self.update_packing_list()
		self.set_billing_hours_and_amount()
		self.update_timesheet_billing_for_project()
		self.set_status()
		if self.is_pos and not self.is_return:
			self.verify_payment_amount_is_positive()

		# validate amount in mode of payments for returned invoices for pos must be negative
		if self.is_pos and self.is_return:
			self.verify_payment_amount_is_negative()

		if (
			self.redeem_loyalty_points
			and self.loyalty_program
			and self.loyalty_points
			and not self.is_consolidated
		):
			validate_loyalty_points(self, self.loyalty_points)

		self.reset_default_field_value("set_warehouse", "items", "warehouse")


	def on_submit(self):
		self.validate_pos_paid_amount()

		if not self.auto_repeat:
			frappe.get_doc("Authorization Control").validate_approving_authority(
				self.doctype, self.company, self.base_grand_total, self
			)

		self.check_prev_docstatus()

		if self.is_return and not self.update_billed_amount_in_sales_order:
			# NOTE status updating bypassed for is_return
			self.status_updater = []

		self.update_status_updater_args()
		self.update_prevdoc_status()

		self.update_billing_status_in_dn()
		self.clear_unallocated_mode_of_payments()

		# Updating stock ledger should always be called after updating prevdoc status,
		# because updating reserved qty in bin depends upon updated delivered qty in SO
		if self.update_stock == 1:
			self.make_bundle_using_old_serial_batch_fields()
			self.update_stock_ledger()

		# this sequence because outstanding may get -ve
		self.make_gl_entries()

		if self.update_stock == 1:
			self.repost_future_sle_and_gle()

		if not self.is_return:
			self.update_billing_status_for_zero_amount_refdoc("Delivery Note")
			self.update_billing_status_for_zero_amount_refdoc("Sales Order")
			# self.check_credit_limit()

		if not cint(self.is_pos) == 1 and not self.is_return:
			self.update_against_document_in_jv()

		self.update_time_sheet(self.name)

		if (
			frappe.db.get_single_value("Selling Settings", "sales_update_frequency") == "Each Transaction"
		):
			update_company_current_month_sales(self.company)
			self.update_project()
		update_linked_doc(self.doctype, self.name, self.inter_company_invoice_reference)

		# create the loyalty point ledger entry if the customer is enrolled in any loyalty program
		if not self.is_return and not self.is_consolidated and self.loyalty_program:
			self.make_loyalty_point_entry()
		elif (
			self.is_return and self.return_against and not self.is_consolidated and self.loyalty_program
		):
			against_si_doc = frappe.get_doc("Sales Invoice", self.return_against)
			against_si_doc.delete_loyalty_point_entry()
			against_si_doc.make_loyalty_point_entry()
		if self.redeem_loyalty_points and not self.is_consolidated and self.loyalty_points:
			self.apply_loyalty_points()

		self.process_common_party_accounting()
		
	def check_credit_limit(self):
		validate_against_credit_limit = False
		bypass_credit_limit_check_at_sales_order = frappe.db.get_value(
			"Customer Credit Limit",
			filters={"parent": self.customer, "parenttype": "Customer", "company": self.company},
			fieldname=["bypass_credit_limit_check"],
		)

		if bypass_credit_limit_check_at_sales_order:
			validate_against_credit_limit = True

		for d in self.get("items"):
			if not (d.sales_order or d.delivery_note):
				validate_against_credit_limit = True
				break
		if validate_against_credit_limit:
			
			check_credit_limit(self,self.customer, self.company, bypass_credit_limit_check_at_sales_order)


def check_credit_limit(self, customer, company, ignore_outstanding_sales_order=False, extra_amount=0):
	credit_limit = get_credit_limit(customer, company)
	if not credit_limit:
		return

	customer_outstanding = get_customer_outstanding(customer, company, ignore_outstanding_sales_order)
	if extra_amount > 0:
		customer_outstanding += flt(extra_amount)

	if credit_limit > 0 and flt(customer_outstanding) > credit_limit:
		message = _("Credit limit has been crossed for customer {0} ({1}/{2})").format(
			customer, customer_outstanding, credit_limit
		)

		message += "<br><br>"

		# If not authorized person raise exception
		credit_controller_role = frappe.db.get_single_value("Accounts Settings", "credit_controller")
		if not credit_controller_role or credit_controller_role not in frappe.get_roles():
			# form a list of emails for the credit controller users
			credit_controller_users = get_users_with_role(credit_controller_role or "Sales Master Manager")

			# form a list of emails and names to show to the user
			credit_controller_users_formatted = [
				get_formatted_email(user).replace("<", "(").replace(">", ")")
				for user in credit_controller_users
			]
			if not credit_controller_users_formatted:
				frappe.throw(
					_("Please contact your administrator to extend the credit limits for {0}.").format(customer)
				)

			user_list = "<br><br><ul><li>{0}</li></ul>".format(
				"<li>".join(credit_controller_users_formatted)
			)

			message += _(
				"Please contact any of the following users to extend the credit limits for {0}: {1}"
			).format(customer, user_list)

			self.custom_credit_exceeded = 1
			# if the current user does not have permissions to override credit limit,
			# prompt them to send out an email to the controller users
			# frappe.msgprint(
			# 	message,
			# 	title=_("Credit Limit Crossed"),
			# 	raise_exception=1,
			# 	primary_action={
			# 		"label": "Send Email",
			# 		"server_action": "erpnext.selling.doctype.customer.customer.send_emails",
			# 		"hide_on_success": True,
			# 		"args": {
			# 			"customer": customer,
			# 			"customer_outstanding": customer_outstanding,
			# 			"credit_limit": credit_limit,
			# 			"credit_controller_users_list": credit_controller_users,
			# 		},
			# 	},
			# )
	else:
		self.custom_credit_exceeded = 0
