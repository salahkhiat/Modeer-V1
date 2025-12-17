from .base_form import Form

class MobileForm(Form):
    def __init__(self,base_form):
        super().__init__(base_form)
        # set form title
        self.setWindowTitle("أدخل معلومات الهاتف المشترى")
        
        # Connect buttons
        self.save_cliced()

    def validate_form_fields(self)->bool:
        """
        If required fields are valid, return True and False otherwise.
        """
        if self.is_empty("mobile_name") is False or self.is_empty("seller_name") or self.is_amount("price") is False:
            print("this field is required")
            return False
        else:
            return True

        
        

    def save_mobile_form(self):
        if self.validate_form_fields() is False:
            return 
        else:
            self.close()

    def save_cliced(self):
        self.ui.save_btn.clicked.connect(self.save_mobile_form)


        




