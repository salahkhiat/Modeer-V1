from .base_form import Form

from PyQt6.QtCore import pyqtSignal

class ItemForm(Form):

    item_added = pyqtSignal(dict)
    
    def __init__(self,base_form):
        super().__init__(base_form)


        self.setWindowTitle("إدخال معلومات السلعة")
        # set icons
        self.set_icon("add_btn","add.svg")

        self.add_item_btn_clicked()
        # Validation
        self.is_valid_name = False
        self.is_valid_purchase_price = False
        self.is_valid_sale_price = False 
        self.is_valid_quantity = False 
        self.is_valid_ref = False

    
    def add_item_to_invoice(self):

        item_details = {
            'name': self.ui.name.text(),
            'purchase_price': self.ui.purchase_price.text(),
            'sale_price': self.ui.sale_price.text(),
            'quantity': self.ui.quantity.text(),
            'ref': self.ui.ref.text().strip(),
        }

        # False means Empty
        if not self.is_empty("ref",False) :
            pass
            
        self.item_added.emit(item_details)
        self.close()


    def add_item_btn_clicked(self):
        self.ui.add_btn.clicked.connect(lambda: self.add_item_to_invoice())

        
 
        