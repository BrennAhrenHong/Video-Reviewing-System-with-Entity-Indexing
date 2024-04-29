from typing import Optional

import MainWindow

def load_extra_ui(self):
    self.pushButton_videoPreview_next.setEnabled(False)
    self.pushButton_videoPreview_prev.setEnabled(False)

    self.label_status.setText("Idle")
    #self.progressBar_status.show()


    self.pushButton_personCropPreview_auto.setCheckable(True)
    self.tabWidget_content.setTabEnabled(1, False)
    #self.pushButton_personCropPreview_auto.setAutoRepeat(True)
    #self.pushButton_personCropPreview_auto.setAutoRepeatInterval(2)
    #self.pushButton_personCropPreview_auto.setAutoRepeatDelay(2)

    #self.tab_details.setEnabled(False)