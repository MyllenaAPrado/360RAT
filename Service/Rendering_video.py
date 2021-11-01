from Entities.ImageAnotation import Image_Anotation
from PyQt5 import QtWidgets
from sys import platform
import cv2
import os
import os.path as osp
import shutil


class Rendering_Video:
    def __init__(self, path: str):
        self.path = r"{}".format(path[0])
        cwd = os.getcwd()
        head, tail = os.path.split(self.path )
        videos = "videos"
        
        if platform == "linux" or platform == "linux2":
            # linux
            path = osp.join(cwd, "videosAnotated/{}".format(videos))
            self.path_original = path + "/{}".format(tail)

        elif platform == "win32":
        # Windows...
            path = osp.join(cwd, "videosAnotated\{}".format(videos))
            self.path_original = path + "\{}".format(tail)
            
        if os.path.exists(self.path_original):
            try:
                shutil.rmtree(self.path_original)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
            
        #os.makedirs(path)
        os.makedirs(self.path_original)
        self.list_frames = []
        self.list_frames_copy = []
        

    def get_list_video(self):
        index = 0
        self.list_frames.clear()
        self.list_frames_copy.clear()

        cap = cv2.VideoCapture(self.path)
        #cv2.namedWindow('video')
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.list_frames.append(Image_Anotation(index, frame, self.path))
            #self.list_frames_copy.append(Image_Anotation(index, frame.copy(), self.path))

            frame_out_path_original = osp.join(self.path_original, '{}.jpg'.format(index))
            #save image in directory
            cv2.imwrite(frame_out_path_original, frame)
            index+=1
            
        cap.release()
        
        return self.list_frames, self.path_original