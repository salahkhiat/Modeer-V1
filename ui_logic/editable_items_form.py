from .base_form import Form
from typing import List 
from PyQt6.QtWidgets import QComboBox, QTableWidget, QHeaderView
class EditableItemsForm(Form):

    def __init__(self,base_form):
        super().__init__(base_form)
        # set icons
        self.set_icon("edit_btn","edit.svg")
        self.set_icon("delete_btn","delete.svg")


            
    def set_table_info(self, table:str, columns:List[str]):

        users = self.get_table_cols_dict(table,columns)
        
        form_table:QTableWidget = self.ui.table
        self.remove_rows_counter(form_table)
        
        form_table.setRowCount(0)
        row = form_table.rowCount()
        for user in users:
            name, tel = user
            form_table.insertRow(row)
            form_table.setItem(row, 0, self.make_item(name))
            form_table.setItem(row, 1, self.make_item(tel))


    def set_window_title(self,title):
        self.setWindowTitle(title)

    def set_table_headers(self, headers:List[str]=["test1","test2"]):
        table = self.ui.table
        self.set_table(table,headers)


        