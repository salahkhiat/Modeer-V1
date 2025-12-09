from PyQt6.QtWidgets import QComboBox
from .base_form import Form

class CustomerPaymentForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("إيداع جديد")

        # default settings
        customers_combo:QComboBox = self.ui.customer
        customers = self.get_table_as_list("customers",["name"])
        customers.pop(customers.index("-"))
        customers_combo.addItems(customers)

        custmoers_dict = self.get_table_as_dict("customers","name")
        print(custmoers_dict)
        
        




