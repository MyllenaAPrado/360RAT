#!/usr/bin/env python3
import os.path as osp
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Rendering:
    def __init__(self, path: str):
        """
        params:
            path: path of video folder or image folder
        """ 
        self.path = osp.join(osp.dirname(osp.abspath(path)), osp.basename(path))
        
    def image_rendering(self, size):
        # Open Image       
        src_img = cv2.imread(osp.join(osp.dirname(osp.abspath(self.path)), osp.basename(self.path)))
        #resize the image
        out_img = cv2.resize(src_img, size, interpolation=cv2.INTER_CUBIC)

        return out_img

    def save_image(self, img):
        cv2.imwrite(self.out_path,img) 