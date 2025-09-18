from .base_form import Form
from .item_form import ItemForm
from uis.item import Ui_Form as ItemUi 

from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QTableWidget
from PyQt6.QtGui import QFont 


from typing import Dict , Any 

class InvoiceForm(Form):

    def __init__(self,base_form):
        super().__init__(base_form)
        # set icons
        self.set_icon("add_item_btn","add.svg")
        self.set_icon("clear_btn","refresh.svg")

        # set table header
        header = self.ui.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 5):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
            if col != 4:
                self.ui.items_table.setColumnWidth(col, 140)
            else:
                self.ui.items_table.setColumnWidth(col, 200)
        # Remove the IDs of the added rows.
        self.ui.items_table.verticalHeader().setVisible(False)



        # connect buttons
        self.add_item_btn_clicked()
    
    
    def show_item_form(self):

        form = ItemForm(ItemUi)
        form.item_added.connect(self.add_item_to_table)
        referenses_list = self.q_table_column_as_list(self.ui.items_table,4)
        form.set_table_refs(referenses_list)
        form.exec()
    
    def add_item_btn_clicked(self):
        self.ui.add_item_btn.clicked.connect( lambda: self.show_item_form())

    def make_item(self,text, font_size=18, bold=True):
        item = QTableWidgetItem(text)
        font = QFont()
        font.setPointSize(font_size)
        font.setBold(bold)
        item.setFont(font)
        return item

    def add_item_to_table(self,item_data:Dict[Any,Any]):
        table = self.ui.items_table
        row = table.rowCount()


        # add 
        table.insertRow(row)
        
        table.setItem(row, 0, self.make_item(item_data['name']))
        table.setItem(row, 1, self.make_item(item_data['purchase_price']))
        table.setItem(row, 2, self.make_item(item_data['sale_price']))
        table.setItem(row, 3, self.make_item(item_data['quantity']))
        table.setItem(row, 4, self.make_item(item_data['ref']))



        