from typing import Optional

import MainWindow

def load_extra_ui(self):
    self.pushButton_videoPreview_next.setEnabled(False)
    self.pushButton_videoPreview_prev.setEnabled(False)

    self.label_status.setText("Idle")
    #self.progressBar_status.hide()

    self.tabWidget_content.setTabEnabled(1, False)