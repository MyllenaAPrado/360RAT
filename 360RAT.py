#!/bin/python3
from Interfaces.Anottation_window import Ui_Anottation
from Interfaces.ROI_save__window import Ui_SaveROI
from Interfaces.compose_ROI_save_window import Ui_SaveComposeROI
from Interfaces.save_ok__window import Ui_save
from Interfaces.add_label_window import Ui_AddLabel
from Interfaces.input_window import Ui_Form
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5 import QtGui
import numpy as np
from Entities.ImageAnotation import Image_Anotation
from Entities.ROI import ROI
from Entities.ComposeROI import Compose_ROI
from Entities.SimplifiedComposeROI import Simple_compose_ROI
from Service.SphereFov import NFOV
from Service.Rendering import Rendering
from Service.Rendering_video import Rendering_Video
from Service.SaveCSV import CSV
from Service.Upload_Annotations import Upload_CSV
from Service.Compose_ROI_controller import ComposeROIController
from Service.Single_ROI_controller import SingleROI
from Service.Scroll_areas import ScrollArea
from Service.Save_windows import SaveWindow
from Service.GetInputUser import GetInput as GetInputFPS
from functools import partial
from sys import platform
import os
import csv
import sys
import cv2
import os.path as osp

class AnottationWindow(QtWidgets.QMainWindow):

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Anottation()
        self.ui.setupUi(self)
        if platform == "linux" or platform == "linux2":
            # linux
            self.setWindowIcon(QtGui.QIcon(os.getcwd() + "/Images/icon.png"))
            self.path_button_prev = os.getcwd() + "/Images/icon_prev.png"
            self.path_button_next = os.getcwd() + "/Images/icon_next.png"

        elif platform == "win32":
            # Windows...
            self.setWindowIcon(QtGui.QIcon(os.getcwd() + "\Images\icon.png"))
            self.path_button_prev = os.getcwd() + "\Images\icon_prev.png"
            self.path_button_next = os.getcwd() + "\Images\icon_next.png"

        self.setWindowTitle("360Rat")
        #self.showMaximized()

        self.set_intial_param()
        self.upload_result_window()
        self.config_buttons_and_sliders()

        
        #self.open_input_window_name("Name")

    def set_intial_param(self):

        self.list_frame = []
        self.flag_pause=True
        self.flag_Upload_video_init = False
        self.fps = 60

        self.nfov = NFOV(400,400)
        self.controllerComposeROI = ComposeROIController(self.ui)
        self.controllerSingleROI = SingleROI(self.ui)
        self.Scroll_area = ScrollArea(self.ui)
        self.Save_proprieties = SaveWindow()
        self.csv = CSV("User")
        self.window_input_FPS = GetInputFPS()
        self.dictionary_label_color, self.dictionary_label_color_RGB = self.Save_proprieties.set_label_dictionary()
        self.ui_roi, self.ui_compose_roi = self.Save_proprieties.get_ui()
        self.ui_roi.button_save_one_ROI.clicked.connect(self.save_ROI)
        self.ui_compose_roi.button_save_compose_ROI.clicked.connect(self.set_first_ROI)

    def config_buttons_and_sliders(self):
        #self.ui.button_upload_labels.clicked.connect(self.open_label_csv)

        #change the maxinum of fov oppening
        self.ui.slider_fov_h.setMaximum(22)
        self.ui.slider_fov_w.setMaximum(11)

        #push bottun conect
        self.ui.button_upload_image.triggered.connect(self.upload_image)
        self.ui.button_upload_folder.triggered.connect(self.upload_folder)
        self.ui.button_upload_video.triggered.connect(self.upload_video)        
        self.ui.button_save.triggered.connect(self.save_csv)
        
        self.ui.button_play_video.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_pause_video.clicked.connect(self.pause)
        self.ui.button_pause_video.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_upload_Annotations.triggered.connect(self.upload_csv)

    
        #buttons single roi
        self.ui.button_save_ROI.clicked.connect(self.open_save_roi_window)
        self.ui.button_save_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_delete_ROI.clicked.connect(self.delete_ROI)
        self.ui.button_delete_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_save_edit.clicked.connect(self.open_save_roi_window)
        self.ui.button_save_edit.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_cancel_edit.clicked.connect(partial(self.controllerSingleROI.finish_edit_ROI, self.ui))
        self.ui.button_cancel_edit.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")


        #buttons compose roi
        self.ui.button_go_to_first.clicked.connect(self.go_to_init_frame)
        self.ui.button_go_to_first.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_go_to_last.clicked.connect(self.go_to_end_frame)
        self.ui.button_go_to_last.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_edit_one_compose_ROI.clicked.connect(self.edit_one_compose_ROI)
        self.ui.button_edit_one_compose_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_save_edit_compose_ROI.clicked.connect(self.save_edit_one_compose_ROI)
        self.ui.button_save_edit_compose_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_cancel_edit_compose_ROI.clicked.connect(self.cancel_edit_one_compose_ROI)
        self.ui.button_cancel_edit_compose_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_delete_compose_ROI.clicked.connect(self.delete_compose_ROI)
        self.ui.button_delete_compose_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_add_new_CROI.clicked.connect(self.add_new_compose_ROI)
        self.ui.button_add_new_CROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_set_new_CROI.clicked.connect(self.set_new_add_compose_ROI)
        self.ui.button_set_new_CROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")

        self.ui.button_add_compose_roi.clicked.connect(self.add_compose_ROI)
        self.ui.button_add_compose_roi.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_save_add_ROI.clicked.connect(self.save_add_compose_ROI)
        self.ui.button_save_add_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_edit_long_CROI.clicked.connect(self.edit_long_compose_ROI)
        self.ui.button_edit_long_CROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")                     
        self.ui.button_set_init_CROI.clicked.connect(self.set_init_edit_group)
        self.ui.button_set_init_CROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_save_CROI.clicked.connect(self.save_edit_group)
        self.ui.button_save_CROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        
        self.ui.button_init_ROI.clicked.connect(self.open_save_compose_roi_window)
        self.ui.button_init_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_end_ROI.clicked.connect(self.save_finish_compose_ROI)
        self.ui.button_end_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")

        self.ui.button_previous.setStyleSheet(":enabled { background-color: rgb(255, 255, 255);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_previous.setIcon(QtGui.QIcon(self.path_button_prev))
            
        self.ui.button_next.setStyleSheet(":enabled { background-color: rgb(255, 255, 255);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")
        self.ui.button_next.setIcon(QtGui.QIcon(self.path_button_next))

        self.ui.button_edit_ROI.setStyleSheet(":enabled { background-color: rgb(0, 0, 100);"
                             + " } :disabled { background-color: rgb(143, 143, 143);}")


        self.ui.button_save.setEnabled(False)
        self.ui.button_previous.setEnabled(False)
        self.ui.button_next.setEnabled(False)
        self.ui.button_play_video.setEnabled(False)
        self.ui.button_pause_video.setEnabled(False)
        self.ui.button_init_ROI.setEnabled(False)
        self.ui.button_end_ROI.setEnabled(False)

        ##sliders
        self.ui.slider_fov_h.valueChanged.connect(self.update_fov)
        self.ui.slider_fov_w.valueChanged.connect(self.update_fov)
        self.ui.slider_pos_x.valueChanged.connect(self.update_pos_xy)
        self.ui.slider_pos_y.valueChanged.connect(self.update_pos_xy)
        self.ui.slider_fov_h.setEnabled(False)
        self.ui.slider_fov_w.setEnabled(False)
        self.ui.slider_pos_x.setEnabled(False)
        self.ui.slider_pos_y.setEnabled(False)

        

        self.ui.input_ROI_W.editingFinished.connect(self.update_fov_W_input)
        self.ui.input_ROI_H.editingFinished.connect(self.update_fov_H_input)
        self.ui.input_ROI_W.setEnabled(False)
        self.ui.input_ROI_H.setEnabled(False)

        

    #Upload Image
    def close_upload_window(self):
        self.window_upload_result.hide()

    def upload_result_window(self):
        self.window_upload_result = QtWidgets.QDialog()
        if platform == "linux" or platform == "linux2":
            # linux
            self.window_upload_result.setWindowIcon(QtGui.QIcon(os.getcwd() + "/Images/icon.png"))

        elif platform == "win32":
            # Windows...
            self.window_upload_result.setWindowIcon(QtGui.QIcon(os.getcwd() + "\Images\icon.png"))
        
        self.window_upload_result.setWindowTitle("360Rat")
        self.ui_upload = Ui_AddLabel()
        self.ui_upload.setupUi(self.window_upload_result)
        self.ui_upload.pushButton_OK.clicked.connect(self.close_upload_window)

    #Image
    def upload_image(self):
        self.list_frame.clear()

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files ( *.jpg *.png)')
        image_path = fname[0]
        self.id_image = 0

        if image_path != '':           
            render_img = Rendering(image_path)
            window_size_equi = (self.ui.equi_image.width(),self.ui.equi_image.height())
            self.list_frame.append(Image_Anotation(0,render_img.image_rendering(window_size_equi), image_path))

            self.set_image_equirectangular_view(self.id_image)
            
            self.ui.button_previous.clicked.connect(self.previous_image)
            self.ui.button_next.clicked.connect(self.next_image)
            self.ui.button_next.setEnabled(False)
            self.ui.button_previous.setEnabled(False)
            
        else:
            self.ui_upload.text_result.setText("Upload Canceled!")
            self.window_upload_result.show()

    def upload_folder(self):
        folder_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))

        if folder_name !='': 
            self.list_frame.clear()
            list_file_image = [(folder_name + "/" + fn) for fn in os.listdir(folder_name)
                                    if any(fn.endswith(ext) for ext in ['jpg', 'jpeg', 'png'])]
            index = 0
            for image_path in list_file_image:
                render_img = Rendering(image_path)
                window_size_equi = (self.ui.equi_image.width(),self.ui.equi_image.height())
                self.list_frame.append(Image_Anotation(index, render_img.image_rendering(window_size_equi), image_path))
                index+=1

            self.id_image = 0 
            if self.list_frame:
                self.set_image_equirectangular_view(self.id_image)

            self.ui.button_previous.clicked.connect(self.previous_image)
            self.ui.button_next.clicked.connect(self.next_image)
            self.ui.button_next.setEnabled(False)
            self.ui.button_previous.setEnabled(False)

            if len(self.list_frame) > 1:
                self.ui.button_next.setEnabled(True)
            
            
        else:
            self.ui_upload.text_result.setText("Upload Canceled!")
            self.window_upload_result.show()

    def previous_image(self):
        self.id_image -= 1
        self.ui.button_next.setEnabled(True)

        if self.id_image == 0:
            self.ui.button_previous.setEnabled(False)
        self.ui.slider_video_duration.blockSignals(True)
        self.ui.slider_video_duration.setValue(self.id_image)
        self.ui.slider_video_duration.blockSignals(False)
        self.set_image_equirectangular_view(self.id_image)

    def next_image(self):
        self.id_image += 1
        self.ui.button_previous.setEnabled(True)

        if (len(self.list_frame) - self.id_image) == 1:
            self.ui.button_next.setEnabled(False)
            self.finish_video = True
            self.pause()
        self.ui.slider_video_duration.blockSignals(True)
        self.ui.slider_video_duration.setValue(self.id_image)
        self.ui.slider_video_duration.blockSignals(False)
        self.set_image_equirectangular_view(self.id_image)

    def set_image_equirectangular_view(self, id):

        self.ui.equi_image.setScaledContents(True)
        img_equi_qt = QtGui.QImage(self.list_frame[id].get_image().data, self.list_frame[id].get_image().shape[1], self.list_frame[id].get_image().shape[0], self.list_frame[id].get_image().shape[1]*3,QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(img_equi_qt)
        self.ui.equi_image.setPixmap(pixmap)
        self.ui.equi_image.repaint()
        QtWidgets.QApplication.processEvents()
        self.ui.equi_image.mousePressEvent = self.get_pos_ROI
        self.ui.text_frame_number.setText(f'Frame: {self.id_image}')
        self.ui.text_time.setText(f'{self.id_image/self.fps :}')

        #set image in nfov
        self.img_copy = self.list_frame[id].get_image().copy()
        self.nfov(self.img_copy)
        self.ui.perspective_image.clear()
        self.ui.slider_fov_h.setEnabled(False)
        self.ui.slider_fov_w.setEnabled(False)
        self.ui.slider_pos_x.setEnabled(False)
        self.ui.slider_pos_y.setEnabled(False)
        self.ui.input_ROI_W.setEnabled(False)
        self.ui.input_ROI_H.setEnabled(False)

        self.Scroll_area.clear_scroll_area_single_ROI()
        self.nfov.nfov_id = 1
        
        #add in scroll area roi saved previous
        for roi in self.list_frame[id].get_list_roi():
            self.add_ROI_in_scroll_area(roi)
            self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
            self.nfov.updateNFOV(roi.get_center_point())
            self.nfov.draw_NFOV_edges(self.img_copy, label_color= self.dictionary_label_color[roi.get_label()])
        
        #print image with roi already marked
        if self.list_frame[id].get_list_roi():
            image = self.img_copy
            image_with_roi = QtGui.QImage(image.data, image.shape[1] , image.shape[0], image.shape[1]*3, QtGui.QImage.Format_BGR888)
            pixmap_roi = QtGui.QPixmap(image_with_roi)
            self.ui.equi_image.setPixmap(pixmap_roi)
            self.ui.equi_image.repaint()

            self.nfov.nfov_id = self.list_frame[id].get_list_roi()[-1].get_id() + 1
        
        #Change the display information about roi
        self.ui.text_nfov_information.setText(" Actual ROI: ")

    #Video
    def upload_video(self):

        video_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files ( *.mp4)')

        if video_path[0] !='':
            self.window_input_FPS.set_text_window("FPS")
            window = self.window_input_FPS.get_window()
            ui_input = self.window_input_FPS.get_ui()
            ui_input.button_OK.clicked.connect(partial(self.rendering_video, video_path))
            window.show()
            window.closeEvent = self.CloseEvent
            self.setEnabled(False)   

        else:
            self.ui_upload.text_result.setText("Upload Canceled!")
            self.window_upload_result.show()

    def rendering_video(self, video_path):

        self.window_input_FPS.close_window()
 
        self.list_frame.clear()
        self.Scroll_area.clear_scroll_area_compose_ROI()
        self.id_image = 0
        self.ui.button_play_video.setEnabled(True)  
        self.finish_video = False
        self.ui.button_previous.clicked.connect(self.previous_image)
        self.ui.button_next.clicked.connect(self.next_image)
        self.ui.button_next.setEnabled(True)
        self.ui.button_previous.setEnabled(False)
        self.flag_Upload_video_init = True
            
        redenring_video = Rendering_Video(video_path)
        self.list_frame, self.path_frames_original = redenring_video.get_list_video()
        self.ui.button_play_video.clicked.connect(self.start)
            
        self.set_image_equirectangular_view(self.id_image)  
        self.ui.slider_video_duration.setMaximum((len(self.list_frame)-1))    
        self.ui.slider_video_duration.valueChanged.connect(self.change_frame_video)

    def timerEvent(self):        
        self.time = self.time.addMSecs(self.Msec)
        self.ui.text_time.setText(self.time.toString("mm:ss"))

    def start(self):
        self.update_fps()
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)
        self.timer.timeout.connect(self.next_image)
        self.timer.setInterval(int(1000 / self.fps))
        self.timer.start()     
        self.ui.button_play_video.setEnabled(False)
        self.ui.button_pause_video.setEnabled(True)
        self.flag_pause=False
        self.Msec = int((1/self.fps) *1000)
    
    def update_fps(self):
        try:
            self.fps = int(self.window_input_FPS.get_input_text())
            
        except ValueError as ex:
            self.fps = 60
            self.ui_upload.text_result.setText("Fps not valid!")
            self.window_upload_result.show()

    def pause(self):
        self.timer.stop()
        if self.finish_video == False :
            self.ui.button_play_video.setEnabled(True)
        self.ui.button_pause_video.setEnabled(False)
        self.flag_pause=True

    def change_frame_video(self):
        self.id_image = self.ui.slider_video_duration.value()
        self.ui.button_next.setEnabled(True)
        self.ui.button_play_video.setEnabled(True)
        if (len(self.list_frame) - self.id_image) == 1:
            self.ui.button_next.setEnabled(False)
            self.ui.button_play_video.setEnabled(False)
        if self.id_image == 0:
            self.ui.button_previous.setEnabled(False)
       
        #self.set_frame_equirectangular_view(self.id_image)
        self.set_image_equirectangular_view(self.id_image)

    #ROI propreties
    def get_pos_ROI(self, event):
        x = event.pos().x()
        y = event.pos().y()

        self.ui.slider_pos_x.blockSignals(True)
        self.ui.slider_pos_y.blockSignals(True)
        self.ui.slider_pos_x.setValue(x)
        self.ui.slider_pos_y.setValue(y)
        self.ui.slider_pos_x.blockSignals(False)
        self.ui.slider_pos_y.blockSignals(False)
        self.ui.button_go_to_first.setEnabled(False)
        self.ui.button_go_to_last.setEnabled(False)

        self.center_point = np.array([x/self.ui.equi_image.width(), y/self.ui.equi_image.height()])
        self.update_view()
        
        #enable button associated with ROI
        if self.controllerSingleROI.get_flag_edit_roi() == False :
            self.ui.button_save_ROI.setEnabled(True)

        if self.flag_Upload_video_init == True :
            self.flag_Upload_video_init = False
            self.ui.button_init_ROI.setEnabled(True)

        if (self.ui.button_add_new_CROI.isEnabled() and self.ui.button_add_compose_roi.isEnabled() 
            and  self.ui.button_edit_one_compose_ROI.isEnabled() and self.ui.button_edit_long_CROI.isEnabled()):
            self.controllerComposeROI.disable_button(self.ui)

        self.ui.slider_pos_x.setEnabled(True)
        self.ui.slider_pos_y.setEnabled(True)
        self.ui.slider_fov_h.setEnabled(True)
        self.ui.slider_fov_w.setEnabled(True)
        self.ui.button_edit_ROI.setEnabled(False)
        self.ui.button_delete_ROI.setEnabled(False)
        self.ui.input_ROI_W.setEnabled(True)
        self.ui.input_ROI_H.setEnabled(True)
        
        if self.flag_pause == False:
            self.pause()

    def update_view(self, label_color = [0, 0, 255]):
        
        #update NFOV
        perspective_img, equi_img = self.nfov.updateNFOV(self.center_point, label_color)

        #update equi image on interface
        img_equi_qt = QtGui.QImage(equi_img.data, equi_img.shape[1], equi_img.shape[0], equi_img.shape[1]*3,QtGui.QImage.Format_BGR888)
        pixmap_equi = QtGui.QPixmap(img_equi_qt)
        self.ui.equi_image.setPixmap(pixmap_equi)
        self.ui.equi_image.repaint()

        #update perspective image on interface
        perspective_img_qt = QtGui.QImage(perspective_img.data, perspective_img.shape[1], 
                                        perspective_img.shape[0], perspective_img.shape[1]*3,QtGui.QImage.Format_BGR888)
        pixmap_perspective = QtGui.QPixmap(perspective_img_qt)
        self.ui.perspective_image.setPixmap(pixmap_perspective)
        self.ui.perspective_image.repaint()

        self.display_roi_information()

    def display_roi_information(self):
        #write nfov information in interface
        ang_H = 2 * np.arctan((self.nfov.FOV[1]*self.nfov.PI_2)/2) * 100
        ang_W = 2 * np.arctan((self.nfov.FOV[0]*self.nfov.PI)/2) * 100
        
        
        nfov_information = (" Actual ROI: "+
                            f'\n          Field of View ~= width:{ang_W :.2f} | height{ang_H :.2f}' +
                            f'\n          ROI ~= W:{self.nfov.FOV[0] :.2f} | H{self.nfov.FOV[1] :.2f}' +
                            "\n          Position: X:{:.3f}, Y: {:.3f}".format(self.center_point[0], self.center_point[1]))

        self.ui.text_nfov_information.setText(nfov_information)

    def update_fov_W_input(self):
        
        if self.ui.input_ROI_W.text() == '':
            return

        fov_w = 2 * np.tan(float(self.ui.input_ROI_W.text())/200)

        if fov_w > (self.ui.slider_fov_w.maximum()/100) or fov_w < 0:
            self.ui_upload.text_result.setText("Value not accept!")
            self.window_upload_result.show()            

        else :
            self.ui.slider_fov_w.setValue(int(fov_w * 100))
            fov_h = self.ui.slider_fov_h.value()/100
            self.nfov.set_fov(fov_h, fov_w)

            self.update_view()

    def update_fov_H_input(self):

        if self.ui.input_ROI_H.text() == '':
            return
        
        fov_h = 2 * np.tan(float(self.ui.input_ROI_H.text())/200) 

        if fov_h > (self.ui.slider_fov_h.maximum()/100) or fov_h < 0:
            self.ui_upload.text_result.setText("Value not accept!")
            self.window_upload_result.show()

        else :
            self.ui.slider_fov_h.setValue(int(fov_h * 100))
            fov_w = self.ui.slider_fov_w.value()/100
            self.nfov.set_fov(fov_h, fov_w)

            self.update_view()

    def update_fov(self):
        fov_h = self.ui.slider_fov_h.value()/100
        fov_w = self.ui.slider_fov_w.value()/100
        self.nfov.set_fov(fov_h, fov_w)

        self.update_view()

    def update_pos_xy(self):
        x = self.ui.slider_pos_x.value()/self.ui.equi_image.width()
        y = self.ui.slider_pos_y.value()/self.ui.equi_image.height()
        self.center_point = np.array([x, y])
        
        self.update_view()

    #save windows
    def close_save_roi_window(self):
        #hide the window of label
        self.Save_proprieties.close_save_roi_window(self.ui)
        self.setEnabled(True)

    def close_save_compose_roi_window(self):
        self.Save_proprieties.close_save_compose_roi_window(self.ui)
        self.setEnabled(True)

    def open_save_roi_window(self):
        window_label_ROI = self.Save_proprieties.get_roi_window()
        window_label_ROI.show()
        window_label_ROI.closeEvent = self.CloseEvent
        self.setEnabled(False)

    def open_save_compose_roi_window(self):
        window_save_compose_ROI = self.Save_proprieties.get_compose_roi_window()
        window_save_compose_ROI.show()
        window_save_compose_ROI.closeEvent = self.CloseEvent
        self.setEnabled(False)
    
    def CloseEvent(self, event):
        self.setEnabled(True)
    
    #Single ROI
    def save_ROI(self):
        
        label = self.Save_proprieties.get_label_ROI()
        roi = ROI(self.center_point, self.nfov.FOV, label)

        if self.controllerSingleROI.get_flag_edit_roi() == False:
            #save roi in a list
            roi = self.list_frame[self.id_image].add_ROI(roi)
            self.nfov.nfov_id = roi.get_id() + 1

            #add and display roi in the list of interface
            self.add_ROI_in_scroll_area(roi)

            #draw the roi permanently
            self.nfov.draw_NFOV_edges(self.img_copy, label_color= self.dictionary_label_color[label])

        if self.controllerSingleROI.get_flag_edit_roi() == True:
            roi.set_id(self.id_edit)
            self.list_frame[self.id_image].edit_roi(roi)
            self.set_image_equirectangular_view(self.id_image)
            
            self.controllerSingleROI.finish_edit_ROI(self.ui)

        self.close_save_roi_window()

    def add_ROI_in_scroll_area(self, roi):
        button = QtWidgets.QPushButton("Id= {}, X= {:.2f}, Y= {:.2f}, Label= {}".format(roi.get_id(), roi.get_center_point()[0],
                                                                                        roi.get_center_point()[1], roi.get_label()))

        button.setStyleSheet("font: bold; color : rgb{}; font-size: 18px;".format(self.dictionary_label_color_RGB[roi.get_label()]))

        button.clicked.connect(partial(self.select_ROI, roi.get_id()))
        self.Scroll_area.add_single_ROI(self.ui, button)
        
    def edit_ROI(self, roi):
        self.id_edit = roi.get_id()
        self.controllerSingleROI.edit_ROI(self.ui, roi)

    def delete_ROI(self):
        self.controllerSingleROI.delet_ROI(self.ui, self.list_frame, self.id_image)
        self.set_image_equirectangular_view(self.id_image)

    def select_ROI(self, id):
        roi = self.list_frame[self.id_image].get_list_roi()[id-1]
        self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
        self.center_point = roi.get_center_point()
        WHITE = (255,255,255)
        self.update_view(label_color= WHITE)
        self.controllerSingleROI.select_ROI(id, self.ui)
        self.ui.button_edit_ROI.clicked.connect(partial(self.edit_ROI, roi))
        
    #Compose ROI
    def highlight_compose_ROI(self, id):
        roi = self.list_frame[self.id_image].get_compose_ROI(id)
        if roi :
            self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
            self.center_point = roi.get_center_point()
            WHITE = (255,255,255)
            self.update_view(label_color= WHITE)

    def go_to_init_frame(self):
        self.highlight_compose_ROI(self.controllerComposeROI.get_first_ROI(self.ui))

    def go_to_end_frame(self):
        self.highlight_compose_ROI(self.controllerComposeROI.get_last_ROI(self.ui))
    
    def select_compose_ROI(self, id):
        self.controllerComposeROI.select_compose_ROI(id, self.ui)
        self.highlight_compose_ROI(id)
        
    def add_compose_ROI_in_scroll_area(self, compose_ROI):
        button = QtWidgets.QPushButton("Id= {}, Frame 1°={} 2°={}, Label= {}".format(compose_ROI.get_id(), compose_ROI.get_frame_init(),
                                                                                        compose_ROI.get_frame_end(), compose_ROI.get_label()))

        button.setStyleSheet("font: bold; color : rgb{}; font-size: 18px;".format(self.dictionary_label_color_RGB[compose_ROI.get_label()]))
        
        button.clicked.connect(partial(self.select_compose_ROI, compose_ROI.get_id()))
        self.Scroll_area.add_compose_ROI(self.ui, button)

    def add_disable_compose_ROI_in_scroll_area(self, compose_ROI):
        button = QtWidgets.QPushButton("Id= {}, Frame 1°={} 2°={}, Label= {}".format(compose_ROI.get_id(), compose_ROI.get_frame_init(),
                                                                                        compose_ROI.get_frame_end(), compose_ROI.get_label()))

        button.setStyleSheet("font: bold; color : rgb{}; font-size: 18px;".format(self.dictionary_label_color_RGB[compose_ROI.get_label()]))

        button.clicked.connect(partial(self.select_compose_ROI, compose_ROI.get_id()))
        button.setEnabled(False)
        self.Scroll_area.add_compose_ROI(self.ui, button)

    def edit_one_compose_ROI(self):
        #disable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_disable_compose_ROI_in_scroll_area(compose_ROI)
        
        self.controllerComposeROI.edit_one_compose_ROI(self.ui)

    def cancel_edit_one_compose_ROI(self):
        #enable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_compose_ROI_in_scroll_area(compose_ROI)

        self.controllerComposeROI.cancel_edit_one_compose_ROI(self.ui)

    def save_edit_one_compose_ROI(self):
        self.controllerComposeROI.save_edit_one_compose_ROI(self.ui, self.center_point, self.nfov.FOV, self.list_frame, self.id_image, self.dictionary_label_color, self.path_frames_original)
        self.set_image_equirectangular_view(self.id_image)

        #enable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_compose_ROI_in_scroll_area(compose_ROI)

    def delete_compose_ROI(self):

        id_select_compose_ROI = self.controllerComposeROI.delete_compose_ROI(self.ui, self.list_frame, self.dictionary_label_color, self.path_frames_original)
        self.Scroll_area.clear_scroll_area_compose_ROI()

        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            if compose_ROI.get_id() > id_select_compose_ROI:
                new_id = compose_ROI.get_id() - 1
                compose_ROI.set_id(new_id)
            self.add_compose_ROI_in_scroll_area(compose_ROI)

        self.set_image_equirectangular_view(self.id_image)
        
    def set_first_ROI(self):
        label = self.Save_proprieties.get_label_compose_ROI()
        movement = self.Save_proprieties.get_movement_flag()
        self.controllerComposeROI.set_first_ROI(self.ui, label, self.center_point,self.nfov.FOV, self.id_image, movement, self.list_frame, self.dictionary_label_color)
        self.close_save_compose_roi_window()

        #disable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_disable_compose_ROI_in_scroll_area(compose_ROI)

    def save_finish_compose_ROI(self):

        flag,roi_compose = self.controllerComposeROI.save_finish_compose_ROI(self.ui, self.center_point, self.nfov.FOV, self.id_image)
        if flag == True:
            self.controllerComposeROI.set_compose_ROI(self.ui, self.list_frame, self.dictionary_label_color)
            self.add_compose_ROI_in_scroll_area(roi_compose)

            #enable buttons in scroll area
            self.Scroll_area.clear_scroll_area_compose_ROI()
            for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
                self.add_compose_ROI_in_scroll_area(compose_ROI)
        else:
            self.ui_upload.text_result.setText("ID Frame wrong!")
            self.window_upload_result.show()

    def add_new_compose_ROI(self):
        self.go_to_end_frame()
        self.controllerComposeROI.disable_button(self.ui)
        self.ui.button_add_new_CROI.setEnabled(False)
        self.ui.button_cancel_edit_compose_ROI.setEnabled(True)
        self.ui.button_set_new_CROI.setEnabled(True)

    def set_new_add_compose_ROI(self):
        #button dois de setar o init
        self.controllerComposeROI.add_new_composer_ROI(self.ui, self.center_point,self.nfov.FOV, self.id_image)
        
        #disable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_disable_compose_ROI_in_scroll_area(compose_ROI)

    def add_compose_ROI(self):
        self.controllerComposeROI.add_compose_ROI(self.ui)
        self.go_to_end_frame()
        
        #disable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_disable_compose_ROI_in_scroll_area(compose_ROI)
            
    def save_add_compose_ROI(self):
        self.controllerComposeROI.save_add_compose_ROI(self.center_point, self.nfov.FOV, self.id_image)
        self.controllerComposeROI.set_add_compose_ROI(self.ui, self.list_frame, self.dictionary_label_color)
        self.ui.button_save_add_ROI.setEnabled(False)
        self.ui.button_init_ROI.setEnabled(True)
        self.ui.button_cancel_edit_compose_ROI.setEnabled(False)

        #enable buttons in scroll area
        self.Scroll_area.clear_scroll_area_compose_ROI()
        for compose_ROI in self.controllerComposeROI.get_list_compose_ROI():
            self.add_compose_ROI_in_scroll_area(compose_ROI)  

    def  edit_long_compose_ROI(self):
        self.ui.button_edit_long_CROI.setEnabled(False)  
        self.controllerComposeROI.disable_button(self.ui)
        self.ui.button_init_ROI.setEnabled(False)
        self.ui.button_set_init_CROI.setEnabled(True)
        self.ui.button_cancel_edit_compose_ROI.setEnabled(True)


    def set_init_edit_group(self):
        self.controllerComposeROI.edit_group_compose_ROI(self.ui, self.center_point,self.nfov.FOV, self.id_image)
        self.ui.button_set_init_CROI.setEnabled(False)
        self.ui.button_save_CROI.setEnabled(True)

    def save_edit_group(self):
        self.controllerComposeROI.save_edit_group_compose_ROI(self.center_point,self.nfov.FOV, self.id_image)
        self.controllerComposeROI.set_edit_group_compose_ROI(self.ui, self.list_frame, self.dictionary_label_color, self.path_frames_original)
        self.ui.button_save_CROI.setEnabled(False)
        self.ui.button_cancel_edit_compose_ROI.setEnabled(False)
        self.ui.button_save.setEnabled(True)
        self.ui.button_init_ROI.setEnabled(True)


    #CSV
    def save_csv(self):
        self.csv.save_file(self.list_frame, self.controllerComposeROI.get_list_compose_ROI(), self.fps, self.nfov, self.dictionary_label_color)

    def upload_csv(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'files ( *.csv)')
        file_path = fname[0]

        if file_path != '':
            self.Scroll_area.clear_scroll_area_compose_ROI()
            self.controllerComposeROI.clear_list_compose_ROI()
            size = (self.ui.equi_image.width(),self.ui.equi_image.height())
            self.id_image = 0
            id =0
            #clear images
            for frame in self.list_frame:
                #set new image for anotation object
                path_original_frame = osp.join(self.path_frames_original, '{}.jpg'.format(id))
                frame_original = cv2.imread(path_original_frame)
                frame_original = cv2.resize(frame_original, size, interpolation=cv2.INTER_CUBIC)
                frame.set_image(frame_original)
                id+=1

            upload_csv = Upload_CSV(file_path)
            upload_csv.read_csv(self.list_frame, self.dictionary_label_color, self.controllerComposeROI)
            for roi in self.controllerComposeROI.get_list_compose_ROI():
                self.add_compose_ROI_in_scroll_area(roi)
                
            self.set_image_equirectangular_view(0)
            self.ui.button_save.setEnabled(True)

            self.ui_upload.text_result.setText("Upload Sucesfull!")
            
        else:
            self.ui_upload.text_result.setText("Upload Fail!")

        self.window_upload_result.show()


def main():
    app = QtWidgets.QApplication([])
    widget = AnottationWindow()
    widget.showMaximized()
    app.exec_()

if __name__ == "__main__":
    main()







