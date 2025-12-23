from PyQt6.QtWidgets import QHeaderView, QTableWidget
from .base_form import Form

class AnalysisForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("إحصائيات الشهر")
        
        # default settings

        incomes_table: QTableWidget = self.ui.incomes_table
        # header
        header = incomes_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        incomes_table.setColumnWidth(0, 200)
        incomes_table.verticalHeader().setDefaultSectionSize(55)


        sales_income = self.get_sales_income()
        services_income= self.get_services_income()
        customers_payments = self.get_customers_payments()
        income = float(sales_income) + float(services_income)  + float(customers_payments)

        self.remove_rows_counter(incomes_table)

        row = incomes_table.rowCount()
        

        incomes_table.insertRow(row)
        cus_pay_label = "مدفوعات الزبائن"
        incomes_table.setItem(row, 0, self.make_item(cus_pay_label))
        incomes_table.setItem(row, 1, self.make_item(f"{customers_payments:.2f}"))

        incomes_table.insertRow(row)
        services_label = "الخدمات"
        incomes_table.setItem(row, 0, self.make_item(services_label))
        incomes_table.setItem(row, 1, self.make_item(f"{services_income:.2f}"))

        incomes_table.insertRow(row)
        sales_label = "المبيعات"
        incomes_table.setItem(row, 0, self.make_item(sales_label))
        incomes_table.setItem(row, 1, self.make_item(f"{sales_income:.2f}"))

        incomes_table.insertRow(row)
        income_label = " مدخول الشهر"
        incomes_table.setItem(row, 0, self.make_item(income_label))
        incomes_table.setItem(row, 1, self.make_item(f"{income:.2f}"))






        
       


