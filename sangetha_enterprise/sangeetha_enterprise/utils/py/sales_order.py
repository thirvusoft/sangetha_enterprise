import frappe
import requests


def on_submit(doc,event):
	# site = "https://sujeethaenterprises.thirvusoft.co.in"
	
	url = f'''https://sujeethaenterprises.thirvusoft.co.in/api/method/sujeetha_enterprises.sujeetha_enterprises.utils.py.purchase_invoice.purchase_invoice_creation'''

	payload = {}
	headers = {
		        'Authorization': 'token 394d20266ee54ff:d56ec5a6aebaf73',
				'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image='
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	frappe.log_error(title='lok',message=url)
