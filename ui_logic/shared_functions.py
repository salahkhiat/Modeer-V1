from PyQt6 import QtGui
import json, os, sys
from typing import Dict, Any 

from PyQt6.QtWidgets import QComboBox

from hijri_converter import Gregorian
from datetime import datetime

class SharedFunctions:
    def set_icon(self, btn_name, icon_name):
        icon_path = self.resource_path(f"./icons/{icon_name}")
        icon = QtGui.QIcon(icon_path)

        btn = getattr(self.ui, btn_name)
        btn.setIcon(icon)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    # get settings as dict 
    def get_settings(self) -> dict:
        return self.get_settings_info(self.get_settings_json_path())
    
    # Returns the Index of the current selected combobox item
    def get_current_combo_index(self,combo_name:str) -> int:
        return getattr(self.ui,combo_name).currentIndex()

    # get current date in Hijri or Gregorian. Hijri is the default.
    def current_date(self) -> str:
        hijri_date =self.get_settings()["hijri_date"]
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        if hijri_date == True:
            return  str(Gregorian(year, month, day).to_hijri())
        else:
            return  str(Gregorian(year, month, day))
    
    # check if settings.json file is exsits returns True, otherwise return False
    def is_settings_file_exists(self) -> bool:
        exists = False 
        for entry in os.scandir("."):
            if entry.is_file() and entry.name == "settings.json":
                exists =  True
                break 

        return exists
    # settings.json file path 
    def get_settings_json_path(self):
        return os.path.join(os.getcwd(), "settings.json")

    # Create setting.json file 
    def create_settings_file(self,settings_path):
        full_path = settings_path
        default_settings = {
            "hijri_date": True,
            "database_path": None,
            "database_name": "shop_data.db"
        }
        with open(full_path,"w") as file:
            json.dump(default_settings, file, indent=4)

    # get settings.json content
    def get_settings_info(self,settings_path): 
            settings = settings_path
            with open(settings,'r') as file:
                settings = json.load(file)
            return settings
    


    def fetch_then_put(self, table:str, column:str, combo:QComboBox) -> None:
        """
        Fetch table rows from the database as a List then, Then put them in combo.
        
        Args:
            table (str):  The table name.
            column (str): The table column.
            combo (QComboBox): The QComboBox.
        
        Example:
            >>> table = "Students"
            >>> column = "name"
            >>> combo = obj.ui.ComboBox
            >>> obj.fetch_then_put(table,column,combo)
            None
        """
        items = self.get_table_as_list(table,[column])
        
        # remove "-" from the list to make it appears first in combo
        items = list(items)
        if "-" in items:
            items.remove("-")
            combo.addItem("-")
            
        combo.addItems(items)
    def reverse_dict(self, dictionary:Dict[Any,Any]) -> Dict[Any,Any]:
     """
     Converting {Key:Value} to {Value:Key}

    Args:
        dictionary (Dict[Any,Any]): The original dictionary.
    Returns:
        Dict[Any,Any]: The reversed dictionary.
    Examples:
        >>> myDict = {1:"one", 2:"two"}
        >>> print(obj.reverse_dict(myDict))
        {"one":1, "two":2}
     """
     return {value:key for key, value in dictionary.items()}