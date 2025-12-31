from PyQt6.QtWidgets import QHeaderView, QTableWidget
from .base_form import Form

class AnalysisForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("إحصائيات الشهر")
        # set icon
        self.set_icon("switch_analysis_btn","refresh.svg")

        self.get_analysis()
        

    def get_analysis(self,s_date:str="today"):
        """ Getting analysis depending on search date or s_date 'today' or 'month' """

        # incomes
        incomes_table: QTableWidget = self.ui.incomes_table
            # headers
        header = incomes_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        incomes_table.setColumnWidth(0, 240)
        # incomes_table.verticalHeader().setDefaultSectionSize(55)
        incomes_table.verticalHeader().setDefaultSectionSize(45)

        sales_income = self.get_sales_income(s_date)
        services_income= self.get_services_income(s_date)
        customers_payments = self.get_customers_payments(s_date)
        income = float(sales_income) + float(services_income)  + float(customers_payments)
        sales_capital = self.get_sales_capital(s_date)
        sales_profit = sales_income - sales_capital
        month_profit = sales_profit + services_income
        """
        
        
        Start working from this Area
        
        """


        self.remove_rows_counter(incomes_table)

        row = incomes_table.rowCount()


        incomes_table.insertRow(row)
        income_label = "الدخل الإجمالي"
        incomes_table.setItem(row, 0, self.make_item(income_label))
        incomes_table.setItem(row, 1, self.make_item(f"{income:.2f}"))

        incomes_table.insertRow(row)
        month_profit_label = "الربح الإجمالي "
        incomes_table.setItem(row, 0, self.make_item(month_profit_label,color="green"))
        incomes_table.setItem(row, 1, self.make_item(f"{month_profit:.2f}",color="green"))


        
        # incomes_table.insertRow(row)
        # cus_pay_label = " إداعات الزبون المميز"
        # incomes_table.setItem(row, 0, self.make_item(cus_pay_label))
        # incomes_table.setItem(row, 1, self.make_item(f"{customers_payments:.2f}"))

        incomes_table.insertRow(row)
        services_label = "أرباح الخدمات "
        incomes_table.setItem(row, 0, self.make_item(services_label))
        incomes_table.setItem(row, 1, self.make_item(f"{services_income:.2f}"))

        incomes_table.insertRow(row)
        sales_profit_label = "أرباح السلع"
        incomes_table.setItem(row, 0, self.make_item(sales_profit_label))
        incomes_table.setItem(row, 1, self.make_item(f"{sales_profit:.2f}"))

        incomes_table.insertRow(row)
        capital_label = "رأس مال المبيعات"
        incomes_table.setItem(row, 0, self.make_item(capital_label))
        incomes_table.setItem(row, 1, self.make_item(f"{sales_capital:.2f}"))



        # expenses
        expenses_table: QTableWidget = self.ui.expenses_table
        ex_header = expenses_table.horizontalHeader()
        ex_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        expenses_table.setColumnWidth(0, 250)
        expenses_table.verticalHeader().setDefaultSectionSize(45)

        self.remove_rows_counter(expenses_table)
        row = expenses_table.rowCount()

        month_expenses = self.get_expenses()
        mo_purchases_deposits = self.get_monthly_purchases_deposits()
        monthly_sup_deposits = self.get_monthly_suppliers_deposits()
        monthly_sup_debts = self.get_monthly_suppliers_debts()
        monthly_emp_withdrawals = self.get_monthly_employees_withdrawals()
        monthly_sup_new_debts = monthly_sup_debts - monthly_sup_deposits
        outcome = month_expenses + monthly_sup_deposits + mo_purchases_deposits + monthly_emp_withdrawals

        expenses_table.insertRow(row)
        total_ex_label = "الخرج الإجمالي"
        expenses_table.setItem(row, 0, self.make_item(total_ex_label))
        expenses_table.setItem(row, 1, self.make_item(f"{outcome:.2f}"))

        expenses_table.insertRow(row)
        ex_label = " مصاريف عامة"
        expenses_table.setItem(row, 0, self.make_item(ex_label))
        expenses_table.setItem(row, 1, self.make_item(f"{month_expenses:.2f}"))

        expenses_table.insertRow(row)
        mo_purchases_deposits_label = "مشتريات سلع"
        expenses_table.setItem(row, 0, self.make_item(mo_purchases_deposits_label))
        expenses_table.setItem(row, 1, self.make_item(f"{mo_purchases_deposits:.2f}"))

        expenses_table.insertRow(row)
        mo_sup_deposits_label = "إيداعاتي للموردين"
        expenses_table.setItem(row, 0, self.make_item(mo_sup_deposits_label))
        expenses_table.setItem(row, 1, self.make_item(f"{monthly_sup_deposits:.2f}"))

        expenses_table.insertRow(row)
        mo_sup_debts_label = "دين جديد - الموردين"
        expenses_table.setItem(row, 0, self.make_item(mo_sup_debts_label))
        expenses_table.setItem(row, 1, self.make_item(f"{monthly_sup_new_debts:.2f}"))

        expenses_table.insertRow(row)
        mo_emp_withdrawals_label = "سحوبات  العمال "
        expenses_table.setItem(row, 0, self.make_item(mo_emp_withdrawals_label))
        expenses_table.setItem(row, 1, self.make_item(f"{monthly_emp_withdrawals:.2f}"))


        # cunclution 
        net_result = income - outcome

        incomes_table.insertRow(row)
        net_result_label = "الصافي "
        color = "green"
        if net_result < 0:
            color = "red"
        incomes_table.setItem(row, 0, self.make_item(net_result_label,color=color))
        incomes_table.setItem(row, 1, self.make_item(f"{net_result:.2f}",color=color))







        
       


