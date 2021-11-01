class ROI:
    def __init__(self, center_point, fov, label):
        self.center_point = center_point
        self.fov = fov
        self.label = label

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_center_point(self):
        return self.center_point

    def set_center_point(self, center_point):
        self.center_point = center_point

    def get_fov(self):
        return self.fov

    def set_fov(self, fov):
        self.fov = fov

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label
    
    def set_movement(self, movement):
        self.movement = movement
    
    def get_movement (self):
        return self.movement