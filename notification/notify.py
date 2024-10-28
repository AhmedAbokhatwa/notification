import frappe
from frappe.utils import add_days, add_months, format_date, getdate, today


# # from frappe.desk.notifications import
# do bench migrate and excute it
# @frappe.whitelist()
def send_notification():
    emails = ["shaymaa@dmc.com", "ahmed.atef@gmail.com"]
    msg = "please make Sales Order"
    for email in emails:
        users = frappe.get_all(
            "Employee",
            fields=["name"],
            filters={"user_id": email},
        )
        for user in users:
            table = frappe.get_all(
                "Comprehensive Health Insurance",
                filters={"parent": user.name, "parenttype": "Employee"},
                fields=["renewal_date", "parent"],
            )
            print("tab :", table[0]["renewal_date"], getdate(today()))
            for row in table:
                if row["renewal_date"] == getdate(today()):
                    try:
                        notification = frappe.new_doc("Notification Log")
                        notification.for_user = email
                        notification.set("type", "Alert")
                        notification.document_type = "User"
                        notification.document_name = email
                        notification.subject = msg
                        notification.insert()
                    except Exception:
                        frappe.msgprint("Failed to send reminder")
