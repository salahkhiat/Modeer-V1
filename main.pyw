# import sys
# from PyQt6.QtWidgets import QApplication 

# from uis.main_screen import Ui_main_window as MainUi 
# from ui_logic.main_screen import MainScreen
    
# def main():
#     # start the application
#     app = QApplication(sys.argv)

#     # Form or MainForm 
#     main_window = MainScreen(MainUi)
#     main_window.showMaximized()
#     sys.exit(app.exec())

# # 👇 Ensures the code only runs when the script is executed directly
# if __name__ == "__main__": main()

from PyQt6.QtCore import Qt, QTimer
import sys
from PyQt6.QtWidgets import QApplication

from uis.main_screen import Ui_main_window as MainUi
from ui_logic.main_screen import MainScreen

def main():
    app = QApplication(sys.argv)

    # Show splash(welcome screen) first; MainScreen will open after duration
    splash = MainScreen.show_welcome_screen(
        app,
        base_form_class=MainUi,
        image_path="splash_screen.png",
        duration=2500,
        width=900,
        height=500
    )

    sys.exit(app.exec())

if __name__ == "__main__":
    main()