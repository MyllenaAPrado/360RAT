from Interfaces.input_window import Ui_Form
from PyQt5 import QtWidgets
from sys import platform
from PyQt5 import QtGui
import os

class GetInput():

    def __init__(self):
        self.input_text = ''
        #set window of save roi
        self.window_input = QtWidgets.QMainWindow()

        if platform == "linux" or platform == "linux2":
            # linux
            self.window_input.setWindowIcon(QtGui.QIcon(os.getcwd() + "/Images/icon.png"))

        elif platform == "win32":
            # Windows...
            self.window_input.setWindowIcon(QtGui.QIcon(os.getcwd() + "\Images\icon.png"))
        
        self.window_input.setWindowTitle("360Rat")
        self.ui_input = Ui_Form()
        self.ui_input.setupUi(self.window_input)
        
    
    def get_window(self):
        return self.window_input

    def get_ui(self):
        return self.ui_input

    def open_window(self):
        self.window_input.show()
    
    def close_window(self):
        self.window_input.close()

    def set_text_window(self, phrase):
        self.ui_input.text_output.setText(phrase)

    def clear_input_field(self):
        self.ui_input.input.clear()
        
    def get_input_text(self):
        return self.ui_input.input.text()