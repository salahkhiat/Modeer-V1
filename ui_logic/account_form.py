from .base_form import Form
from PyQt6.QtCore import pyqtSlot
class AccountForm(Form):
    def __init__(self,base_form, user_item_id: int=None):
        super().__init__(base_form)
        # Set form title
        self.setWindowTitle("قم بإنشاء حساب") 
        
        # Default validation values
        self.is_valid_name = False
        self.is_valid_tel = True
        if user_item_id:
            self.user_item_id = user_item_id
        print(user_item_id)
        # Filtering inputs
        telephone_field = self.ui.tel
        self.accept_numbers_only(telephone_field)

        # Validate fields.
        self.ui.name.textChanged.connect(lambda:self.update_validation_response("name","is_empty"))
        self.ui.tel.textChanged.connect(lambda:self.update_validation_response("tel","is_tel_ready"))

        # Re-validate the telephone number again when the user changes the account type.
        self.ui.account_type.activated.connect(lambda:self.update_validation_response("tel","is_tel_ready"))

        # Buttons connection
        self.save_btn_clicked()


    # save account form inputs
    def save_account_form(self) -> None:
        """
        Save an account form data in the database.
        """ 
        name = self.ui.name
        tel = self.ui.tel
        combo_index = self.get_current_combo_index('account_type')
        print(name.text())
        
        account_types = ["customers", "suppliers", "employees"]
        
        table = account_types[combo_index]
        columns = ["name", "tel"]
        data = (name.text(),tel.text())
        
        if self.is_valid_name == True and self.is_valid_tel == True:
            self.store(table, columns, data)
            fields = [name, tel]
            self.clear_fields(fields)
            self.close()
              
    def save_btn_clicked(self) -> None:
        self.ui.save_btn.clicked.connect(self.save_account_form)
        


 
