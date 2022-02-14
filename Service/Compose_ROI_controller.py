from Interfaces.Anottation_window import Ui_Anottation
from Service.SphereFov import NFOV
from Entities.SimplifiedComposeROI import Simple_compose_ROI
from Entities.ComposeROI import Compose_ROI
import numpy as np
import os.path as osp
import cv2

class ComposeROIController():
    def __init__(self, ui):

        self.list_compose_ROI = []
        self.id_compose_ROI = 0
        self.id_select_compose_ROI = 0
        self.nfov = NFOV()
        self.disable_button(ui)
        
    def disable_button(self, ui):
        ui.button_edit_one_compose_ROI.setEnabled(False)
        ui.button_save_edit_compose_ROI.setEnabled(False)
        ui.button_cancel_edit_compose_ROI.setEnabled(False)
        ui.button_delete_compose_ROI.setEnabled(False)
        ui.button_go_to_first.setEnabled(False)
        ui.button_go_to_last.setEnabled(False)
        ui.button_add_compose_roi.setEnabled(False)
        ui.button_save_add_ROI.setEnabled(False)
        ui.button_add_new_CROI.setEnabled(False)
        ui.button_set_new_CROI.setEnabled(False)
        ui.button_edit_long_CROI.setEnabled(False)
        ui.button_set_init_CROI.setEnabled(False)
        ui.button_save_CROI.setEnabled(False)

    def get_list_compose_ROI(self):
        return self.list_compose_ROI
    
    def clear_list_compose_ROI(self):
        self.id_compose_ROI = 0
        self.id_select_compose_ROI = 0
        self.list_compose_ROI.clear()

    def get_roi_compose(self):
        return self.roi_compose
    
    def get_id_selected_compose_ROI(self):
        return self.id_select_compose_ROI

    def add_ROI(self, roi):
        self.id_compose_ROI += 1
        self.list_compose_ROI.append(roi)

    def set_first_ROI(self, ui, label, center_point, FOV, id_image, movement_roi,  list_frame, dictionary_label_color):
        self.id_compose_ROI += 1
        self.roi_compose= Compose_ROI(self.id_compose_ROI, center_point, FOV, id_image, label, movement_roi)

        #draw ROI
        self.nfov(list_frame[id_image].get_image())
        self.nfov.set_fov(FOV[1], FOV[0])
        self.nfov.updateNFOV(center_point)

        self.nfov.draw_NFOV_edges(list_frame[id_image].get_image(), label_color= dictionary_label_color[label])


        ui.button_init_ROI.setEnabled(False)
        ui.button_end_ROI.setEnabled(True)
        ui.button_go_to_first.setEnabled(False)
        ui.button_go_to_last.setEnabled(False)

    def save_finish_compose_ROI(self, ui, center_point, FOV, id_image):

        if id_image <= self.roi_compose.get_frame_init():
            return False, None
        
        ui.button_init_ROI.setEnabled(True)
        ui.button_end_ROI.setEnabled(False)

        self.roi_compose.set_end_ROI(center_point, FOV, id_image)
        self.roi_compose.calcule_pos_ROI_variation()
        self.list_compose_ROI.append(self.roi_compose)        
        
        return True, self.roi_compose

    def set_compose_ROI(self, ui, list_frame, dictionary_label_color):

        #set image of nfov
        self.nfov(list_frame[self.roi_compose.get_frame_init()].get_image())

        for i in range(0, self.roi_compose.get_number_of_ROI(), 1):
            if self.roi_compose.get_movement():
                    pos_x = self.roi_compose.get_center_point_init()[0] + (i * self.roi_compose.get_delta_x())
                    pos_y = self.roi_compose.get_center_point_init()[1] + (i * self.roi_compose.get_delta_y())
                    fov_h = self.roi_compose.get_fov_init()[0] + (i * self.roi_compose.get_delta_fov_h())
                    fov_w = self.roi_compose.get_fov_init()[1] + (i * self.roi_compose.get_delta_fov_w())

            else :
                    pos_x = self.roi_compose.get_center_point_init()[0]
                    pos_y = self.roi_compose.get_center_point_init()[1]
                    fov_h = self.roi_compose.get_fov_init()[0]
                    fov_w = self.roi_compose.get_fov_init()[1]
            
            roi = Simple_compose_ROI(self.id_compose_ROI , np.array([pos_x, pos_y]), [fov_h, fov_w], self.roi_compose.get_label(), self.roi_compose.get_movement())

            #save roi in a list
            list_frame[self.roi_compose.get_frame_init()+ i].add_compose_ROI(roi)
            self.nfov.set_fov(fov_w, fov_h)
            self.nfov.updateNFOV(np.array([pos_x, pos_y]))
            self.nfov.draw_NFOV_edges(list_frame[self.roi_compose.get_frame_init()+ i].get_image(), label_color= dictionary_label_color[self.roi_compose.get_label()])

        #back to init frame of compose roi
        #ui.slider_video_duration.setValue(self.roi_compose.get_frame_init())

    def edit_one_compose_ROI(self, ui):
        ui.button_edit_one_compose_ROI.setEnabled(False)
        ui.button_delete_compose_ROI.setEnabled(False)
        ui.button_cancel_edit_compose_ROI.setEnabled(True)
        ui.button_save_edit_compose_ROI.setEnabled(True)
        ui.button_add_compose_roi.setEnabled(False)
        ui.button_go_to_first.setEnabled(False)
        ui.button_go_to_last.setEnabled(False)
        ui.button_init_ROI.setEnabled(False)
        ui.button_add_new_CROI.setEnabled(False)

    def cancel_edit_one_compose_ROI(self, ui):
        ui.button_cancel_edit_compose_ROI.setEnabled(False)
        ui.button_save_edit_compose_ROI.setEnabled(False)
        ui.button_init_ROI.setEnabled(True)
        self.disable_button(ui)

    def save_edit_one_compose_ROI(self, ui, center_point, FOV, list_frame, id_image, dictionary_label_color, path_frame):
        #print(self.id_select_compose_ROI)
        #set new parametes for roi
        roi = list_frame[id_image].get_list_compose_ROI()[self.id_select_compose_ROI - 1]
        roi.set_center_point(center_point)
        roi.set_fov(FOV)

        ui.button_cancel_edit_compose_ROI.setEnabled(False)
        ui.button_save_edit_compose_ROI.setEnabled(False)
        ui.button_init_ROI.setEnabled(True)

        #set new image for anotation object
        size = (ui.equi_image.width(),ui.equi_image.height())
        path_original_frame = osp.join(path_frame, '{}.jpg'.format(id_image))
        frame_original = cv2.imread(path_original_frame)
        frame_original = cv2.resize(frame_original, size, interpolation=cv2.INTER_CUBIC)
        list_frame[id_image].set_image(frame_original)
        
        #list_frame[id_image].set_image(list_frame_copy[id_image].get_image().copy())

        #set image in nfov to draw
        self.nfov(list_frame[id_image].get_image())

        #draw all rois in new iamge
        for roi in list_frame[id_image].get_list_compose_ROI():
            self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
            self.nfov.updateNFOV(roi.get_center_point())
            self.nfov.draw_NFOV_edges(list_frame[id_image].get_image(), label_color= dictionary_label_color[roi.get_label()])

        self.disable_button(ui)

    def select_compose_ROI(self, id, ui):
        ui.button_go_to_first.setEnabled(True)
        ui.button_go_to_last.setEnabled(True)
        ui.button_edit_one_compose_ROI.setEnabled(True)
        ui.button_delete_compose_ROI.setEnabled(True)
        ui.button_add_compose_roi.setEnabled(True)
        ui.button_add_new_CROI.setEnabled(True)
        ui.button_edit_long_CROI.setEnabled(True)
        self.id_select_compose_ROI = id
        #print("Select:", self.id_select_compose_ROI)
    
    def delete_compose_ROI(self, ui, list_frame, dictionary_label_color, path_frame):
 
        self.id_compose_ROI-=1
        compose_roi = self.list_compose_ROI[self.id_select_compose_ROI-1]
        size = (ui.equi_image.width(),ui.equi_image.height())

        for id_frame in range (compose_roi.get_frame_init(), (compose_roi.get_frame_end() + 1), 1):

            #set new image for anotation object
            path_original_frame = osp.join(path_frame, '{}.jpg'.format(id_frame))
            frame_original = cv2.imread(path_original_frame)
            frame_original = cv2.resize(frame_original, size, interpolation=cv2.INTER_CUBIC)
            list_frame[id_frame].set_image(frame_original)

            #list_frame[id_frame].set_image(list_frame_copy[id_frame].get_image().copy())
            list_frame[id_frame].delete_compose_ROI(self.id_select_compose_ROI)

            #draw all the compose roi again
            for roi in list_frame[id_frame].get_list_compose_ROI():
                self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
                self.nfov.updateNFOV(roi.get_center_point())
                self.nfov.draw_NFOV_edges(list_frame[id_frame].get_image(), label_color= dictionary_label_color[roi.get_label()])

        #remove the compose roi
        self.list_compose_ROI.remove(compose_roi)
        self.disable_button(ui)

        return self.id_select_compose_ROI

    def get_first_ROI(self, ui):
        #change the value of slider to change the frame
        id_frame = self.list_compose_ROI[self.id_select_compose_ROI-1].get_frame_init()
        ui.slider_video_duration.setValue(id_frame)
        ui.button_go_to_first.setEnabled(False)
        ui.button_go_to_last.setEnabled(True)

        return self.id_select_compose_ROI

    def get_last_ROI(self, ui):
        
        #change the value of slider to change the frame
        id_frame = self.list_compose_ROI[self.id_select_compose_ROI-1].get_frame_end()
        ui.slider_video_duration.setValue(id_frame)
        ui.button_go_to_last.setEnabled(False)
        ui.button_go_to_first.setEnabled(True)

        return self.id_select_compose_ROI

    def add_new_composer_ROI(self, ui, center_point, FOV, id_image):
        
        aux_compose_ROI = self.list_compose_ROI[self.id_select_compose_ROI-1]
        self.roi_add= Compose_ROI(self.id_compose_ROI, center_point, FOV, id_image, aux_compose_ROI.get_label(), aux_compose_ROI.get_movement())

        ui.button_init_ROI.setEnabled(False)
        ui.button_edit_one_compose_ROI.setEnabled(False)
        ui.button_delete_compose_ROI.setEnabled(False)
        ui.button_add_compose_roi.setEnabled(False)
        ui.button_set_new_CROI.setEnabled(False)
        ui.button_save_add_ROI.setEnabled(True)
        ui.button_cancel_edit_compose_ROI.setEnabled(True)

    def add_compose_ROI(self, ui):

        aux_compose_ROI = self.list_compose_ROI[self.id_select_compose_ROI-1]

        self.roi_add = Compose_ROI(0,aux_compose_ROI.get_center_point_end(), aux_compose_ROI.get_fov_end(), (aux_compose_ROI.get_frame_end()+1), aux_compose_ROI.get_label(), aux_compose_ROI.get_movement())
        #print("Mov", aux_compose_ROI.get_movement())
       
        #control of buttons
        ui.button_init_ROI.setEnabled(False)
        ui.button_edit_one_compose_ROI.setEnabled(False)
        ui.button_delete_compose_ROI.setEnabled(False)
        ui.button_add_compose_roi.setEnabled(False)
        ui.button_add_new_CROI.setEnabled(False)
        ui.button_save_add_ROI.setEnabled(True)
        ui.button_cancel_edit_compose_ROI.setEnabled(True)
        
    def save_add_compose_ROI(self, center_point, FOV, id_image):
        self.roi_add.set_end_ROI(center_point, FOV, id_image)
        self.roi_add.calcule_pos_ROI_variation()

    def set_add_compose_ROI(self, ui, list_frame, dictionary_label_color):
        #set image of nfov
        self.nfov(list_frame[self.roi_add.get_frame_init()].get_image())
        #print("Flag:", self.roi_add.get_movement())
        
        for i in range(0, self.roi_add.get_number_of_ROI(), 1):
            if self.roi_add.get_movement():
                    pos_x = self.roi_add.get_center_point_init()[0] + (i * self.roi_add.get_delta_x())
                    pos_y = self.roi_add.get_center_point_init()[1] + (i * self.roi_add.get_delta_y())
                    fov_h = self.roi_add.get_fov_init()[0] + (i * self.roi_add.get_delta_fov_h())
                    fov_w = self.roi_add.get_fov_init()[1] + (i * self.roi_add.get_delta_fov_w())

            else :
                    pos_x = self.roi_add.get_center_point_init()[0]
                    pos_y = self.roi_add.get_center_point_init()[1]
                    fov_h = self.roi_add.get_fov_init()[0]
                    fov_w = self.roi_add.get_fov_init()[1]
            
            roi = Simple_compose_ROI(self.id_select_compose_ROI , np.array([pos_x, pos_y]), [fov_h, fov_w], self.roi_add.get_label(), self.roi_add.get_movement())

            #save roi in a list
            list_frame[self.roi_add.get_frame_init()+ i].add_compose_ROI(roi)
            self.nfov.set_fov(fov_w, fov_h)
            self.nfov.updateNFOV(np.array([pos_x, pos_y]))
            self.nfov.draw_NFOV_edges(list_frame[self.roi_add.get_frame_init()+ i].get_image(), label_color= dictionary_label_color[self.roi_add.get_label()])
        
        self.list_compose_ROI[self.id_select_compose_ROI-1].set_end_ROI(self.roi_add.get_center_point_end(), self.roi_add.get_fov_end(), self.roi_add.get_frame_end())

        #back to init frame of compose roi
        ui.slider_video_duration.setValue(self.roi_add.get_frame_init())

    def edit_group_compose_ROI(self, ui, center_point, FOV, id_image):
        aux_compose_ROI = self.list_compose_ROI[self.id_select_compose_ROI-1]
        self.roi_add= Compose_ROI(self.id_compose_ROI, center_point, FOV, id_image, aux_compose_ROI.get_label(), aux_compose_ROI.get_movement())

    def save_edit_group_compose_ROI(self, center_point, FOV, id_image):
        self.roi_add.set_end_ROI(center_point, FOV, id_image)
        self.roi_add.calcule_pos_ROI_variation()

    def set_edit_group_compose_ROI(self, ui, list_frame, dictionary_label_color, path_frame):
        #set image of nfov
        self.nfov(list_frame[self.roi_add.get_frame_init()].get_image())
        #print("Flag:", self.roi_add.get_movement())
        
        for i in range(0, self.roi_add.get_number_of_ROI(), 1):
            if self.roi_add.get_movement():
                    pos_x = self.roi_add.get_center_point_init()[0] + (i * self.roi_add.get_delta_x())
                    pos_y = self.roi_add.get_center_point_init()[1] + (i * self.roi_add.get_delta_y())
                    fov_h = self.roi_add.get_fov_init()[0] + (i * self.roi_add.get_delta_fov_h())
                    fov_w = self.roi_add.get_fov_init()[1] + (i * self.roi_add.get_delta_fov_w())

            else :
                    pos_x = self.roi_add.get_center_point_init()[0]
                    pos_y = self.roi_add.get_center_point_init()[1]
                    fov_h = self.roi_add.get_fov_init()[0]
                    fov_w = self.roi_add.get_fov_init()[1]

            
            #set new parametes for roi
            #logic works with only on compose ROI by frame
            roi = list_frame[self.roi_add.get_frame_init()+ i].get_list_compose_ROI()[0]
            roi.set_center_point(np.array([pos_x, pos_y]))
            roi.set_fov([fov_h, fov_w])

            #set new image for anotation object
            size = (ui.equi_image.width(),ui.equi_image.height())
            path_original_frame = osp.join(path_frame, '{}.jpg'.format(self.roi_add.get_frame_init()+ i))
            frame_original = cv2.imread(path_original_frame)
            frame_original = cv2.resize(frame_original, size, interpolation=cv2.INTER_CUBIC)
            list_frame[self.roi_add.get_frame_init()+ i].set_image(frame_original)
        
            #set image in nfov to draw
            self.nfov(list_frame[self.roi_add.get_frame_init()+ i].get_image())

            #draw all rois in new iamge
            for roi in list_frame[self.roi_add.get_frame_init()+ i].get_list_compose_ROI():
                self.nfov.set_fov(roi.get_fov()[1], roi.get_fov()[0])
                self.nfov.updateNFOV(roi.get_center_point())
                self.nfov.draw_NFOV_edges(list_frame[self.roi_add.get_frame_init()+ i].get_image(), label_color= dictionary_label_color[roi.get_label()])

        #back to init frame of compose roi
        ui.slider_video_duration.setValue(self.roi_add.get_frame_init())


        

        