from Interfaces.Anottation_window import Ui_Anottation

class SingleROI():
    def __init__(self, ui):
        ui.button_save_ROI.setEnabled(False)
        ui.button_delete_ROI.setEnabled(False)
        ui.button_edit_ROI.setEnabled(False)
        ui.button_cancel_edit.setEnabled(False)
        ui.button_save_edit.setEnabled(False)
        self.id_select = 0
        self.flag_edit_roi = False
    
    def set_flag_edit_roi(self, flag):
        self.flag_edit_roi = flag

    def get_flag_edit_roi(self):
        return self.flag_edit_roi

    def select_ROI(self, id, ui):
        self.id_select = id
        ui.button_edit_ROI.setEnabled(True)
        ui.button_delete_ROI.setEnabled(True)

    def delet_ROI(self, ui, list_frame, id_image):
        list_frame[id_image].delet_ROI(self.id_select)
        ui.button_edit_ROI.setEnabled(False)
        ui.button_delete_ROI.setEnabled(False)

    def edit_ROI(self, ui, roi):
        self.flag_edit_roi = True
        ui.button_delete_ROI.setEnabled(False)

        ui.slider_pos_x.blockSignals(True)
        ui.slider_pos_y.blockSignals(True)
        ui.slider_fov_h.blockSignals(True)
        ui.slider_fov_w.blockSignals(True)

        #adjuste values of sliders
        ui.slider_fov_h.setValue(int(roi.get_fov()[1] * 100))
        ui.slider_fov_w.setValue(int(roi.get_fov()[0] * 100))
        ui.slider_pos_x.setValue(int(roi.get_center_point()[0] * ui.equi_image.width()))
        ui.slider_pos_y.setValue(int(roi.get_center_point()[1] * ui.equi_image.height()))

        ui.slider_pos_x.blockSignals(False)
        ui.slider_pos_y.blockSignals(False)
        ui.slider_fov_h.blockSignals(False)
        ui.slider_fov_w.blockSignals(False)

        ui.button_save_ROI.setEnabled(False)
        ui.button_upload_image.setEnabled(False)
        ui.button_upload_folder.setEnabled(False)
        ui.button_save_ROI.setEnabled(False)
        ui.button_save.setEnabled(False)

        ui.button_save_edit.setEnabled(True)
        ui.button_cancel_edit.setEnabled(True)

    def finish_edit_ROI(self, ui):

        self.flag_edit_roi = False
        ui.button_edit_ROI.setEnabled(False)

        ui.button_save_ROI.setEnabled(True)
        ui.button_upload_image.setEnabled(True)
        ui.button_upload_folder.setEnabled(True)
        ui.button_save_ROI.setEnabled(True)
        ui.button_save.setEnabled(True)

        ui.button_save_edit.setEnabled(False)
        ui.button_cancel_edit.setEnabled(False)



    

