import frappe
import requests

def on_submit(doc,event):
    site_url = 'https://sujeethaenterprises.thirvusoft.co.in'

    url = f'''{site_url}/api/method/sujeetha_enterprises.sujeetha_enterprises.utils.py.sales_invoice.sales_invoice_creation'''

    payload = {}
    headers = {
          'Authorization': 'token 394d20266ee54ff:da6aa4687b4e5c6',
          'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image='
        }

    response = requests.request("GET", url, headers=headers, data=payload)

    frappe.log_error(response)
