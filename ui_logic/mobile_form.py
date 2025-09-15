from .base_form import Form

class MobileForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("أدخل معلومات الهاتف المشترى")
        # set icons
        self.set_icon("add_document_type_btn","add.svg")

        




