from Interfaces.Anottation_window import Ui_Anottation
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class ScrollArea():

    def __init__(self, ui):
        #set parameters to scroll area in list of roi 
        self.form_layout = QtWidgets.QFormLayout()
        self.group_box = QtWidgets.QGroupBox("List of ROI")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.group_box.setFont(font)
        ui.scroll_area_ROI.setWidget(self.group_box)

        #set parameters to scroll area in list of compose roi 
        self.form_layout_compose = QtWidgets.QFormLayout()
        self.group_box_compose = QtWidgets.QGroupBox("List of compose ROI")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.group_box_compose.setFont(font)
        ui.scroll_area_compose_ROI.setWidget(self.group_box_compose)

    def add_single_ROI(self, ui, button):
        self.form_layout.addRow(button)
        self.group_box.setLayout(self.form_layout)
        ui.scroll_area_ROI.setWidget(self.group_box)
    
    def add_compose_ROI(self, ui, button):
        self.form_layout_compose.addRow(button)
        self.group_box_compose.setLayout(self.form_layout_compose)
        ui.scroll_area_compose_ROI.setWidget(self.group_box_compose)

    def clear_scroll_area_single_ROI(self):
        #clear scroll area of roi
        for i in range ((self.form_layout.count()-1), -1, -1):
            self.form_layout.removeRow(i)
    
    def clear_scroll_area_compose_ROI(self):
        #clear scroll area of roi
        for i in range ((self.form_layout_compose.count()-1), -1, -1):
            self.form_layout_compose.removeRow(i)






