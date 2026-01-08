from .base_form import Form
from typing import List 
class EditableItemsForm(Form):

    def __init__(self,base_form):
        super().__init__(base_form)
        # set icons
        self.set_icon("edit_btn","edit.svg")
        self.set_icon("delete_btn","delete.svg")

        # table
  
        


    def set_window_title(self,title):
        self.setWindowTitle(title)

    def set_table_headers(self, headers:List[str]=["test1","test2"]):
        table = self.ui.table
        self.set_table(table,headers)


        