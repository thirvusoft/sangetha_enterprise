frappe.ui.form.on("Opportunity", {
    refresh: function(frm) {
        frm.set_query('item_code',"items", function(doc){
            let value={}
            if (frm.doc.custom_item_group){
                value["item_group"]= frm.doc.custom_item_group
            }
            if (frm.doc.custom_brand){
                value["brand"]= frm.doc.custom_brand
            }
            if (frm.doc.custom_category){
                value["custom_category"]= frm.doc.custom_category
            }
			return{
				"filters":value
			}
		});

    }
})