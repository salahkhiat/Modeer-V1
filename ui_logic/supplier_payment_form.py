from PyQt6.QtWidgets import QComboBox
from .base_form import Form

class SupplierPaymentForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("إيداع أو دين جديد")
        # default 
        self.selected_supplier_id = 0

        # get suppliers
        suppliers_combo:QComboBox = self.ui.supplier
        self.fetch_then_put("suppliers","name",suppliers_combo)
        current_supplier = suppliers_combo.currentText()

        suppliers_combo.currentTextChanged.connect(self.get_current_combo_text)

    

    def get_current_combo_text(self,text:str):
        """
            get a supplier id depending on a name
        """
        
        

        




