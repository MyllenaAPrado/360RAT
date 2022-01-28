from Entities.ROI import ROI
from Entities.ComposeROI import Compose_ROI
from Entities.SimplifiedComposeROI import Simple_compose_ROI
from Service.SphereFov import NFOV
import csv
import cv2
import numpy as np

class Upload_CSV:
    
    def __init__(self, path):
        self.path = path

    def csv_compatible_video(self, list_imagens):
        with open(self.path, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader)
            self.data = list(reader)
            end_frame =0
            for row in self.data:
                type_roi = int(row[0])
                if type_roi == 1 :
                    end_frame = id_frame = int(row[1])
                if type_roi == 2 :
                    if(end_frame > len(list_imagens)):
                        return False
                    else:
                        return True
        return True

    def read_csv(self, list_imagens, dictionary_label_color, control_compose_ROI):

        with open(self.path, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader)
            self.data = list(reader)
            for row in self.data:
                type_roi = int(row[0])
                id_frame = int(row[1])
                id_roi = int(row[2])
                center_point = np.array([float(row[3]), float(row[4])])
                fov = np.array([float(row[5]), float(row[6])])
                label = row[7]
                movement = row[8]
                

                '''print("type: ", type_roi)
                print("frame: ", id_frame)
                print("id:", id_roi)
                print("center_point:",center_point)
                print("fov:", fov)
                print("Label:", label)
                print("movement:", movement)
                '''

                if type_roi == 0 : #single ROI
                    roi = ROI(center_point, fov, label)
                    list_imagens[id_frame].add_ROI(roi)
                
                if type_roi == 1 :
                    compose_roi = Simple_compose_ROI(id_roi, center_point, fov, label, movement)
                    list_imagens[id_frame].add_compose_ROI(compose_roi)
                    nfov = NFOV()
                    nfov(list_imagens[id_frame].get_image())
                    nfov.set_fov(fov[1], fov[0])
                    nfov.updateNFOV(center_point)
                    nfov.draw_NFOV_edges(list_imagens[id_frame].get_image(), label_color= dictionary_label_color[label])

                if type_roi == 2 :
                    id_frame_end = int(row[9])
                    center_point_end = np.array([float(row[10]), float(row[11])])
                    fov_end = np.array([float(row[12]), float(row[13])])

                    roi_compose= Compose_ROI(id_roi, center_point, fov, id_frame, label, movement)
                    roi_compose.set_end_ROI(center_point_end, fov_end, id_frame_end)
                    control_compose_ROI.add_ROI(roi_compose)


                
            #self.dictionary_label_color = {rows[0]:rows[1] for rows in self.data}
            #self.dictionary_label_color_RGB = {rows[0]:rows[2] for rows in self.data}
        #print(self.dictionary_label_color)
        #print(self.dictionary_label_color_RGB)

        '''
            for image in self.list_frame:
                image.delet_list_roi()
            self.add_label_roi()
            if self.list_frame:
                self.set_image_equirectangular_view(self.id_image)
        '''



