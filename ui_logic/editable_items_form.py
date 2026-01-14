from .base_form import Form
from typing import List 
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
            columns: List[str]
    ):
        users = self.get_table_cols_dict(db_table,columns)
        
        table_widget.setRowCount(0)
        row = table_widget.rowCount()
        for user in users:
            name, tel = user
            table_widget.insertRow(row)
            table_widget.setItem(row, 0, self.make_item(name))
            table_widget.setItem(row, 1, self.make_item(tel))


    def set_window_title(self,title):
        self.setWindowTitle(title)

   



        