from SphereFov import NFOV
from PyQt5 import QtWidgets
import csv
import numpy as np
import cv2
import os
from pathlib import Path

class main():

    def __init__(self):

        self.list_imagens = [] 
        self.nfov = NFOV()
        self.set_colors_variables()
        self.dictionary_label_color = self.get_dictionary_color()
        #self.video_path = "path\\video_22_nas_1000x500_30.mp4"
        self.video_path = "path\\video_22_nas_4320x2160_30.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.fps_input = 5
        self.fps_output = 30
        data_folder = Path("path/video_22_nas_1000x500_5.mp4")
        self.path_csv = data_folder /  "list_of_Roi.csv"
        self.path_output_video = "output_4320x2160.mp4"
        self.width = 4320
        self.height = 2160
        self.read_csv()


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

    def get_dictionary_color(self):
        dictionary= {'Accessory' : self.GREEN, 'Animal' : self.ORANGE,
                                       'Appliance' : self.PINK, 'Electronic' : self.PURPLE, 
                                       'Food' : self.SAPGREEN, 'Furniture' : self.BLUE,
                                       'Indoor' : self.YELLOW, 'Kitchen' : self.MANGETA, 
                                       'Outdoor' : self.BROWN, 'Person' : self.CADETBLUE, 
                                       'Sports' : self.GOLD, 'Vehicle' : self.LIGHTPINK}
        '''
        dictionary = {'Primary' : self.GREEN, 'Secondary' : self.PURPLE, 
                                       'Tertiary' : self.BLUE, 'Quaternary' : self.YELLOW}
        '''

        return dictionary


    def read_csv(self):
        last_id_frame = -1
        list_images = []

        with open(self.path_csv, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader)
            self.data = list(reader)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_DBSCAN = cv2.VideoWriter(self.path_output_video, fourcc, 30, (self.width,self.height))
            
            for row in self.data:
                type_roi = int(row[0])
                id_frame = int(row[1])
                id_roi = int(row[2])
                center_point = np.array([float(row[3]), float(row[4])])
                fov = np.array([float(row[5]), float(row[6])])
                label = row[7]
                movement = row[8]

                if last_id_frame != id_frame:
                    for frame in list_images:
                        out_DBSCAN.write(frame)
                    list_images.clear()
                    for i in range (0, int(self.fps_output / self.fps_input) , 1):
                        ret, frame = self.cap.read()
                        list_images.append(frame)
                    last_id_frame = id_frame

                if type_roi == 0 or type_roi == 1: 
                    for frame in list_images:
                        self.draw_fov(frame, fov, center_point, label)

            for frame in list_images:
                 out_DBSCAN.write(frame)

            out_DBSCAN.release()
                
    def draw_fov(self, image, fov, center_point, label):
        self.nfov(image, self.width, self.height)
        self.nfov.set_fov(fov[1], fov[0])
        self.nfov.updateNFOV(center_point)
        self.nfov.draw_NFOV_edges(image, label_color= self.dictionary_label_color[label])


if __name__ == "__main__":
    main()