from PyQt6.QtWidgets import QTableWidgetItem

from .base_form import Form

class AnalysisForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("إحصائيات الشهر")
        
        # default
        self.incomes_table = self.ui.incomes_table

        income = self.get_sales_income()

        row = self.incomes_table.rowCount()
        self.incomes_table.insertRow(row)

        self.incomes_table.setItem(row, 0, QTableWidgetItem("Sales income"))
        self.incomes_table.setItem(row, 1, QTableWidgetItem(f"{income:.2f}"))
        
       


