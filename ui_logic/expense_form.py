from PyQt6.QtWidgets import QComboBox, QLineEdit, QPushButton
from .base_form import Form

class ExpenseForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("تسجيل مصروف جديد")
        

        # default settings
        categories = self.get_table_as_list("expenses_categories",["name"])

        categories_combo:QComboBox = self.ui.category
        categories_combo.addItems(categories)

        current_category = categories_combo.currentText()
    
        # getting a selected employee's id, then assign it into obj.selected_employee_id.
        self.selected_category_id = self.get_item_info("expenses_categories",("id",),"name",current_category)["id"]
        categories_combo.currentTextChanged.connect(self.set_current_category_id)

        # an amount field
        self.amount: QLineEdit = self.ui.amount
        self.accept_numbers_only(self.amount)

        # a note field
        self.note: QLineEdit = self.ui.note

        # connect save button
        save_btn: QPushButton = self.ui.save_btn
        save_btn.clicked.connect(self.create_transaction)


    def set_current_category_id(self,text:str):
        """
            setting a selected category id
        """
        self.selected_category_id = self.get_item_info("expenses_categories",("id",),"name",text.strip())["id"]
        print(f"the ID of {text.strip()} is {self.selected_category_id}.")

    
    def create_transaction(self):
        valid_amount = self.is_amount("amount")
        if not valid_amount:
            print("invalid amount")
            return
        else:
            amount = float(self.ui.amount.text().strip())
            note = self.ui.note.text().strip()
            
            columns = ["category_id","note","amount","created"]
            data = (
                self.selected_category_id,
                note,
                amount,
                self.current_date()
            )
            self.store("expenses",columns,data)
            
            fields = [
                self.amount,
                self.note
            ]

            self.clear_fields(fields)
            self.close()
            self.play_success_sound()

    
        
        





        

   





