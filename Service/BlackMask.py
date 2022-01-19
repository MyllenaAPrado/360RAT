from Service.SphereFovBlackMask import NFOV
from PyQt5 import QtWidgets
import csv
import numpy as np
import cv2
import os
from pathlib import Path
from os import listdir
from os.path import isfile, join
from PIL import Image

class BlackMask():

    def __init__(self):
        self.WHITE = [255,255,255]
        self.nfov = NFOV()
    
    def draw_black_mask(self, path, list_roi, list_compose_roi):

        self.img = np.zeros((540+2, 1080+2), np.uint8)
        WHITE = (255,255,255)
        
        for roi in list_roi:
            self.draw_fov(roi.get_fov(), roi.get_center_point(), self.WHITE)
        
        for roi in list_compose_roi:
            self.draw_fov(roi.get_fov(), roi.get_center_point(), self.WHITE)

        im_pil = Image.fromarray(self.img)
        im_pil.save(path)                   

                
    def draw_fov(self, fov, center_point, label):
        self.nfov(self.img, 1080, 540)
        self.nfov.set_fov(fov[1], fov[0])
        self.nfov.updateNFOV(center_point)
        self.nfov.draw_NFOV_edges(self.img, label_color= label)
