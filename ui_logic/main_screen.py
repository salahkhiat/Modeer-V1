from PyQt6.QtCore import Qt, QTimer

from .base_form import MainForm

from uis.database_ui import Ui_Form as DatabaseUi 
from .database_form import DatabaseForm

from uis.account import Ui_Form as AccountUi
from .account_form import AccountForm

from uis.analysis_tables import Ui_Form as AnalysisUi
from .analysis_form import AnalysisForm

from uis.mobile import Ui_Form as MobileUi
from .mobile_form import MobileForm

from uis.expense import Ui_Form as ExpenseUi 
from .expense_form import ExpenseForm

from uis.withdrawal import Ui_Form as WithdrawalUi 
from .withdrawal_form import WithdrawalForm

from uis.supplier_payment import Ui_Form as SupplierPaymentUi 
from .supplier_payment_form import SupplierPaymentForm

from uis.customer_payment import Ui_Form as CustomerPaymentUi 
from .customer_payment_form import CustomerPaymentForm

from uis.service import Ui_Form as ServiceUi
from .service_form import ServiceForm

from uis.invoice import Ui_Form as InvoiceUi 
from .invoice_form import InvoiceForm

from uis.choose_product import Ui_Form as ChooseProductUi 
from .choose_product_form import ChooseProductForm

# We used 'category' UI for requested products form because it has the same required properties.
from uis.category import Ui_Form as RequestedProductUi
from .requested_product_form import RequestedProductForm

from uis.error_msg import Ui_Dialog as ErrorUi
from .error_form import ErrorForm

from uis.editable_items import Ui_ChooseItemUi as EditableItemsUi
from .editable_items_form import EditableItemsForm

from PyQt6.QtCore import pyqtSignal 

from PyQt6.QtWidgets import QComboBox, QTableWidget, QHeaderView

from typing import Dict, List

class MainScreen(MainForm):
   
    def __init__(self,base_form):
        super().__init__(base_form)

        # Test started part ------


        
        
        
        # ------------------------

        # Set main screen title
        self.setWindowTitle("برنامج مدير لإدارة المحلات")
        
        # Set a main screen direction Right to Left
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # Set screen icons
        self.set_screen_icons()

        # connect main screen buttons with their forms
        self.show_database_form()
        self.show_account_form()
        self.show_analysis_form()
        self.show_requested_product_form()
        self.show_mobile_form()
        self.show_expense_form()
        self.show_withdrawal_form()
        self.show_supplier_payment_form()
        self.show_customer_payment_form()
        self.show_service_form()
        self.add_customer_invoice_tab()
        self.show_supplier_invoice_tab()

        # opened customers invoices list
        self.opened_customers_invoices = []
        self.opened_suppliers_invoices = []

        # create settings.json file with default information if not exists.
        if not self.is_settings_file_exists():
            self.create_settings_file(self.get_settings_json_path())

        # if database path is not selected yet, open DatabaseForm
        settings = self.get_settings_info(self.get_settings_json_path())
        database = settings["database_path"]
        if database == None:
            form = DatabaseForm(DatabaseUi)
            form.exec()
        
        # Create the default  called "-"
        self.create_default_column("customers","name")
        self.create_default_column("services_categories","name")

        # Dealing with requested_products table
        self.refresh_requested_products_table()

        # MenuBar
        users_header = ["الإسم","الهاتف","الحساب"]
        users_header_width: List[int] = [35, 35, 30]
        users_db_table_cols = ["name","tel"]

        self.ui.suppliers_action.triggered.connect(
            lambda: self.show_tab("جدول الموردين","suppliers",users_db_table_cols,users_header,users_header_width)
        )
        self.ui.customers_action.triggered.connect(
            lambda: self.show_tab("جدول الزبائن","customers",users_db_table_cols,users_header,users_header_width)
        )
        self.ui.employees_action.triggered.connect(
            lambda: self.show_tab("جدول الموظفين","employees",users_db_table_cols,users_header,users_header_width)
        )

        products_header = ["الإسم", "المرجع", "الكمية", "البيع بـ", "الشراء بـ"]
        products_header_width = [30, 20, 10, 20, 20]
        products_db_table_cols = ["name", "barcode", "quantity", "sale_price", "purchase_price"]

        self.ui.products_action.triggered.connect(
            lambda: self.show_tab("جدول السلع", "products", products_db_table_cols, products_header, products_header_width)
        )
       
    # show tab table
    def show_tab(
            self, title: str, 
            db_table: str, 
            db_table_columns: List[str], 
            headers: List[str], 
            headers_width: List[int]
    ):
        form = EditableItemsForm(EditableItemsUi)
        form.set_window_title(title)

        # Table configuration
        table: QTableWidget = form.ui.table

        QTimer.singleShot(
            0, 
            lambda: self.set_table_properties(table, headers, headers_width)
        )
        form.set_db_table_info(table, db_table,db_table_columns)
        form.exec()


    # set database form button 
    def database_form(self):
        form = DatabaseForm(DatabaseUi)
        form.exec()

    def show_database_form(self):
        self.ui.set_db_btn.clicked.connect(self.database_form)
    
    def requested_product_form(self):
        form = RequestedProductForm(RequestedProductUi)
        form.product_info.connect(self.refresh_requested_products_table)
        form.exec()
        
    

    def show_requested_product_form(self):
        self.ui.requested_products_btn.clicked.connect(self.requested_product_form)
    
    def refresh_requested_products_table(self,data:Dict=None):
        r_p_table:QTableWidget = self.ui.requested_products_table 
        r_p_table.setRowCount(0)
        self.remove_rows_counter(r_p_table)
        requested_products = None 
        if data is None:
            requested_products:Dict = self.get_table_as_dict("requested_products","name")
        else:
            requested_products = data
        header = r_p_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
       

        row = r_p_table.rowCount()

        
        for product in requested_products.values():
            r_p_table.insertRow(row)
            date_label = self.current_date()
            r_p_table.setItem(row, 0, self.make_item(product))
            r_p_table.setItem(row, 1, self.make_item(date_label)) 


    # set new user form button
    def account_form(self):
        form = AccountForm(AccountUi)
        form.exec()
    def show_account_form(self):
        self.ui.new_user_btn.clicked.connect(self.account_form)
    
    # set analysis form
    def analysis_form(self):
        form = AnalysisForm(AnalysisUi)
        form.exec()
    def show_analysis_form(self):
        self.ui.analysis_btn.clicked.connect(self.analysis_form)

    # set moblie buy mobile form
    def mobile_form(self):
        form = MobileForm(MobileUi)
        form.exec()
    def show_mobile_form(self):
        self.ui.buy_mobile_btn.clicked.connect(self.mobile_form)
    
    # set expenses form 
    def expense_form(self):
        form = ExpenseForm(ExpenseUi)
        form.exec()
    def show_expense_form(self):
        self.ui.new_expense_btn.clicked.connect(self.expense_form)

    # set withdrawal form 
    def withdrawal_form(self):
        form = WithdrawalForm(WithdrawalUi)
        form.exec()
    def show_withdrawal_form(self):
        self.ui.new_employee_withdrawal_btn.clicked.connect(self.withdrawal_form)
    
    # set supplier payment form 
    def supplier_payment_form(self):
        form = SupplierPaymentForm(SupplierPaymentUi)
        form.exec()
    def show_supplier_payment_form(self):
        self.ui.new_supplier_transaction_btn.clicked.connect(self.supplier_payment_form)

    # set customer payment form 
    def customer_payment_form(self):
        form = CustomerPaymentForm(CustomerPaymentUi)
        form.exec()
    def show_customer_payment_form(self):
        self.ui.new_customer_transaction_btn.clicked.connect(self.customer_payment_form)

    # set service form 
    def service_form(self):
        form = ServiceForm(ServiceUi)
        form.fetch_then_put("customers","name",form.ui.customer)
        form.fetch_then_put("services_categories","name",form.ui.category)
        form.exec()

    def show_service_form(self):
        self.ui.new_service_btn.clicked.connect(self.service_form)

    # add an invoice tab
    def add_invoice_tab(self,index_list,title,invoice_type=None):
                
                if len(index_list) < 3:
                    form = InvoiceForm(InvoiceUi,invoice_type) 
    
                    main_tab_widget = self.ui.tab_widget
                    # styling the active tab_bar
                    current_style = main_tab_widget.styleSheet()
                    new_style = "QTabBar::tab:selected {background-color:#3f5482;color:white;}"
                    main_tab_widget.setStyleSheet(current_style + "\n" + new_style)
                    # add a new tab 
                    tab_index = main_tab_widget.addTab(form,"")
                    # show it 
                    main_tab_widget.setCurrentIndex(tab_index)
                    # set its label
                    main_tab_widget.setTabText(tab_index,title )   
                    # add the tab invoice index to the opened inovices list 
                    index_list.append(tab_index)
                
                    # 🔑 Connect the cancel_btn to remove this tab
                    form.ui.cancel_btn.clicked.connect(lambda _, f=form: self.remove_tab_by_widget(f))

                    # ✅ Close tab when invoice is saved
                    form.invoice_saved.connect(lambda success, f=form: self.remove_tab_by_widget(f) if success else None)


                else:
                    print(f"You achieved the top, You have created {len(index_list)} Invoices")

    # remove an invoice tab index
    def remove_tab_index(self,target):
        if target in self.opened_customers_invoices:
            self.opened_customers_invoices.remove(target) 
            print(f"#{target} tab index was deleted")
            return True 
        elif target in self.opened_suppliers_invoices:
            self.opened_suppliers_invoices.remove(target)
            print(f"#{target} tab index was deleted")
            return True
        else:
            print(f"the #{target} tab index is not exists.")
            return False
        
    # remove an invoice tab
    def remove_tab_by_widget(self, widget):
        main_tab_widget = self.ui.tab_widget
        index = main_tab_widget.indexOf(widget)
        if index != -1:
            main_tab_widget.removeTab(index)
            self.remove_tab_index(index)

    # set new customer invoice tab
    def customer_invoice_tab(self):
        self.add_invoice_tab(self.opened_customers_invoices,"فاتورة الزبون ","customers")

    def add_customer_invoice_tab(self):
        self.ui.new_customer_invoice_btn.clicked.connect(self.customer_invoice_tab)

    # set new supplier invoice tab
    def supplier_invoice_tab(self):
        # Are there suppliers 
        if self.is_db_table_empty("suppliers") is True:
            msg = "ليس لديك موردين بعد"
            self.error_form = ErrorForm(ErrorUi,msg)
            self.error_form.show()
            QTimer.singleShot(2500,self.error_form.close)
            return 
        else:
            self.add_invoice_tab(self.opened_suppliers_invoices,"فاتورة المورد","suppliers")

    def show_supplier_invoice_tab(self):
        self.ui.new_supplier_invoice_btn.clicked.connect(self.supplier_invoice_tab)
    
    # Set Main Screen Icons
    def set_screen_icons(self):
        btns_icons = {
            "new_customer_invoice_btn":"add_a_sale_invoice.svg",
            "new_supplier_invoice_btn":"new_purchase_invoice.svg",
            "new_service_btn":"new_service.svg",
            "new_supplier_transaction_btn":"new_transaction_sup.svg",
            "new_customer_transaction_btn":"new_transaction_cus.svg",
            "new_employee_withdrawal_btn":"new_withdrawal.svg",
            "new_expense_btn":"new_expense.svg",
            "buy_mobile_btn":"buy_mobile.svg",
            "new_user_btn":"new_user.svg",
            "requested_products_btn":"requested_products.svg",
            "analysis_btn":"analysis.svg",
            "set_db_btn":"database.svg"
        }
        
        for btn, icon in btns_icons.items():
            self.set_icon(btn,icon)



        
