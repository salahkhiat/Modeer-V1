from .base_form import Form
from PyQt6.QtCore import pyqtSignal 

class ChooseProductForm(Form):

    def __init__(self,base_form):
        super().__init__(base_form)
        # set icons
        self.set_icon("add_btn","add.svg")
        self.set_icon("cancel_btn","cancel.svg")
        
        