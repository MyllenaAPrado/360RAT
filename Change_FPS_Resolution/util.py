from SphereFov import NFOV
from PyQt5 import QtWidgets
import csv
import numpy as np
import cv2
import os
from pathlib import Path
from os import listdir
from os.path import isfile, join

class main():

    def __init__(self):

        self.list_imagens = [] 
        self.nfov = NFOV()
        self.set_colors_variables()
        self.dictionary_label_color = self.get_dictionary_color()
        
        #Change the follow variables
        #intit frame to draw
        self.id_init = 0
        #final frame to draw
        self.id_final = 151
        #intit frame to draw
        self.id_cube = '000200'


        self.nome_video = "Amizade_1080x540_5.mp4"
        self.nome_folder_cube= "Amizade_1080x540_5"
        
        #place where the csv are. The image output will be in this folder too
        
        data_folder = f"C:\\Users\\vntmypr\\Documents\\myllena\\TCC2\\Git\\360RAT\\files CSV\\second part\\{self.nome_video}"
        
        for id_frame in range (self.id_init, self.id_final, 1):

            #Path of original frame
            #self.image_path = f"C:\\Users\\vntmypr\\Documents\\myllena\\TCC2\\Git\\CP-360-Weakly-Supervised-Saliency\\output\\static_resnet50\\{self.nome_folder_cube}\\" + '{0:06}.jpg'.format(id_frame+2)
            self.image_path = f"C:\\Users\\vntmypr\\Documents\\myllena\\TCC2\\Git\\360RAT\\videosAnotated\\videos\\{self.nome_video}\\{id_frame}.jpg"
            print("PATH:",self.image_path)
            self.img = cv2.imread(self.image_path)
            self.img = cv2.resize(self.img, (1080, 540), interpolation = cv2.INTER_AREA)
            
            # To draw in a black mask change the self.img to the follow line:
            #self.img = np.zeros((self.img .shape[0]+2, self.img .shape[1]+2), np.uint8)
            self.color =[self.BLACK, self.RED, self.OLIVE, self.ORANGE, self.INDIGO, self.CYAN,  self.MANGETA, self.BLUE, self.GREEN]

            files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
            for file in files:
                if file.endswith(".csv"):
                    #read a row in csv and draw the ROI in the image: self.img
                    self.read_csv((data_folder + "\\"+ file), self.color[0], id_frame)
                    self.color.pop(0)


            output_path = data_folder + f"\\img_{id_frame}_amizade.jpg"
            print("Output: ",output_path)

            cv2.imwrite(output_path, self.img)


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
        self.OLIVE = (128, 128, 0)
        self.CYAN = (0, 255, 255)
        self.INDIGO = (75, 0, 130)


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


    def read_csv(self, file, label, id):
        with open(file, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader)
            self.data = list(reader)

            for row in self.data:
                type_roi = int(row[0])
                id_frame = int(row[1])
                id_roi = int(row[2])
                center_point = np.array([float(row[3]), float(row[4])])
                fov = np.array([float(row[5]), float(row[6])])

                if( id_frame == id and type_roi !=2):
                    self.draw_fov( fov, center_point, label)
                

                
    def draw_fov(self, fov, center_point, label):
        self.nfov(self.img, 1080, 540)
        self.nfov.set_fov(fov[1], fov[0])
        self.nfov.updateNFOV(center_point)
        self.nfov.draw_NFOV_edges(self.img, label_color= label)


if __name__ == "__main__":
    main()