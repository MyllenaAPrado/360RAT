from PyQt5 import QtWidgets, QtGui
from Interfaces.save_ok__window import Ui_save
from Service.BlackMask import BlackMask
from Service.GetInputUser import GetInput
from sys import platform
import csv
import os
import sys
import shutil
import cv2
import os.path as osp

class CSV:
    
    def __init__(self, user):
        self.list_dictionary = []
        self.user = user
        self.window_save_csv = QtWidgets.QMainWindow()
        if platform == "linux" or platform == "linux2":
            # linux
            self.window_save_csv.setWindowIcon(QtGui.QIcon(os.getcwd() + "/Images/icon.png"))

        elif platform == "win32":
            # Windows...
            self.window_save_csv.setWindowIcon(QtGui.QIcon(os.getcwd() + "\Images\icon.png"))
        
        
        self.window_save_csv.setWindowTitle("360Rat")
        self.ui_save = Ui_save()
        self.ui_save.setupUi(self.window_save_csv)
        self.ui_save.pushButton_OK.clicked.connect(self.close_save_csv_window)

        self.window_input = GetInput()
        ui_input = self.window_input.get_ui()
        ui_input.button_OK.clicked.connect(self.save)
        ui_input.input.editingFinished.connect(self.save)
        self.fps = 60

        self.flag_path = False

    def close_save_csv_window(self):
        self.window_save_csv.hide()

    def save_file(self, list_imagens, list_ROI, fps, FOV, dictionary, flag):
        self.list_image_anotation = list_imagens
        self.list_compose_ROI = list_ROI
        self.fps = fps
        self.nfov = FOV
        self.dict_color = dictionary

        self.window_input.set_text_window("Enter your name:")
        window = self.window_input.get_window()
        self.flag_path = flag
        
        
        window.show()

    def save(self):

        self.window_input.close_window()
        self.user = self.window_input.get_input_text()
        #self.window_input.clear_input_field()
        self.list_dictionary.clear()
        if self.flag_path == False:
            path = os.getcwd()
            cwd = osp.join(path, "videosAnotated")
        else:
            fname = QtWidgets.QFileDialog.getExistingDirectory()
            cwd = fname

        self.save_imagens_files(cwd)
        self.create_dictionary()
        self.save_dictionary(cwd)       

        self.window_save_csv.show()

    def save_imagens_files(self, cwd):        
        
        head, tail = os.path.split(self.list_image_anotation[0].get_path())
        
        path = osp.join(cwd, self.user)
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(*[cwd, self.user, tail])
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        if not os.path.exists(path):
            os.makedirs(path)


        path = os.path.join(*[cwd, self.user, tail, "annotation"])        
        if not os.path.exists(path):
            os.makedirs(path)
        

        mask_path = os.path.join(*[cwd, self.user, tail, "blackMask"])
        if not os.path.exists(mask_path):
            os.makedirs(mask_path)      

        path_video = os.path.join(*[cwd, self.user, tail, "video.mp4"])
        shape = self.list_image_anotation[0].get_image().shape
        width = shape[1] 
        height = shape[0] 
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_DBSCAN = cv2.VideoWriter(path_video, fourcc, self.fps, (width,height))
        blackmask = BlackMask()

        for image in self.list_image_anotation:
            img_aux = image.get_image().copy()
            if image.get_list_roi():
                
                for roi in image.get_list_roi():                    
                    #draw ROI
                    self.nfov(img_aux)
                    self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
                    self.nfov.updateNFOV(roi.get_center_point())

                    self.nfov.draw_NFOV_edges(img_aux, label_color= self.dict_color[roi.get_label()])
            
            
            mask_out_path = osp.join(mask_path, '{}.jpg'.format(image.get_id()))
            blackmask.draw_black_mask(mask_out_path, image.get_list_roi(), image.get_list_compose_ROI())

            frame_out_path = osp.join(path, '{}.jpg'.format(image.get_id()))
            #save image in directory
            cv2.imwrite(frame_out_path, img_aux)
            out_DBSCAN.write(img_aux)

        out_DBSCAN.release()

    def create_dictionary(self):
        for image in self.list_image_anotation:
            for roi in image.get_list_roi():
                roi_dict = {
                            "Type" : 0,
                            "Frame" : image.get_id(),
                            "Id roi" : roi.get_id(),
                            "Center_point X" : roi.get_center_point()[0],
                            "Center_point Y" : roi.get_center_point()[1],
                            "ROI H" : roi.get_fov()[0],
                            "ROI W" : roi.get_fov()[1],
                            "Label" : roi.get_label(), 
                            "Movement" : "**",
                            "Frame_end" : 0,
                            "Center_point_end X" : 0,
                            "Center_point_end Y" :0,
                            "ROI_end H" : 0,
                            "ROI_end W" : 0,
                            "user": self.user,
                            }
                self.list_dictionary.append(roi_dict)
            
            for roi in image.get_list_compose_ROI():
                roi_dict = {
                            "Type" : 1,
                            "Frame" : image.get_id(),
                            "Id roi" : roi.get_id(),
                            "Center_point X" : roi.get_center_point()[0],
                            "Center_point Y" : roi.get_center_point()[1],
                            "ROI H" : roi.get_fov()[0],
                            "ROI W" : roi.get_fov()[1],
                            "Label" : roi.get_label(), 
                            "Movement" : roi.get_movement(),
                            "Frame_end" : 0,
                            "Center_point_end X" : 0,
                            "Center_point_end Y" :0,
                            "ROI_end H" : 0,
                            "ROI_end W" : 0,
                            "user": self.user,
                            }
                self.list_dictionary.append(roi_dict)

        for roi in self.list_compose_ROI:
            roi_dict = {
                        "Type" : 2,
                        "Frame" : roi.get_frame_init(),
                        "Id roi" : roi.get_id(),
                        "Center_point X" : roi.get_center_point_init()[0],
                        "Center_point Y" : roi.get_center_point_init()[1],
                        "ROI H" : roi.get_fov_init()[0],
                        "ROI W" : roi.get_fov_init()[1],
                        "Label" : roi.get_label(), 
                        "Movement" : roi.get_movement(),
                        "Frame_end" : roi.get_frame_end(),
                        "Center_point_end X" : roi.get_center_point_end()[0],
                        "Center_point_end Y" : roi.get_center_point_end()[1],
                        "ROI_end H" : roi.get_fov_end()[0],
                        "ROI_end W" : roi.get_fov_end()[1],
                        "user": self.user,
                        }
            self.list_dictionary.append(roi_dict)

    def save_dictionary(self, cwd):
        head, tail = os.path.split(self.list_image_anotation[0].get_path())
        
        path = os.path.join(*[cwd,self.user, tail, f'list_of_Roi_{self.user}_{tail}.csv'])
        if os.path.exists(path):
            os.remove(path)

        keys = self.list_dictionary[0].keys()
        with open(path, 'w', newline='') as output_file:
                #dict_writer = csv.DictWriter(output_file, keys)
                dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
                dict_writer.writeheader()
                dict_writer.writerows(self.list_dictionary)
            
