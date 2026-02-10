from .base_form import Form

class ConfirmationMsgForm(Form):
    def __init__(self,base_form,msg=""):
        super().__init__(base_form)
        self.setWindowTitle(msg)
        self.ui.msg.setText(msg)
        # set icons
        self.set_icon("apply_btn","apply.svg")
        self.set_icon("cancel_btn","cancel.svg")