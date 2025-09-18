from .base_form import Form

from PyQt6.QtCore import pyqtSignal
from typing import List,Dict 



class ItemForm(Form):
    item_added = pyqtSignal(dict)
    def __init__(self,base_form):
        super().__init__(base_form)
        self.setWindowTitle("إدخال معلومات السلعة")
        # set icons
        self.set_icon("add_btn","add.svg")

        self.add_item_btn_clicked()

        # accept only digits
        self.accept_numbers_only(self.ui.ref)
        self.accept_numbers_only(self.ui.quantity)
        self.accept_numbers_only(self.ui.purchase_price)
        self.accept_numbers_only(self.ui.sale_price)
        
        # Validation
        self.is_valid_name = False
        self.is_valid_purchase_price = False
        self.is_valid_sale_price = False 
        self.is_valid_quantity = False 
        self.is_valid_ref = False
    
    def set_table_refs(self,table_refs:List):
        self.table_references_list = table_refs

    def add_item_to_invoice(self):
        
        item_details = {
            'name': self.ui.name.text(),
            'purchase_price': self.ui.purchase_price.text(),
            'sale_price': self.ui.sale_price.text(),
            'quantity': self.ui.quantity.text(),
            'ref': self.ui.ref.text().strip(),
        }

        # if a reference field is Empty.
        if not self.is_empty("ref",err_msg=False) :  # False means Empty, If Empty do this part.
            
            print("a reference will be generated automatically ...")
            while True:
                # step 1: generate a reference.
                generated_ref = str(self.generate_reference())

                # step 2: check if a reference is in the database, if yes, regenerate it and recheck.
                if self.is_in_table("product","barcode",generated_ref):
                    continue
                
                # if a reference is not in the database.
                else:
                    # if the invoice table widget is Empty.
                    if len(self.table_references_list) == 0:
                        item_details['ref'] = generated_ref
                        self.item_added.emit(item_details)
                        self.close()
                        break

                    # check if the invoice table widget is not empty.
                    elif len(self.table_references_list) > 0:
                        # step 3: check if a reference is in the invoice table widget, if yes, regenerate and recheck. 
                        if generated_ref in self.table_references_list:
                            continue
                        else:
                            item_details['ref'] = generated_ref
                            self.item_added.emit(item_details)
                            self.close()
                            break
        # if a reference field is not empty.
        else:
            ref = item_details['ref']
            err_msg = "المرجع مستخدم مسبقا"

            # step 1: Check if a reference in the database, if yes, ask the use to retry.
            if self.is_in_table("product","barcode",ref):
                self.set_err_msg("ref",err_msg)

            # if a reference is not in the database:
            else:
                # if the invoice table widget is empty.
                if len(self.table_references_list) == 0:
                    if item_details['ref'].strip() != "":
                            self.item_added.emit(item_details)
                            self.close()

                # if the invoice table widget is not empty.
                if len(self.table_references_list) > 0:

                    # Step 2: Check if a reference in the invoice table widget, if yes, ask the user to retry.
                    if ref in self.table_references_list:
                        self.set_err_msg("ref",err_msg)

                    # Check if a reference is not in the invoice table widget, then it is valid
                    else: 
                        if item_details['ref'].strip() != "":
                            self.item_added.emit(item_details)
                            self.close()
                    
    def add_item_btn_clicked(self):
        self.ui.add_btn.clicked.connect(lambda: self.add_item_to_invoice())

        
 
        