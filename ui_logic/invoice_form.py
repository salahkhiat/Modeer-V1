from .base_form import Form
from .item_form import ItemForm
from uis.item import Ui_Form as ItemUi 

from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QTableWidget
from PyQt6.QtGui import QFont 

from typing import Dict , Any 

# just for coloring logs messages
from rich.console import Console
from rich.logging import RichHandler
import logging

# Setup logging with RichHandler
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, markup=True)]
)

log = logging.getLogger("rich")
# # Green message (e.g. success)
# log.info("[green]✔ Operation successful[/green]")

# # Red message (e.g. error)
# log.error("[red]✖ Operation failed[/red]")
# ----- just to

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

        # Set  buttons
        self.ui.save_btn.setEnabled(False)
        self.ui.save_btn.setStyleSheet("background-color:grey;border:1px solid grey;")

        # Connect buttons
        self.add_item_btn_clicked()
        self.save_btn_clicked()

        # Set suppiler_id
        table = "suppliers"
        column = "name"
        combo = self.ui.users
        self.fetch_then_put(table,column,combo)

        self.supplier_id = None
        self.refresh_supplier_id()
        self.ui.users.activated.connect(self.refresh_supplier_id)

        
    def refresh_supplier_id(self):
        table = "suppliers"
        column = "name"
            # reverse dict from {1:"Ahmed", 2:"Noor"} to {"Ahmed":1, "Noor":2}
        suppliers = self.reverse_dict(self.get_table_as_dict(table,column))
        current_supplier = self.ui.users.currentText()
            # make the value as key 
        self.supplier_id = suppliers.get(current_supplier) 
        

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
        
        table.insertRow(row)
        
        table.setItem(row, 0, self.make_item(item_data['name']))
        table.setItem(row, 1, self.make_item(item_data['purchase_price']))
        table.setItem(row, 2, self.make_item(item_data['sale_price']))
        table.setItem(row, 3, self.make_item(item_data['quantity']))
        table.setItem(row, 4, self.make_item(item_data['ref']))
        
        # enable save btn
        if table.rowCount() > 0:
            self.ui.save_btn.setEnabled(True)
            self.ui.save_btn.setStyleSheet("background-color:none;")
            self.ui.save_btn.setStyleSheet("QPushButton:hover{background-color:#3f5482;border: 1px solid #3f5482}")
   

    def save_invoice_in_db(self):
        # create an invoice
        invoice_id = None
        invoice_barcode = None 
        created = self.current_date()
        if self.supplier_id is None:
            print("Sorry, You need to add suppliers first.")
        else:
            # Generate and Set an invoice barcode if it does not exist.
            while True:
                generated_barcode = str(self.generate_reference())
                if self.is_in_table("purchase_invoices","invoice_number",generated_barcode):
                    continue
                else:
                    invoice_barcode = generated_barcode
                    invoice_id = self.store("purchase_invoices",["supplier_id","invoice_number","created_at"],(self.supplier_id,invoice_barcode,created),True)
                    break
            
        table = self.ui.items_table
        products_list = {}
        # reading products data from QTableWidget and put them into products_list dictionary
        for row in range(table.rowCount()):
            row_data = {}
            for col in range(table.columnCount()):
                cell_item = table.item(row, col)
                if cell_item is not None:
                    row_data[col] = cell_item.text()
                else:
                    row_data[col] = None
            products_list[row] = row_data

        table_name = "products"
        columns = ["name","purchase_price","sale_price","quantity","barcode","invoice_id"]

        # looping through products table and save them into database
        for _ , product_info in products_list.items():
            # unpacking product info
            name, purchase_price, sale_price, quantity, barcode = product_info.values()
            data = (name, purchase_price, sale_price, quantity, barcode,str(invoice_id))

            # p_h means purchases_history
            p_h_table = "purchases_history"
            p_h_columns = ["invoice_id","product_id","product_name","barcode","quantity","purchase_price","sale_price"]
            

            # If a product is already existing in a database.
            if self.is_in_table("products","barcode",barcode):

                updated_columns = ["name", "purchase_price", "sale_price", "quantity","invoice_id"]
                updated_data = (name, purchase_price, sale_price, quantity,str(invoice_id))

                # If product info updated successfully
                if self.update_info("products",updated_columns,updated_data,"barcode = ?",(barcode,)):
                    updated_product_id = self.search_by("products","barcode",barcode,"id")

                    # If a product barcode is not existing in a database.
                    if updated_product_id is None:
                        log.error(f"[red]product:{name} with {barcode} barcode is not existing in a database.[/red]")
                        return 
                    else:
                        p_h_data = (invoice_id,updated_product_id,name,barcode,quantity,purchase_price,sale_price)
                        # If product info was not inserted into a purchases_history table
                        if self.store(p_h_table,p_h_columns,p_h_data) is not True:
                            log.error(f"[red]Product:{name} with {barcode} barcode was not inserted in purchases_table. [/red]")
                            return

                else:
                    log.error(f"[red]Product:{name} with {barcode} was not updated. [/red]")
                    return

            # If a product is not existing in a database.
            else:
                product_id = self.store(table_name,columns,data,True)
                p_h_data = (invoice_id,product_id,name,barcode,quantity,purchase_price,sale_price)
                """
                
                
                    Refine this part, then we can move to :
                    1- show an alert if something when wrong when saving an invoice.
                
                
                """
                if product_id is not False:

                    if self.store(p_h_table,p_h_columns,p_h_data) is True:
                        print(f"Product called [{name}] has inserted to [purchases_history]")
                    else:
                        print(f"Product called [{name}] does not inserted to [purchases_history]")


                    print(f"product called [{name}] has inserted to [products] ")
                    
                else:
                    print("sorry, your products never saved")

            
    def save_btn_clicked(self):
        self.ui.save_btn.clicked.connect(self.save_invoice_in_db) 


        





        