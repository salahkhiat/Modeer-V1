from PyQt6.QtGui import  QRegularExpressionValidator 
from PyQt6.QtCore import QRegularExpression 
from PyQt6.QtWidgets import QLineEdit
from typing import List


from .database_manager import DatabaseManager

class SharedValidators(DatabaseManager):
    # Set only numbers are accepted  
    def accept_numbers_only(self,field:QLineEdit ) -> None:
        """
        Accept only numbers.
        """
        regex = QRegularExpression("^\d*$") # Accepts only digits 0-9
        validator = QRegularExpressionValidator(regex)
        field.setValidator(validator)
    
    def enable_field(self, field:QLineEdit, state=True):
        """
        Enable/Disable QLineEdit field, Enabled by default.

        Args:
            field (QLineEdit): the field as QLineEdit.
            state (bool): True is Enabled, and False is Disabled.
        """
        if state is True:
            field.setStyleSheet("background-color:white;")
        else:
            self.clear_fields([field])
            field.setStyleSheet("background-color:gray;")
        field.setEnabled(state)


    # Check the minimum and the maximum of an amount. min = 1 DZD , max = 100000 DZD.
    def is_price(self, field_name:str):
        field = getattr(self.ui,field_name).text()
        if len(field) > 0:
            amount = int(field)
            if amount == 0 :
                self.set_err_msg(field_name,"الصفر قيمة مرفوضة")
                return False 
            elif amount > 100000:
                self.set_err_msg(field_name,"أقصى مبلغ هو : 100000 دج")
                return False
            elif amount > 0 and amount < 100001:
                self.set_err_msg(field_name, "الحقل جاهز")
                return True 
            
    # Set a error message
    def set_err_msg(self, field_name:str ,msg:str=""):
        field_err = getattr(self.ui,field_name + "_err")
        field_err.setText(msg)

    # Check if the field is empty
    def is_empty(self, field_name:str, err_msg:bool=True )-> bool:
        """
        If the field is empty return False, and True otherwise.

        Args:
            field_name (str): the QLineEdit name.
            err_msg (bool): True by default to return error messages, and False without messages.
        """
        field = getattr(self.ui,field_name).text()
        if len(field) == 0:
            if err_msg:
                self.set_err_msg(field_name,"هذا الحقل مطلوب")
            return False
        else:
            if err_msg:
                self.set_err_msg(field_name,"الحقل جاهز")
            return True 
         
    # Check if the field is a telephone
    def is_tel(self, field_name:str) -> bool:
        field = getattr(self.ui,field_name).text()
        
        if len(field) < 10 and len(field) > 0:
            self.set_err_msg(field_name,"الهاتف أقصر من 10 أرقام")
            return False
        
        elif len(field) == 0:
            self.set_err_msg(field_name,"رقم الهاتف إختياري")
            return True 
        
        else:
            if field.startswith(("05","06","07")) :
                self.set_err_msg(field_name,"رقم الهاتف جاهز")
                return True
            
            else:
                self.set_err_msg(field_name," الهاتف يجب أن يبدأ بـ 05, 06, 07")
                return False
            
    def is_tel_ready(self, tel_field:str) -> bool :
        """
        is a telephone number ready to save?

        :param tel_field: a QLineEdit field name as a string.
        :type tel_field: str
        :return: True if a number is ready to save, and False otherwise.
        :rtype: bool

        :example:
            >>> obj.is_tel_ready("QLineEdit_name")
            True
        """
        combo_index = self.get_current_combo_index('account_type')
        account_types = ["customers", "suppliers", "employees"]
        table = account_types[combo_index]
        
        tel= getattr(self.ui,tel_field).text()
        if  self.is_tel(tel_field) == True and len(tel) == 0:
            return True
        elif self.is_tel(tel_field) == True and len(tel) == 10:
            if self.tel_exists(table,tel):
                self.set_err_msg(tel_field,"هذا الرقم موجود مسبقا")
                return False
            else:
                return True
    
    def is_amount(self, field_name:str) -> bool:
        """
        Check if the given field name is a valid amount

        Args: 
            field_name (str): The amount field name.
        Returns:
            bool: True if the field is non-empty and a valid price, False otherwise.
        """
        return self.is_empty(field_name) and self.is_price(field_name)
    
    
    def is_deposit(self, field_name:str) -> bool:
        """
        Check if the given field name is a valid deposit.

        Args: 
            field_name (str): The amount field name.
        Returns:
            bool: True if the field is empty(optional) or a valid price, False otherwise.
        """
        if self.is_empty(field_name) == False:
            self.set_err_msg(field_name, "هذا الحقل إختياري")
            return True 
        else:
            return self.is_price(field_name)
    
    def is_max(self, table:str, column:str, max_len:int=10) -> bool:
        """
        Check if the table has the numbers of rows equivalent/greater than max_len.

        Args:
            table (str): the table name.
            column (str): the column name.4
            max_length (int): the maximum number of rows.
        Returns:
            bool : True if the numbers of rows is equivalent to max_len or greater 10 by default, and False otherwise.
        Examples:
            >>> table = "customers"
            >>> column = "name"
            >>> obj.is_max(table, column,5)
            False
        """
        rows = self.get_table_as_list(table,[column])
        
        if len(rows)  >= max_len:
            return True 
        else:
            return False 
        
    def is_cur_item_empty(self, combo_name:str) -> bool:
        """
        Check if the current (selected combo item) is empty ("") or equivalent to "-".

        Args:
            combo (str): the combo box name.
        Returns:
            bool: True if it is empty or equivalent to '-', and False otherwise.
        Examples:
            >>> combo = "QComboBox_name"
            >>> combo.addItem("first item")
            >>> obj.is_cur_item_empty(combo)
            False
        """
        combo_value = getattr(self.ui,combo_name).currentText()
        if combo_value == "" or combo_value == "-":
            return False 
        else:
            return True 

    def clear_fields(self, fields: List[QLineEdit] ) -> None:
        """
        Clears the text in multiple QLineEdit fields.

        :param fields: a list of QLineEdit .
        :type fields: list[QLineEdit]

        example:
        >>> name = obj.ui.name
        >>> address = obj.ui.address
        >>> fields = [name,address]
        >>> obj.clear_fields(fields)
        """
        for field in fields:
            field.clear()
    

            
    def update_validation_response(self,field_name :str ,validating_fun:str) -> None:
        """
        store a validation function response (True or False) in the is_valid_xxx indicator like is_valid_name etc.

        :param field_name: a validation field name.
        :type field_name: str
        :param validating_fun: a validation function.
        :type validating_fun: str

        :example:
            >>> obj.update_validation_response("is_valid_name","is_empty")
        """
        
        validating = getattr(self,validating_fun)
        response = validating(field_name)
        setattr(self,"is_valid_"+field_name,response)

        """
            item_form : purchase price validation.
        """

    def is_purchase_price(self, field_name:str) -> bool:
        """
        Validaing Purchase_price field.

        Args:
            field_name (str): A QLineEdit field name. 
        
        Returns:
            bool: True if it is valid, and False otherwise.
        """
        
        # if purchase price is not empty.
        if self.is_empty(field_name,err_msg=False):
            field = int(getattr(self.ui,field_name).text())
            # if purchase price is equivalent to 0.
            if field == '0':
                msg = "إنتبه! سعر الشراء الآن '0دج'"
                self.set_err_msg(field_name,msg)
                return True 
            # if purchase price is greater than 100.000 DZD.
            elif field > 100000:
                msg = "أقصى سعر مسموح به هو 100.000 دج"
                self.set_err_msg(field_name,msg)
                return False
            # if purchase price is greater than 0 and less than 100.001 DZD.
            elif field > 0 and field < 100001:
                msg = "السعر جاهز"
                self.set_err_msg(field_name,msg)
                return True
            # if there is an expected error.
            else:
                msg = "تأكد من سلامة الحقل"
                self.set_err_msg(field_name,msg)
                return False
            
        # if a purchase price is empty.
        else:
            # item_details["purchase_price"] = '0'
            msg = "إنتبه! سعر الشراء الآن '0دج'"
            self.set_err_msg(field_name,msg)
            return True 


    


    
        
    


        