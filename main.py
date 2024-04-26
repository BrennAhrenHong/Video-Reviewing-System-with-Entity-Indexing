import os
import sqlite3
import sys

import cv2
import shutil

from typing import Optional

from PySide6.QtCore import QStringListModel, QItemSelection
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlTableModel

from ImageProcessing import Person
from VideoFrameLogic import VideoFrame
from VideoIndexing import VideoDetails
from pymediainfo import MediaInfo

from MainWindow import Ui_MainWindow
from PySide6 import QtCore, QtGui, QtWidgets

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QListView,
                               QMainWindow, QMenuBar, QProgressBar, QPushButton,
                               QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
                               QTabWidget, QToolBar, QVBoxLayout, QWidget, QHeaderView, QTableView, QAbstractItemView)

class SummaryLogic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #init
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables
        self.input_folder_path = r"./input/"
        self.output_folder_path = r"./output/"
        self.temp_folder_path = r"./temp/"

        self.input_video_list = []
        self.processed_video_list = []
        self.videodetails_list = []
        self.current_selected_video = None
        self.current_selected_videodetail = None
        self._preview_frame_image_list = None
        self._preview_frame_image_counter = None

        self.currentSelectedPerson = None

        # Setup
        # We're going to add an if condition where if the video is "processed" the details should not be unavailable
        #QTabWidget.setTabEnabled(self.ui.tabWidget_content, 1, False) # Disable "Details" tab

        # Create input/output folder if it doesn't exist
        self.housekeeping()

        # Create a preset selection list
        #self.ui.comboBox_presetSelection_box.addItem()

        # Startup
        # Video Selection
        self.create_videodetails()
        self.load_combobox_videoSelection()

        # Summary
        self.ui.comboBox_videoSelection_box.setCurrentIndex(-1)
        selected_videofile_path = os.path.join(self.input_folder_path, self.ui.comboBox_videoSelection_box.currentText())

        # Event Handlers
        self.ui.pushButton_summary_process.pressed.connect(lambda: self.process())
        self.ui.pushButton_videoPreview_next.pressed.connect(self.video_preview_next)
        self.ui.pushButton_videoPreview_prev.pressed.connect(self.video_preview_prev)
        self.ui.comboBox_videoSelection_box.currentIndexChanged.connect(self._on_combobox_video_selection_changed)
        self.ui.comboBox.currentIndexChanged.connect(self.test())

        self.show()
    # Functionalities
    def on_startup(self):
        pass

    def create_videodetails(self):
        def get_processed_videos():
            try:
                conn = sqlite3.connect("main.db")

                cursor = conn.cursor()
                cursor.execute("SELECT * FROM VideoDetails")
                all_entries = cursor.fetchall()
                conn.close()

                VideoDetails_list = []
                for detail in all_entries:
                    video_title, is_processed = detail
                    VideoDetails_list.append(VideoDetails(video_title=video_title,is_processed=is_processed))

                    return VideoDetails_list

            except sqlite3.Error as e:
                print(f"Error connecting to database:{e}")

            except Exception as e:
                print(f"An error occurred: {e}")

        unprocessed_video_list = []
        for video in os.listdir(self.input_folder_path):
            try:
                if video.endswith(".mp4"):
                    unprocessed_video_list.append(str(video))
                    self.input_video_list.append(str(video))
            except Exception as e:
                print(f"Error adding video: {e}")

        processed_video_list = get_processed_videos()

        # remove processed videos from unprocessed list
        for video in unprocessed_video_list:
            for processed_video in processed_video_list:
                if video == processed_video.video_title:
                    unprocessed_video_list.remove(video)

        videodetails_list = []
        for video in unprocessed_video_list:
            new_videodetails = VideoDetails(video_title=video)
            videodetails_list.append(new_videodetails)

        videodetails_list.extend(processed_video_list)

        self.videodetails_list = videodetails_list

    def housekeeping(self):
        if not os.path.exists(self.input_folder_path):
            os.mkdir( self.input_folder_path)
        if not os.path.exists( self.output_folder_path):
            os.mkdir( self.output_folder_path)
        if not os.path.exists( self.temp_folder_path):
            os.mkdir( self.temp_folder_path)
        else:
            try:
                shutil.rmtree(self.temp_folder_path, ignore_errors=True)
                print("cleared temp folder")
            except OSError as e:
                print(f"Error deleting: {e}")

    # Load combobox
    def load_combobox_videoSelection(self):

        # video_db_list = get_videodetails_sql()
        # processed_video_list = check_for_processed_videos(video_db_list)

        for video in self.videodetails_list:
            try:
                self.ui.comboBox_videoSelection_box.addItem(str(video.video_title))
            except Exception as e:
                print(f"Error adding video: {e}")

    def load_combobox_presets(self):
        pass

    def nothing(self):
        pass

    def process(self):
        # begin YOLO so insert startyolo here
        self.ui.tabWidget_content.setTabEnabled(1,True)
        self.load_detected_persons_combobox()
        self.ui.pushButton_summary_process.setDisabled(True)

    def load_detected_persons_combobox(self):
        def load_persons():
            try:
                video_title = self.current_selected_videodetail
                conn = sqlite3.connect('main.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM Person WHERE video_title = '{video_title.video_title}';")
                all_entries = cursor.fetchall()
                conn.close()

                person_list = []
                for detail in all_entries:
                    person_id, has_montage, video_title = detail
                    person_list.append(person_id)

                return person_list

            except sqlite3.Error as e:
                print(f"Error connecting to database:{e}")

            except Exception as e:
                print(f"An error occurred: {e}")

        person_list = load_persons()

        for person in person_list:
            self.ui.comboBox.addItem(str(person))
        pass



    def get_indexed_people(self):
        project_output_path = r".\output\Indexed\Thesis_FullOfficeCut_T300_5mins"
        pass

    def _on_combobox_detected_person_changed(self):
        self.currentSelectedPerson = self.ui.comboBox.currentText()
        pass

    def _on_combobox_video_selection_changed(self):
        self.ui.pushButton_videoPreview_prev.setEnabled(False)
        self.ui.pushButton_videoPreview_next.setEnabled(False)
        self.ui.progressBar_status.show()
        self.ui.label_status.show()
        self.ui.progressBar_status.setValue(0)
        track_list = self.get_summary_details()
        preview_frames = self.get_video_preview_frames(int(track_list[4]))
        new_video_frame = VideoFrame()
        self.clear_temp_folder()
        # Extract frames
        self.ui.progressBar_status.setValue(50)
        new_video_frame.extract_and_save_frames(self.ui.progressBar_status, self.selected_video_filepath, self.temp_folder_path, preview_frames)
        self.set_preview_frame_images_list()
        #self.set_preview_frame_image()

        self.ui.pushButton_videoPreview_prev.setEnabled(True)
        self.ui.pushButton_videoPreview_next.setEnabled(True)

        self.ui.label_videoPreview_image.setPixmap(self._preview_frame_image_list[0])
        self._preview_frame_image_counter = 0

        self.ui.label_summary_format_content.setText(track_list[0])
        self.ui.label_summary_resolution_content.setText(track_list[1])
        self.ui.label_summary_duration_content.setText(track_list[2])
        self.ui.label_summary_framerate_content.setText(track_list[3])
        self.ui.label_summary_frames_content.setText(track_list[4])
        self.ui.label_summary_processed_content.setText(track_list[5])
        self.ui.label_status.hide()
        self.ui.progressBar_status.hide()


    def set_preview_frame_images_list(self):
        preview_image_path_list = []
        for file in os.listdir(self.temp_folder_path):
            if file.endswith(".png"):
                image_path = os.path.join(self.temp_folder_path, file)
                pixmap = QPixmap(image_path)
                preview_image_path_list.append(pixmap)

        for img in preview_image_path_list:
            print(img)

        self._preview_frame_image_list = preview_image_path_list

    def get_video_preview_frames(self, frames):
        frame_list = []
        if frames == None:
            return frame_list

        if frames < 10:
            frame_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            i = 10
            while i <= 100:
                multiplier = i / 100
                frame_number = round(frames * multiplier)
                if(frame_number >= frames):
                    frame_number = frames - 1
                frame_list.append(frame_number)
                i += 10

        return frame_list

    # Get summary details
    def get_summary_details(self):
        self.current_selected_video = self.ui.comboBox_videoSelection_box.currentText()
        self.selected_video_filepath = os.path.join(self.input_folder_path, self.ui.comboBox_videoSelection_box.currentText())
        media_info = MediaInfo.parse(self.selected_video_filepath)
        track_info_list = []

        video_info = None

        # Get the video track by cycling through the video file data
        for track in media_info.tracks:
            if track.track_type == "Video":
                video_info = track
                break

        # Get the resolution
        resolution = f"{str(video_info.width)}x{str(video_info.height)}"

        # Get the duration
        # Calculate total seconds (including decimals for microseconds)
        total_seconds = video_info.duration / 1000

        # Extract hours, minutes, seconds, and microseconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        # Format the time string with zero-padding for hours, minutes, and seconds
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # get frames
        frames = self.get_frames(self.selected_video_filepath)

        # check if video is processed
        filename = os.path.basename(self.selected_video_filepath)
        video_title, extension = filename.split('.')
        #is_processed = check_video_if_processed(str(video_title))

        get_video = None
        for video in self.videodetails_list:
            if video.video_title == self.current_selected_video:
                get_video = video
                self.current_selected_videodetail = video

        is_processed = get_video.is_processed
        if (is_processed):
            processed = "Yes"
            self.ui.tabWidget_content.setTabEnabled(1,True)
            self.ui.pushButton_summary_process.setDisabled(True)
            self.load_detected_persons_combobox()
        else:
            processed = "No"
            self.ui.tabWidget_content.setTabEnabled(1,False)
            self.ui.pushButton_summary_process.setEnabled(True)

        track_info_list.append(str(video_info.format))
        track_info_list.append(str(resolution))
        track_info_list.append(str(time_string))
        track_info_list.append(str(video_info.frame_rate))
        track_info_list.append(str(frames))
        track_info_list.append(str(processed))

        return track_info_list

    def get_frames(self, video_file):
        try:
            # Create a video capture object
            cap = cv2.VideoCapture(video_file)

            # Check if video capture is successful
            if not cap.isOpened():
                print("Error opening video file.")
                return None

            # Get the total number of frames
            num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            # Release the capture object
            cap.release()

            return int(num_frames)

        except Exception as e:
            print(f"Error extracting number of frames using OpenCV: {e}")
            return None

 # Controls for preview image
    def video_preview_next(self):
        i = self._preview_frame_image_counter
        if i + 1 >= len(self._preview_frame_image_list):
            image = self._preview_frame_image_list[0]
            self._preview_frame_image_counter = 0
            self.ui.label_videoPreview_image.setPixmap(image)
        else:
            i += 1
            self._preview_frame_image_counter = i
            image = self._preview_frame_image_list[i]
            self.ui.label_videoPreview_image.setPixmap(image)

    def video_preview_prev(self):
        i = self._preview_frame_image_counter
        if i - 1 <= -1:
            i = len(self._preview_frame_image_list) - 1
            image = self._preview_frame_image_list[i]
            self._preview_frame_image_counter = i
            self.ui.label_videoPreview_image.setPixmap(image)
        else:
            i -= 1
            self._preview_frame_image_counter = i
            image = self._preview_frame_image_list[i]
            self.ui.label_videoPreview_image.setPixmap(image)


    def test(self):
        print("Hello World")

    def clear_temp_folder(self):
        try:
            if not os.path.exists(self.temp_folder_path):
                os.mkdir(self.temp_folder_path)
                pass
            for file in os.listdir(self.temp_folder_path):
                file_path = os.path.join(self.temp_folder_path, file)
                os.remove(file_path)
            print("cleared temp folder")
        except OSError as e:
            print(f"Error deleting: {e}")

    def run_diagnostics(self):
        print("video_selection_combobox_count:", self.ui.comboBox_videoSelection_box.count())
        print("video_presetSelection_combobox_count:", self.ui.comboBox_presetSelection_box.count())


class TableViewPerson:
    def __init__(self, id, crops):
        self.id = id
        self.crops = crops

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Security System")
    main_window = SummaryLogic()

    app.exec()
    app.activeWindow()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
