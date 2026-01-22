from .base_form import Form
from typing import List, Any 
from PyQt6.QtWidgets import QComboBox, QTableWidget, QHeaderView

class EditableItemsForm(Form):

    def __init__(self,base_form):
        super().__init__(base_form)
        # set icons
        self.set_icon("edit_btn","edit.svg")
        self.set_icon("delete_btn","delete.svg")
        
    def set_db_table_info(
        self,
        table_widget: QTableWidget, 
        db_table: str, 
        columns: List[str],
        font_size: int = 16
    ) -> None:
        items = self.get_table_cols_list(db_table, columns)

        # Make the columns of Qt meet the db_table.
        table_widget.setColumnCount(len(columns)) 

        for item in items:
            item = list(item)

            if db_table == "suppliers":
                balance = self.calculate_balance("supplier", item[0])
                item.pop(0)
                item.append(balance)

            # where the next row should go
            row = table_widget.rowCount() 

            # insert new row at the bottom of the table
            table_widget.insertRow(row) 

            for col_id, col_info in enumerate(item):
                    table_item = self.make_item(col_info, font_size=font_size)
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
        
    def set_window_title(self,title):
        self.setWindowTitle(title)

   



        