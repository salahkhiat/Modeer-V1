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
    ):
        items = self.get_table_cols_list(db_table,columns)
        table_widget.setColumnCount(len(columns)) # make the columns of Qt meet the db_table.

        for item in items:
            row = table_widget.rowCount() # where the next row should go
            table_widget.insertRow(row) # insert new row at the bottom of the table
            for col_id, col_info in enumerate(item):
                table_widget.setItem(row, col_id, self.make_item(col_info,font_size=font_size))

    def set_window_title(self,title):
        self.setWindowTitle(title)

   



        