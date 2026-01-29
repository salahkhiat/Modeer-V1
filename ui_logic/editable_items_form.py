from .base_form import Form
from typing import List, Any 
from PyQt6.QtWidgets import  QTableWidget, QLineEdit, QComboBox
from PyQt6.QtCore import Qt, QTimer

from .account_form import AccountForm
from uis.account import Ui_Form as AccountFormUi

from .item_form import ItemForm
from uis.item import Ui_Form as ItemFormUi

from .error_form import ErrorForm
from uis.error_msg import Ui_Dialog as ErrorFormUi

class EditableItemsForm(Form):

    def __init__(self,base_form):
        super().__init__(base_form)
        # set icons
        self.set_icon("edit_btn","edit.svg")
        self.set_icon("delete_btn","delete.svg")

        # default settings
        self.qt_table: QTableWidget = self.ui.table 
        self.db_table: str = None
        self.columns: List = None 
        self.item_id: int = None 

        self.update_variable_on_row_select(self.qt_table, "item_id", 0)

        # obj.column for database searchs purposes : SELECT column FROM ...
        self.column: str = "name" 
        
        # Search box
        search_box: QLineEdit = self.ui.search_box
        search_box.textChanged.connect(self.search_box)

        # connect buttons
        self.ui.edit_btn.clicked.connect(self.edit_item_info)
        
    def set_db_table_info(
        self,
        table_widget: QTableWidget, 
        db_table: str, 
        columns: List[str],
        font_size: int = 16,
        data = None
    ) -> None:
        
        # set default table data
        self.qt_table = table_widget
        self.db_table = db_table
        self.columns = columns
        self.variable = None 

        items = None
        if data == None:
            items = self.get_table_cols_list(db_table, columns)
        else:
            items = data
        
        account_types = ["suppliers", "customers", "employees"]

        if  db_table in account_types:
            # Make the columns of Qt meet the db_table.
            table_widget.setColumnCount(len(columns)+1) 
        else:
            table_widget.setColumnCount(len(columns)) 

        for item in items:
            item = list(item)
            if db_table == "suppliers":
                balance = self.calculate_balance("supplier", item[0])
                item.append(balance)
    
            # where the next row should go
            row = table_widget.rowCount() 
            
            # insert new row at the bottom of the table
            table_widget.insertRow(row) 

            for col_id, col_info in enumerate(item):
                    table_item = self.make_item(col_info, font_size=font_size, read_only=True)
                    table_widget.setItem(row, col_id, table_item)
    

    def calculate_balance(self, account_type: str, user_id: int) -> float:
        if account_type == "supplier":
            transactions_deposits = self.get_supplier_transactions_sum("deposit", user_id)
            purchases_deposits = self.get_supplier_purchase_sum("deposit", user_id)
            deposits = transactions_deposits + purchases_deposits

            transactions_debts = self.get_supplier_transactions_sum("debt", user_id)
            purchases_total = self.get_supplier_purchase_sum("total", user_id)
            debts = transactions_debts + purchases_total
            
            return debts - deposits
        raise ValueError(f"Unsupported account type: {account_type}")
    
    def search_box(self, search_word: str) -> None:
        self.qt_table.setRowCount(0)
        search_word = str(search_word).strip()

        items = self.search_by_similar(
            self.db_table, self.column, search_word, self.columns
        )
        data = [ tuple(item.values()) for item in items]

        self.set_db_table_info(self.qt_table, self.db_table, self.columns, 16, data)

    def edit_item_info(self):

        if self.item_id is None:
            print("you didn't select an item yet")
            return 
        
        # When tables are suppliers, customers, employees
        users_table = ["suppliers", "customers", "employees"]

        if self.db_table in users_table:
            user_info = self.get_item_info(
                self.db_table,
                ("name", "tel"),
                "id",
                self.item_id
            )
       
            form = AccountForm(AccountFormUi)
            form.ui.name.setText(user_info["name"])
            form.ui.tel.setText(user_info["tel"])

            account_placeholder = {
                "suppliers": "مورد",
                "customers": "زبون",
                "employees": "عامل"
            }
            form.ui.account_type.setItemText(0, account_placeholder[self.db_table])
            form.ui.account_type.setEnabled(False)
            form.exec()
        
        # When table is products
        if self.db_table == "products":
            product_information = self.get_item_info(
                self.db_table,
                (
                    "barcode", 
                    "name", 
                    "quantity", 
                    "sale_price", 
                    "purchase_price"
                ),
                "barcode",
                self.item_id
            )
            product_info = product_information.values()
            barcode, name, quantity, sale_price, purchase_price = product_info
        
            form = ItemForm(ItemFormUi)

            form.ui.title.setText(name)
            form.ui.ref.setText(barcode)
            form.ui.name.setText(name)
            form.ui.quantity.setText(str(quantity))
            form.ui.purchase_price.setText(purchase_price)
            # form.ui.sale_price.setText(str(sale_price))
            
            form.exec()
            
        
            
            
            
            
              
              
              
              
              

        
        
    def set_window_title(self,title):
        self.setWindowTitle(title)

   



        