#!/usr/bin/env python3
#Reference: http://blog.nitishmutha.com/equirectangular/360degree/2017/06/12/How-to-project-Equirectangular-image-to-rectilinear-view.html
#Reference - code structure: https://stackoverflow.com/questions/65306884/avoid-recursion-error-with-cv2-and-mouse-callback
import cv2
import numpy as np
from math import pi

class NFOV:


    def __init__(self, nfov_screen_height=400, nfov_screen_width=400,save_grid_coords=False):
        self.FOV = [0.11, 0.22]
        self.PI = pi
        self.PI_2 = pi * 0.5
        self.PI2 = pi * 2.0
        self.nfov_screen_height = nfov_screen_height
        self.nfov_screen_width = nfov_screen_width
        self.screen_points = self._get_screen_img()
        self.save_grid_coords = save_grid_coords
        self.nfov_id = 1

    def __call__(self, equi_img):      
        #Image properties
        self.equi_img = equi_img
        self.equi_height = self.equi_img.shape[0]
        self.equi_width = self.equi_img.shape[1]
        self.equi_channel = self.equi_img.shape[2]

            
    def updateNFOV(self, center_point, label_color= [0,0,255]):
        #mudança
        self.center_point = center_point
        self.equi_img_copy = self.equi_img.copy()
        
        # Compute all NFOV grid coordinates in radians
        self.cp = self._get_cp_rad() 
        convertedScreenCoord = self._get_coord_rad()
        sphericalCoord = self._calcSphericaltoGnomonic(convertedScreenCoord)
        self.sc_grid = sphericalCoord.reshape(self.nfov_screen_height, self.nfov_screen_width, 2).astype(np.float32)
        
        #Remap accordingly to the computed grid
        self.img_NFOV = cv2.remap(self.equi_img, \
                        self.sc_grid[..., 0]*self.equi_width, \
                        self.sc_grid[..., 1]*self.equi_height, \
                        interpolation=cv2.INTER_LINEAR, \
                        borderMode=cv2.BORDER_WRAP)
        
               
        self.draw_NFOV_edges(self.equi_img_copy, label_color)

        if (self.save_grid_coords):
           self.save_array(self.sc_grid)

        '''Plotar mascara branca no ROI
        aux_W = np.array(self.sc_grid[..., 0]*self.equi_width )
        W= np.reshape(aux_W, 400*400)
        aux_H = np.array(self.sc_grid[..., 1]*self.equi_height)
        H= np.reshape(aux_H, 400*400)
        point = np.array([H, W], np.int32)

        for idx in range (0, 160000):
            if(point[1][idx] >= self.equi_width):
                point[1][idx] = point[1][idx] - self.equi_width
            if(point[0][idx] >= self.equi_height):
                point[0][idx] = point[0][idx] - self.equi_height
            self.equi_img_copy[point[0][idx], point[1][idx]] = (255, 255, 255)
        '''

        return self.img_NFOV, self.equi_img_copy

    def save_array(self,array):
        np.save("../results/sph_fov_line.npy",array)                        

    def _get_screen_img(self):
        xx, yy = np.meshgrid(np.linspace(0, 1, self.nfov_screen_width), np.linspace(0, 1, self.nfov_screen_height))
        return np.array([xx.ravel(), yy.ravel()]).T
    
    # Compute pixel grid coordinates from screen and from center in rad
    def _get_cp_rad(self):
        return (self.center_point * 2 - 1) * np.array([self.PI, self.PI_2]) 
        
    def _get_coord_rad(self):
        #print(np.ones(self.screen_points.shape) * self.FOV)
        #print((self.screen_points * 2 - 1) * np.array([self.PI, self.PI_2]) * (np.ones(self.screen_points.shape) * self.FOV))
        return (self.screen_points * 2 - 1) * np.array([self.PI, self.PI_2]) * (np.ones(self.screen_points.shape) * self.FOV)  

    def _calcSphericaltoGnomonic(self, convertedScreenCoord):
        x = convertedScreenCoord.T[0]
        y = convertedScreenCoord.T[1]

        rou = np.sqrt(x ** 2 + y ** 2)
        c = np.arctan(rou)
        sin_c = np.sin(c)
        cos_c = np.cos(c)

        phi = np.arcsin(cos_c * np.sin(self.cp[1]) + (y * sin_c * np.cos(self.cp[1])) / rou)
        theta = self.cp[0] + np.arctan2(x * sin_c, rou * np.cos(self.cp[1]) * cos_c - y * np.sin(self.cp[1]) * sin_c)
        '''print(np.max(phi))
        print(phi[0], phi[159599])
        print(np.max(theta))
        print(theta[0], theta[399])
        print("Shape:", phi.shape)'''

        phi = (phi / self.PI_2 + 1.) * 0.5
        theta = (theta / self.PI + 1.) * 0.5

        return np.array([theta, phi]).T
    
    def set_fov(self, value_h, value_w):
         self.FOV = [value_w, value_h]

    #NFOV Rendering
    def draw_NFOV_edges(self, image, label_color= [0,0,255]):
        '''
        Get edges in clockwise order 
        Reference: https://stackoverflow.com/questions/41200719/how-to-get-all-array-edges
        Requisito: extrair os elementos de fronteira do grid em formato np.int32(N,2)
        '''
        THICKNESS = 2 
        ISCLOSED = False
        self.equi_height = image.shape[0]
        self.equi_width = image.shape[1]
        #Get edges from grid in clock-wise order and with border pixels repetition
        sph_coord_row1 = self.sc_grid[0,::-1][:]
        sph_coord_row2 = self.sc_grid[-1,::-1][:]
        sph_coord_col1 = self.sc_grid[::-1,0][:]
        sph_coord_col2 = self.sc_grid[::-1,-1][:]

        sph_coord_row1 = np.array([sph_coord_row1[:,0]*self.equi_width,
                    sph_coord_row1[:,1]*self.equi_height]).astype(np.int32)
        
        sph_coord_row2 = np.array([sph_coord_row2[:,0]*self.equi_width,
                    sph_coord_row2[:,1]*self.equi_height]).astype(np.int32)

        sph_coord_col1 = np.array([sph_coord_col1[:,0]*self.equi_width,
                    sph_coord_col1[:,1]*self.equi_height]).astype(np.int32)

        sph_coord_col2 = np.array([sph_coord_col2[:,0]*self.equi_width,
                    sph_coord_col2[:,1]*self.equi_height]).astype(np.int32)

        #check the fov
        sph_coord_row1_r = []
        sph_coord_row1_l = []
        sph_coord_row1_n = []
        sph_coord_row2_r = []
        sph_coord_row2_l = []
        sph_coord_row2_n = []
        sph_coord_col1_r = []
        sph_coord_col1_l = []
        sph_coord_col1_n = []
        sph_coord_col2_r = []
        sph_coord_col2_l = []
        sph_coord_col2_n = []



        for aux in sph_coord_row1.T:
            if(aux[0]> self.equi_width ):
                sph_coord_row1_r.append([aux[0] - self.equi_width , aux [1]])
            elif (aux[0]< 0):
                sph_coord_row1_l.append([aux[0] + self.equi_width , aux [1]])
            else :
                sph_coord_row1_n.append([aux[0] , aux [1]])
                
        for aux in sph_coord_row2.T:
            if(aux[0]> self.equi_width ):
                sph_coord_row2_r.append([aux[0] - self.equi_width , aux [1]])
            elif (aux[0]< 0):
                sph_coord_row2_l.append([aux[0] + self.equi_width , aux [1]])
            else:
                sph_coord_row2_n.append([aux[0] , aux [1]])

        for aux in sph_coord_col1.T:
            if(aux[0]> self.equi_width ):
                sph_coord_col1_r.append([aux[0] - self.equi_width , aux [1]])
            elif (aux[0]< 0):
                sph_coord_col1_l.append([aux[0] + self.equi_width , aux [1]])
            else :
                sph_coord_col1_n.append([aux[0] , aux [1]])

        for aux in sph_coord_col2.T:
            if(aux[0]> self.equi_width ):
                sph_coord_col2_r.append([aux[0] - self.equi_width , aux [1]])
            elif (aux[0]< 0):
                sph_coord_col2_l.append([aux[0] + self.equi_width , aux [1]])
            else :
                sph_coord_col2_n.append([aux[0] , aux [1]])


        if sph_coord_row1_r:
            cv2.polylines(image,[np.array(sph_coord_row1_r)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_row1_l:
            cv2.polylines(image,[np.array(sph_coord_row1_l)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_row1_n:
            cv2.polylines(image,[np.array(sph_coord_row1_n)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        
        if sph_coord_row2_r:
            cv2.polylines(image,[np.array(sph_coord_row2_r)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_row2_l:
            cv2.polylines(image,[np.array(sph_coord_row2_l)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_row2_n:
            cv2.polylines(image,[np.array(sph_coord_row2_n)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)

        if sph_coord_col1_r:
            cv2.polylines(image,[np.array(sph_coord_col1_r)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_col1_l:
            cv2.polylines(image,[np.array(sph_coord_col1_l)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_col1_n:
            cv2.polylines(image,[np.array(sph_coord_col1_n)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)

        if sph_coord_col2_r:
            cv2.polylines(image,[np.array(sph_coord_col2_r)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_col2_l:
            cv2.polylines(image,[np.array(sph_coord_col2_l)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)
        if sph_coord_col2_n:
            cv2.polylines(image,[np.array(sph_coord_col2_n)],isClosed=ISCLOSED,color=label_color,thickness=THICKNESS)

