from .base_form import Form

from uis.item import Ui_Form as ItemUi
from .item_form import ItemForm

from uis.choose_item import Ui_ChooseItemUi as ChooseItemUi
from .choose_item_form import ChooseItemForm

from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QTableWidget
from PyQt6.QtGui import QFont 
from PyQt6.QtCore import pyqtSignal 

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
    invoice_saved = pyqtSignal(bool)

    def __init__(self,base_form, invoice_type:str):
        super().__init__(base_form)

        # set invoice type
        self.invoice_type = invoice_type
        print(self.invoice_type)
        # set icons
        self.set_icon("add_item_btn","add.svg")
        self.set_icon("clear_btn","refresh.svg")

        # Invoice table details
        self.table = invoice_type
        self.column = "name"
        self.invoice_total = 0 

        # test

        # Set column count and headers for items_table
        items_table : QTableWidget = self.ui.items_table 

        # remove rows counter
        self.remove_rows_counter(items_table)
        
        if invoice_type == "suppliers":
            items_table.setColumnCount(5)

            # Define headers and font
            headers = ["الإسم", "الشراء بـ", "البيع بـ", "الكمية", "المرجع"]
            header_font = QFont()
            header_font.setPointSize(16)
            header_font.setBold(True)

            # Set each header item with font
            for i, title in enumerate(headers):
                item = QTableWidgetItem(title)
                item.setFont(header_font)
                items_table.setHorizontalHeaderItem(i, item)
            # set table header
            header = items_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            for col in range(1, 5):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
                if col != 4:
                    items_table.setColumnWidth(col, 140)
                else:
                    items_table.setColumnWidth(col, 200)



        elif invoice_type == "customers": 
            items_table.setColumnCount(4)

            # Define headers and font
            headers = ["الإسم", "البيع بـ", "الكمية", "المرجع"]
            header_font = QFont()
            header_font.setPointSize(16)
            header_font.setBold(True)

            # Set each header item with font
            for i, title in enumerate(headers):
                item = QTableWidgetItem(title)
                item.setFont(header_font)
                items_table.setHorizontalHeaderItem(i, item)
            # set table header
            header = self.ui.items_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            for col in range(1, 4):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
                if col != 3:
                    self.ui.items_table.setColumnWidth(col, 140)
                else:
                    self.ui.items_table.setColumnWidth(col, 200)
        else:
            log.error(f"{invoice_type} invoice_type is unknown")


        # Set  buttons
        self.ui.save_btn.setEnabled(False)
        self.ui.save_btn.setStyleSheet("background-color:grey;border:1px solid grey;")
        self.clear_btn_clicked()

        # Connect buttons
        self.add_item_btn_clicked()
        self.save_btn_clicked()

        # put users customers/suppliers into a Combo
        self.put_users_on_combo()

        # Set suppiler_id/customer_id
        self.supplier_id = None
        self.refresh_user_id()
        self.ui.users.activated.connect(self.refresh_user_id)
        
        # accept only numbers in amount field.
        self.accept_numbers_only(self.ui.amount)

    def put_users_on_combo(self):
        combo = self.ui.users
        self.fetch_then_put(self.table,self.column,combo)

    def refresh_user_id(self):
            # reverse dict from {1:"Ahmed", 2:"Noor"} to {"Ahmed":1, "Noor":2}
        users = self.reverse_dict(self.get_table_as_dict(self.table,self.column))
        current_user = self.ui.users.currentText()
            # make the value as key 
        self.user_id = users.get(current_user) 

    def refresh_invoice(self):
        # clear table 
        table : QTableWidget = self.ui.items_table
        table.setRowCount(0)
        # clear deposit
        self.ui.amount.clear() 
        # clear invoice total
        self.invoice_total = 0 
        self.ui.total.display(0)
        
    def clear_btn_clicked(self):
        self.ui.clear_btn.clicked.connect(self.refresh_invoice)

    def show_item_form(self):
        form = None 
        if self.table == "suppliers":
            form = ItemForm(ItemUi)
            form.item_added.connect(self.add_item_to_table)
            referenses_list = self.q_table_column_as_list(self.ui.items_table,4)
            form.set_table_refs(referenses_list)

        elif self.table == "customers":
            form = ChooseItemForm(ChooseItemUi)
            form.item_barcode_sent.connect(self.add_item_to_cus_invoice)
        form.exec()

    def add_item_to_cus_invoice(self,barcode):
        table = "products"
        columns = ("name", "sale_price", "quantity", "barcode")
        keyword = "barcode"
        target = barcode
        product_info : dict = self.get_item_info(table, columns, keyword, target)
        row = [ value for value in product_info.values()]
        row[2]=1
        qtable : QTableWidget = self.ui.items_table
        self.add_list_in_qtable(qtable, row)
        

        """
        
            Get an item information from database, name, sale_price, quatity, barcode.
            put them in an invoice table row
        
        """
   

    
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
        # calculates total
        p_price = item_data["purchase_price"]
        qt = item_data["quantity"]
        self.invoice_total += self.calculate_total(p_price, qt)
        self.ui.total.display(self.invoice_total)
        
        table.setItem(row, 0, self.make_item(item_data['name']))
        if self.invoice_type == "suppliers":
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
        invoice_deposit = "0" if self.ui.amount.text() == "" else self.ui.amount.text()
        created = self.current_date()
        
        table : QTableWidget = self.ui.items_table
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

        # Calculates an invoice total.
        invoice_total = 0 
        for _ , product_info in products_list.items():
            invoice_total += int(product_info[1]) * int(product_info[3]) # purchase_price * quantity

        # Generates an invoice.
        if self.user_id is None:
            log.error("[red]Sorry, You need to add suppliers first.[/red]")
        else:
            # Generate and Set an invoice barcode if it does not exist.
            while True:
                generated_barcode = str(self.generate_reference())
                if self.is_in_table("purchase_invoices","invoice_number",generated_barcode):
                    continue
                else:
                    invoice_barcode = generated_barcode
                    invoice_id = self.store("purchase_invoices",["supplier_id","invoice_number","total","deposit","created_at"],(self.user_id,invoice_barcode,str(invoice_total),invoice_deposit,created),True)
                    break
        
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
    
                if product_id is False:
                    log.error(f"[red]Product:{name} with {barcode} was not inserted into products table.[/red]")
                    return
                else:
                    if self.store(p_h_table,p_h_columns,p_h_data) is False:
                        log.error(f"[red]Product:{name} with barcode {barcode} was not inserted into purchases_history [/red]")
                        return 
                    

        self.play_success_sound()  
        self.invoice_saved.emit(True)           


            
    def save_btn_clicked(self):
        self.ui.save_btn.clicked.connect(self.save_invoice_in_db) 


        





        