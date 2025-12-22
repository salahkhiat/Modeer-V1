from PyQt6.QtWidgets import QHeaderView, QTableWidget


from .base_form import Form

class AnalysisForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("إحصائيات الشهر")
        
        # default

        incomes_table: QTableWidget = self.ui.incomes_table
        # header
        header = incomes_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        incomes_table.setColumnWidth(0, 160)

        sales_income = self.get_sales_income()
        services_income= self.get_services_income()
        income = float(sales_income) + float(services_income) 

        row = incomes_table.rowCount()
        incomes_table.insertRow(row)
        self.remove_rows_counter(incomes_table)
        income_label = "دخل الشهر"
        incomes_table.setItem(row, 0, self.make_item(income_label))
        incomes_table.setItem(row, 1, self.make_item(f"{income:.2f}"))




        
       


