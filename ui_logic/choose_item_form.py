from .base_form import Form
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView
from PyQt6.QtGui import QFont 

class ChooseItemForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        self.setWindowTitle("إختر السلعة")
        # set icons
        self.set_icon("add_btn","add_item.svg")
        self.set_icon("cancel_btn","cancel.svg")
        # setup table 
        self.setup_table_columns()
        table : QTableWidget = self.ui.items_table
        self.remove_rows_counter(table)

        self.make_row_scrollable(table,1)
        # database table details
        self.ui.name.textChanged.connect(lambda: self.put_data_into_table(self.get_product_name(),"name"))
        self.ui.ref.textChanged.connect(lambda: self.put_data_into_table(self.get_product_ref(),"barcode"))

    def setup_table_columns(self):
        table: QTableWidget = self.ui.items_table
        
        header = table.horizontalHeader()
        
        # Column 0: stretch (name)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        # Column 1: fixed width
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        table.setColumnWidth(1, 120)

        # Column 2: fixed width
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        table.setColumnWidth(2, 120)


        

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


        # Set the size of table Font
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)

        # Create and set items with the font
        for col, value in enumerate([name, barcode, sale_price]):
            item = QTableWidgetItem(str(value))
            item.setFont(header_font)
        
            table.setItem(row_position, col, item)


 








    def put_data_into_table(self, prefix:str, column:str):
        self.ui.items_table.setRowCount(0)

        products = self.get_product_info(prefix,column)
        for product in products :
            info = [product["name"], product["barcode"], product["sale_price"]]
            self.add_row(info)

    

    
    
    

        
        


