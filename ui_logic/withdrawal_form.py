from .base_form import Form

class WithdrawalForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("سجل سحب الموظف")
        

   


