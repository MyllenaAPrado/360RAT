class Compose_ROI:
    def __init__(self, id, center_point, fov, frame, label,movement):
        self.id = id
        self.center_point_init = center_point
        self.fov_init = fov
        self.frame_init = frame
        self.label = label
        self.movement = movement

    def set_end_ROI(self, center_point, fov, frame):
        self.center_point_end = center_point
        self.fov_end = fov
        self.frame_end = frame
        self.number_of_ROI= self.frame_end - self.frame_init +1

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_frame_init(self):
        return self.frame_init
    
    def get_frame_end(self):
        return self.frame_end

    def set_frame_end(self, frame_id):
        self.frame_end = frame_id

    def get_center_point_init(self):
        return self.center_point_init

    def set_center_point_init(self, center_point):
        self.center_point_init = center_point
    
    def get_center_point_end(self):
        return self.center_point_end

    def set_center_point_end(self, center_point):
        self.center_point_end = center_point

    def get_fov_init(self):
        return self.fov_init

    def set_fov_init(self, fov):
        self.fov_init = fov

    def get_fov_end(self):
        return self.fov_end

    def set_fov_end(self, fov):
        self.fov_end = fov

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label
    
    def set_movement(self, movement):
        self.movement = movement
    
    def get_movement(self):
        return self.movement

    def calcule_pos_ROI_variation(self):
        self.delta_x = (self.center_point_end[0] - self.center_point_init[0]) / (self.number_of_ROI - 1)
        self.delta_y = (self.center_point_end[1] - self.center_point_init[1]) / (self.number_of_ROI - 1) 
        self.delta_fov_h = (self.fov_end[0] - self.fov_init[0]) / (self.number_of_ROI - 1)
        self.delta_fov_w = (self.fov_end[1] - self.fov_init[1]) / (self.number_of_ROI - 1)
    
    def get_delta_x(self):
        return self.delta_x
    
    def get_delta_y(self):
        return self.delta_y
    
    def get_delta_fov_w(self):
        return self.delta_fov_w
    
    def get_delta_fov_h(self):
        return self.delta_fov_h
    
    def get_number_of_ROI(self):
        return self.number_of_ROI


