frappe.ui.form.on("Opportunity", {
    refresh: function(frm){
        frm.set_query('item_code', 'items', function(doc, cdt, cdn){
            let row = locals[cdt][cdn]
            let value={}
            if (row.item_group){
                value["item_group"]= row.item_group
            }
            if (row.brand){
                value["brand"]= row.brand
            }
            if (row.custom_category){
                value["custom_category"]= row.custom_category
            }
			return{
				"filters":value
			} 
        });
    }
})