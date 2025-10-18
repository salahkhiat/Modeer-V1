from .base_form import Form
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt6.QtGui import QFont 

class ChooseItemForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        self.setWindowTitle("إختر السلعة")
        # set icons
        self.set_icon("add_btn","add_item.svg")
        self.set_icon("cancel_btn","cancel.svg")
        # database table details
        self.ui.name.textChanged.connect(lambda: self.put_data_into_table(self.get_product_name(),"name"))
        self.ui.ref.textChanged.connect(lambda: self.put_data_into_table(self.get_product_ref(),"barcode"))

        

    def get_product_name(self):
        name = self.ui.name.text().strip()
        return name
    
    def get_product_ref(self):
        ref = self.ui.ref.text().strip()
        return ref
    
    def get_product_info(self, prefix:str, column:str):
        table = "products"
        targets = ["name", "barcode", "sale_price"]
        products = self.search_by_similar(table,column,prefix,targets)
        return products


    def add_row(self,columns:list):
        table : QTableWidget = self.ui.items_table
        row_position = table.rowCount()
        table.insertRow(row_position)
        name, barcode, sale_price = columns
        """
            Set the size of table Font
        """
        # Set data in each column
        table.setItem(row_position, 0, QTableWidgetItem(str(name)))
        table.setItem(row_position, 1, QTableWidgetItem(str(barcode)))
        table.setItem(row_position, 2, QTableWidgetItem(str(sale_price)))

    def put_data_into_table(self, prefix:str, column:str):
        self.ui.items_table.setRowCount(0)

        products = self.get_product_info(prefix,column)
        for product in products :
            info = [product["name"], product["barcode"], product["sale_price"]]
            self.add_row(info)

    

    
    
    

        
        


