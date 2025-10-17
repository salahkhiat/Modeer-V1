from .base_form import Form

class ChooseItemForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        self.setWindowTitle("إختر السلعة")
        # set icons
        self.set_icon("add_btn","add_item.svg")
        self.set_icon("cancel_btn","cancel.svg")
        
        


