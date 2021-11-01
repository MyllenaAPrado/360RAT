class Image_Anotation:
    def __init__(self, id, image, path_image):
        self.id = id
        self.FOV = [0.30,0.60]
        self.image = image
        self.list_roi=[]
        self.list_compose_ROI=[]
        self.id_roi=0
        self.path_image = path_image
    
    def set_image(self, image):
        self.image = image

    def get_image(self):
        return self.image

    def get_id(self):
        return self.id

    def get_path(self):
        return self.path_image

    def get_list_roi(self):
        return self.list_roi
    
    def add_ROI(self, roi):
        self.id_roi += 1
        roi.set_id(self.id_roi)
        self.list_roi.append(roi)

        #return roi to get the id
        return roi
        
    def delet_ROI(self, id):        
        for element in self.list_roi:
            if element.get_id() == id:
                self.list_roi.remove(element)
                self.id_roi -= 1
                break

        for element in self.list_roi:
            if element.get_id() > id:
                new_id = element.get_id()  - 1
                element.set_id(new_id)
    
    def edit_roi(self, roi):
        self.list_roi[(roi.get_id()-1)] = roi

    def delet_list_roi(self):
        self.list_roi.clear()
        
    def add_compose_ROI(self, compose_ROI):
        self.list_compose_ROI.append(compose_ROI)

    def get_list_compose_ROI(self):
        return self.list_compose_ROI
    
    def get_compose_ROI(self, id):
        for roi in self.list_compose_ROI:
            if roi.get_id() == id:
                return roi
        return None
    
    def delete_compose_ROI(self, id):
        for element in self.list_compose_ROI:
            if element.get_id() == id:
                self.list_compose_ROI.remove(element)
                break

        for element in self.list_compose_ROI:
            if element.get_id() > id:
                new_id = element.get_id()  - 1
                element.set_id(new_id)
    

    def modify_compose_ROI(self, id, compose_ROI):
        self.list_compose_ROI[id]= compose_ROI


        

        

