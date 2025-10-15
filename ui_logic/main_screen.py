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

from uis.error_msg import Ui_Dialog as ErrorUi
from .error_form import ErrorForm

from PyQt6.QtCore import pyqtSignal 

from PyQt6.QtWidgets import QComboBox
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

    # set database form button 
    def database_form(self):
        form = DatabaseForm(DatabaseUi)
        form.exec()
    def show_database_form(self):

        self.ui.set_db_btn.clicked.connect(self.database_form)

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

                   
                    """


                        find a solution "How to receive this emitted invoice type" in "invoice_form"
                        

                    """
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



        
