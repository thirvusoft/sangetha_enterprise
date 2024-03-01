frappe.ui.form.on("Sales Invoice Item", {
    qty: function(frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        frappe.call({
            method:'sangetha_enterprise.sangeetha_enterprise.utils.py.sales_invoice.get_margin_rate',
            args:{
                'item_code':row.item_code,
                'rate':row.rate
            },
            callback:function(res){
                console.log(res.message)
                frappe.model.set_value(row.doctype,row.name,'custom_lowest_margin_rate',res.message.custom_lowest_margin_rate)
                frappe.model.set_value(row.doctype,row.name,'custom_lowest_margin',res.message.custom_lowest_margin)
                frappe.model.set_value(row.doctype,row.name,'custom_highest_margin_rate',res.message.custom_highest_margin_rate)
                frappe.model.set_value(row.doctype,row.name,'custom_highest_margin',res.message.custom_highest_margin)
            }
        })
    },
    rate:function(frm,cdt,cdn) {
        let row = locals[cdt][cdn]
        frappe.call({
            method:'sangetha_enterprise.sangeetha_enterprise.utils.py.sales_invoice.get_margin_rate',
            args:{
                'item_code':row.item_code,
                'rate':row.rate
            },
            callback:function(res){
                frappe.model.set_value(row.doctype,row.name,'custom_lowest_margin_rate',res.message.custom_lowest_margin_rate)
                frappe.model.set_value(row.doctype,row.name,'custom_lowest_margin',res.message.custom_lowest_margin)
                frappe.model.set_value(row.doctype,row.name,'custom_highest_margin_rate',res.message.custom_highest_margin_rate)
                frappe.model.set_value(row.doctype,row.name,'custom_highest_margin',res.message.custom_highest_margin)

            }
        })
    },
    item_code:function(frm,cdt,cdn) {
        setTimeout(() => {
            let row = locals[cdt][cdn]
            if(row.item_code){
                frappe.call({
                    method:'sangetha_enterprise.sangeetha_enterprise.utils.py.sales_invoice.get_margin_rate',
                    args:{
                        'item_code':row.item_code,
                        'rate':row.rate
                    },
                    callback:function(res){
                        frappe.model.set_value(row.doctype,row.name,'custom_lowest_margin_rate',res.message.custom_lowest_margin_rate)
                        frappe.model.set_value(row.doctype,row.name,'custom_lowest_margin',res.message.custom_lowest_margin)
                        frappe.model.set_value(row.doctype,row.name,'custom_highest_margin_rate',res.message.custom_highest_margin_rate)
                        frappe.model.set_value(row.doctype,row.name,'custom_highest_margin',res.message.custom_highest_margin)
        
                    }
                })
            }
        }, 150);
            
    },

})