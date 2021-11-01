from Interfaces.ROI_save__window import Ui_SaveROI
from Interfaces.compose_ROI_save_window import Ui_SaveComposeROI
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from sys import platform
import os

class SaveWindow():
    def __init__(self):
        #set window of save roi
        self.window_label_ROI = QtWidgets.QMainWindow()

        if platform == "linux" or platform == "linux2":
            # linux
            self.window_label_ROI.setWindowIcon(QtGui.QIcon(os.getcwd() + "/Images/icon.png"))

        elif platform == "win32":
            # Windows...
            self.window_label_ROI.setWindowIcon(QtGui.QIcon(os.getcwd() + "\Images\icon.png"))
        
        self.window_label_ROI.setWindowTitle("360Rat")
        self.ui_roi = Ui_SaveROI()
        self.ui_roi.setupUi(self.window_label_ROI)

        #set window of save roi
        self.window_save_compose_ROI = QtWidgets.QMainWindow()
        if platform == "linux" or platform == "linux2":
            # linux
            self.window_save_compose_ROI.setWindowIcon(QtGui.QIcon(os.getcwd() + "/Images/icon.png"))

        elif platform == "win32":
            # Windows...
            self.window_save_compose_ROI.setWindowIcon(QtGui.QIcon(os.getcwd() + "\Images\icon.png"))
        
        self.window_save_compose_ROI.setWindowTitle("360Rat")
        self.ui_compose_roi = Ui_SaveComposeROI()
        self.ui_compose_roi.setupUi(self.window_save_compose_ROI)

        self.set_colors_variables()
        self.set_label_dictionary()
        self.add_label_roi(self.ui_roi)
        self.add_label_roi(self.ui_compose_roi)

        self.ui_compose_roi.button_yes.clicked.connect(self.enable_save_roi_yes)
        self.ui_compose_roi.button_no.clicked.connect(self.enable_save_roi_no)
        self.ui_compose_roi.button_yes.setStyleSheet("background-color : rgb(0,0,100);")
        self.ui_compose_roi.button_no.setStyleSheet("background-color : rgb(0,0,100);")
        self.ui_compose_roi.button_save_compose_ROI.setEnabled(False) 

        self.movement_roi = False
    
    def get_ui(self):
        return self.ui_roi, self.ui_compose_roi
    
    def get_compose_roi_window(self):
        return self.window_save_compose_ROI

    def get_roi_window(self):
        return self.window_label_ROI

    def get_label_ROI(self):
        #get the label selected
        widget = self.ui_roi.scrollArea.widget()
        if widget :
            children = widget.children()
            children.pop(0)
            for aux in children:
                if(aux.isChecked()==True):
                    label = aux.text() 
        
        return label

    def get_label_compose_ROI(self):
        #get the label selected
        widget = self.ui_compose_roi.scrollArea.widget()
        if widget :
            children = widget.children()
            children.pop(0)
            for aux in children:
                if(aux.isChecked()==True):
                    label = aux.text() 

        return label

    def get_movement_flag(self):
        return self.movement_roi

    def  set_colors_variables(self):
        #https://www.webucator.com/article/python-color-constants-module/
        self.BLACK = (0, 0, 0)
        self.BLACK_RGB = (0, 0, 0)
        self.BLUE = (255, 0, 0)
        self.BLUE_RGB = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.GREEN_RGB = (0, 255, 0)
        self.RED = (0, 0, 255)
        self.RED_RGB = (255, 0, 0)
        self.YELLOW = (0, 215, 255)
        self.YELLOW_RGB = (255, 215, 0)
        self.MANGETA = (255, 0, 255)
        self.MANGETA_RGB = (255, 0, 255)
        self.PINK = (147, 20, 255)
        self.PINK_RGB = (255, 20, 147)
        self.WHITE = (255,255,255)
        self.WHITE_RGB = (255, 255, 255)
        self.ORANGE = (0, 128, 255)
        self.ORANGE_RGB = (255, 128, 0)
        self.PURPLE = (128, 0, 128)
        self.PURPLE_RGB = (128, 0, 128)
        self.BROWN = (15, 54, 138)
        self.BROWN_RGB = (138, 54, 15)
        self.CADETBLUE = (209, 206, 0)
        self.CADETBLUE_RGB = (0, 206, 209)
        self.GOLD = (0, 117, 139)
        self.GOLD_RGB = (139, 117, 0)
        self.LIGHTPINK = (185, 174, 255)
        self.LIGHTPINK_RGB = (255, 174, 185)
        self.SAPGREEN = (20, 128, 48)
        self.SAPGREEN_RGB = (48, 128, 20)
        self.LIGHTSTEELBLUE = (255,225,202)
        self.LIGHTSTEELBLUE_RGB = (202,225,255)
        self.PLUM = (221,160,221)
        self.PLUM_RGB = (221,160,221)
        self.SEAGREEN = (87,139,46)
        self.SEAGREEN_RGB = (46,139,87)

        


    def set_label_dictionary(self):
        #set parameters in scroll area of widnow of save roi
        
        self.dictionary_label_color = {'Accessory' : self.GREEN, 'Animal' : self.ORANGE,
                                       'Appliance' : self.PINK, 'Electronic' : self.PURPLE, 
                                       'Food' : self.SAPGREEN, 'Furniture' : self.BLUE,
                                       'Indoor' : self.YELLOW, 'Kitchen' : self.MANGETA, 
                                       'Outdoor' : self.BROWN, 'Person' : self.CADETBLUE, 
                                       'Sports' : self.GOLD, 'Vehicle' : self.LIGHTPINK,
                                       'Architecture/buildings' : self.LIGHTSTEELBLUE, 'Text' : self.PLUM,
                                       'Vegetation' : self.SEAGREEN}

        self.dictionary_label_color_RGB = {'Accessory' : self.GREEN_RGB, 'Animal' : self.ORANGE_RGB,
                                       'Appliance' : self.PINK_RGB, 'Electronic' : self.PURPLE_RGB, 
                                       'Food' : self.SAPGREEN_RGB, 'Furniture' : self.BLUE_RGB,
                                       'Indoor' : self.YELLOW_RGB, 'Kitchen' : self.MANGETA_RGB, 
                                       'Outdoor' : self.BROWN_RGB, 'Person' : self.CADETBLUE_RGB, 
                                       'Sports' : self.GOLD_RGB, 'Vehicle' : self.LIGHTPINK_RGB,
                                       'Architecture/buildings' : self.LIGHTSTEELBLUE_RGB, 'Text' : self.PLUM_RGB,
                                       'Vegetation': self.SEAGREEN_RGB} 
        '''
        self.dictionary_label_color = {'Primary' : self.GREEN, 'Secondary' : self.PURPLE, 
                                       'Tertiary' : self.BLUE, 'Quaternary' : self.YELLOW}

        self.dictionary_label_color_RGB = {'Primary' : self.GREEN_RGB, 'Secondary' : self.PURPLE_RGB, 
                                           'Tertiary' : self.BLUE_RGB, 'Quaternary' : self.YELLOW_RGB}
        '''

        return self.dictionary_label_color, self.dictionary_label_color_RGB

    def add_label_roi(self, widget):

         #add labels in scroll area
        layout = QtWidgets.QFormLayout()
        groupBox = QtWidgets.QGroupBox()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        groupBox.setFont(font)

        for label in self.dictionary_label_color:
            radio_button = QtWidgets.QRadioButton("{}".format(label))
            radio_button.setStyleSheet("font: bold; color : rgb{}; font-size: 24px;".format(self.dictionary_label_color_RGB[label]))
            layout.addRow(radio_button)
        
        groupBox.setLayout(layout)
        widget.scrollArea.setWidget(groupBox)
        #self.ui_compose_roi.scrollArea.setWidget(groupBox)

    def enable_save_roi_yes(self):
        self.ui_compose_roi.button_save_compose_ROI.setEnabled(True) 
        self.ui_compose_roi.button_yes.setStyleSheet("background-color : green;")
        self.ui_compose_roi.button_no.setStyleSheet("background-color : rgb(0,0,100);")
        self.movement_roi = True
    
    def enable_save_roi_no(self):
        self.ui_compose_roi.button_save_compose_ROI.setEnabled(True)
        self.ui_compose_roi.button_yes.setStyleSheet("background-color : rgb(0,0,100);")
        self.ui_compose_roi.button_no.setStyleSheet("background-color : green;")
        self.movement_roi = False

    def close_save_compose_roi_window(self, ui):
        self.window_save_compose_ROI.hide()
        self.ui_compose_roi.button_save_compose_ROI.setEnabled(False)
        self.ui_compose_roi.button_yes.setStyleSheet("background-color : rgb(0,0,100);")
        self.ui_compose_roi.button_no.setStyleSheet("background-color : rgb(0,0,100);")

        #enable save csv button
        ui.button_save.setEnabled(True)

    def close_save_roi_window(self, ui):
        #hide the window of label
        self.window_label_ROI.hide()

        #update fov sliders to default value
        ui.slider_fov_h.setValue(60)
        ui.slider_fov_w.setValue(30)

        #enable save csv button
        ui.button_save.setEnabled(True)

