import asyncio
import os
import sqlite3
import sys
import time
from tkinter import filedialog

import cv2
import shutil

from typing import Optional, Sequence

import torch.cuda
from PySide6.QtCore import QStringListModel, QItemSelection, QThread
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlTableModel

import YoloTracking
import video_trimming
from ImageProcessing import Frame, Crop, Person
from VideoFrameLogic import VideoFrame
from VideoIndexing import VideoDetails
from SqliteScripts import SqliteScripts

#from AsyncioPySide6 import AsyncioPySide6

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
        # init
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables
        self.input_folder_path = r"./input/"
        self.output_folder_path = r"./output/"
        self.temp_folder_path = r"./temp/"
        self.inferred_folder = r"./output/inferred"

        # self.processed_video_list = []
        self._input_video_list = []
        self._videodetails_list: Optional[list[VideoDetails]] = []
        self._videodetails_persons_list = []
        self._selected_person_crop_list = []
        self._preview_frame_pixmap_list = []
        self._preview_crop_pixmap_list = []
        self._preset_combobox_list = []
        self.add_video_list = []

        self._last_button_clicked = None
        self._auto_button_state = False
        self.total_preview_frames = 0

        self._selected_person_crop_counter = None

        self._selected_video = None
        self._selected_videodetail : Optional[VideoDetails] = None
        self._selected_video_filepath = None

        self._preview_frame_image_list = None
        self._preview_frame_image_counter = None

        self._selected_person = None
        self._selected_build_folder_path = None


        #self.counter_thread = QThread.

        # Setup
        # We're going to add an if condition where if the video is "processed" the details should not be unavailable
        # QTabWidget.setTabEnabled(self.ui.tabWidget_content, 1, False) # Disable "Details" tab

        # Create input/output folder if it doesn't exist
        self.on_startup()

        # Create a preset selection list
        self.load_combobox_presets()

        # Startup
        # Video Selection
        self.create_videodetails()
        self.load_combobox_video_selection()

        # Summary
        self.ui.comboBox_videoSelection_box.setCurrentIndex(-1)
        #selected_videofile_path = os.path.join(self.input_folder_path,
                                              # self.ui.comboBox_videoSelection_box.currentText())

        # Event Handlers
        self.ui.pushButton_summary_process.pressed.connect(lambda: self.process())
        self.ui.pushButton_videoPreview_next.pressed.connect(self.video_preview_next)
        self.ui.pushButton_videoPreview_prev.pressed.connect(self.video_preview_prev)
        self.ui.comboBox_videoSelection_box.currentIndexChanged.connect(self._on_combobox_video_selection_changed)
        self.ui.comboBox_detectedPeople_list.currentIndexChanged.connect(self._on_combobox_detected_persons_changed)

        self.ui.pushButton_personCropPreview_auto.clicked.connect(self.auto_button)
        self.ui.pushButton_personCropPreview_next.pressed.connect(self.crop_preview_next)
        self.ui.pushButton_personCropPreview_prev.pressed.connect(self.crop_preview_prev)
        self.ui.pushButton_videoSelection_openFolder.pressed.connect(lambda: self.open_input_folder())
        self.ui.pushButton_videoSelection_add.clicked.connect(self.add_video)
        self.ui.pushButton_montagePanel_create.clicked.connect(self.create_montage)
        self.ui.pushButton_controlPanel_openVideoFolder.clicked.connect(lambda: self.open_video_folder())
        self.ui.pushButton_controlPanel_playVideo.clicked.connect(lambda: self.play_video_folder())

        self.show()

    def create_montage(self):
        def cut_and_join_video(video_path, start_frame, end_frame, output_filename, fps):
            # Open video capture object
            cap = cv2.VideoCapture(video_path)

            # Check if video opened successfully
            if not cap.isOpened():
                print("Error opening video!")
                return

            # Get frame width and height
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Define video codec (e.g., 'XVID') and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

            # Skip to the start frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            # Process video frames
            frame_count = start_frame
            while cap.isOpened() and frame_count <= end_frame:
                ret, frame = cap.read()

                if ret:
                    # Write frame to output video
                    out.write(frame)
                    frame_count += 1
                else:
                    break

            # Release resources
            cap.release()
            out.release()
            print(f"Video '{output_filename}' created successfully!")

        output_montage_path = os.path.join(self.output_folder_path, "montage", self.selected_videodetail.video_title, self.ui.comboBox_detectedPeople_list.currentText())
        person_build_folder_path = os.path.join(self.output_folder_path, "builds", self.selected_videodetail.video_title, self.ui.comboBox_detectedPeople_list.currentText())
        input_video = os.path.join(self.input_folder_path, self.selected_videodetail.video_title)

        crop_list = []
        for crop in os.listdir(person_build_folder_path):
            crop_list.append(crop)

        crop_ini, extension = crop_list[0].split(".")
        start_frame = int(crop_ini)
        end_frame = int(crop_ini)

        for crop in crop_list:
            frame_number, extension = crop.split(".")
            if start_frame > int(frame_number):
                start_frame = int(frame_number)

            if  end_frame < int(frame_number):
                end_frame = int(frame_number)

        if not os.path.exists("./output/montage"):
            os.mkdir("./output/montage")

        if not os.path.exists(f"./output/montage/{self.selected_videodetail.video_title}"):
            os.mkdir(f"./output/montage/{self.selected_videodetail.video_title}")

        if not os.path.exists(output_montage_path):
            os.mkdir(output_montage_path)

        self.ui.comboBox_detectedPeople_list.currentText()
        output_filename = os.path.join(output_montage_path, "montage.mp4")
        cut_and_join_video(video_path=input_video, start_frame=start_frame, end_frame=end_frame, output_filename=output_filename, fps=5)
        sql = SqliteScripts()
        sql.person_has_montage_true(video_title=self.selected_videodetail.video_title, person_id=self.ui.comboBox_detectedPeople_list.currentText())
        self.get_summary_details()

    def open_input_folder(self):
        os.startfile(os.path.join(os.getcwd(), "input"))

    def add_video(self):
        video_lists = filedialog.askopenfilenames(title="Select a Video File",
                                               filetypes=[("Video Files", "*.mp4 *.avi *.mov *.wmv")])
        if video_lists:
            print("Selected video(s):", video_lists)
            self.add_video_list.append(video_lists)
            for video in video_lists:
                destination = os.path.join(os.getcwd(), "input", os.path.basename(video))
                if not os.path.exists(destination):
                    shutil.copyfile(src=video, dst= destination)

            self.create_videodetails()
            self.load_combobox_video_selection()

    # Functionalities
    def load_combobox_presets(self):
        recommended = "Recommended (medium accuracy)"
        fast = "Fast (low accuracy)"
        high_quality = "Slow (high accuracy)"

        preset_tuple = (recommended, fast, high_quality)

        self.ui.comboBox_presetSelection_box.addItems(preset_tuple)
        pass

    def open_video_folder(self):
        video_title = self.selected_videodetail.video_title
        person_id = self.ui.comboBox_detectedPeople_list.currentText()
        montage_folder = f"./output/montage/{video_title}/{person_id}"
        person_folder = os.path.join(os.getcwd(), montage_folder)
        os.startfile(person_folder)

    def play_video_folder(self):
        video_title = self.selected_videodetail.video_title
        person_id = self.ui.comboBox_detectedPeople_list.currentText()
        montage_folder = f"./output/montage/{video_title}/{person_id}/montage.mp4"
        person_folder = os.path.join(os.getcwd(), montage_folder)
        os.startfile(person_folder)

    def process(self):
        def start_yolo():
            # begin YOLO
            video_source = os.path.join(self.input_folder_path, self.current_selected_video)
            model = ""
            output_path = os.path.join(self.output_folder_path, "inferred", self.selected_videodetail.video_title)
            imgsz = None
            iou = None
            conf = None
            device = None

            preset_value = self.ui.comboBox_presetSelection_box.currentText().split(" ")[0]

            match preset_value:
                case "Recommended":
                    model = "yolov8m.pt"
                    imgsz = 640
                    iou = 0.8
                    conf = 0.5
                    device = "CPU"
                case "Fast":
                    model = "yolov8s.pt"
                    imgsz = 640
                    iou = 0.8
                    conf = 0.5
                    device = "CPU"
                case "Slow":
                    model = "yolov8x.pt"
                    imgsz = 1280
                    iou = 0.8
                    conf = 0.5
                    device = "CPU"
                case _:
                    pass

            self.ui.pushButton_summary_process.setDisabled(True)

            if torch.cuda.is_available():
                device = 0

            YoloTracking.start_yolo(video_source=video_source, model=model, output_path=output_path,
                                    imgsz=imgsz, iou=iou, conf=conf, device=device, total_frames=self.total_preview_frames,
                                    ui=self.ui)

        #update_is_processed = SqliteScripts.videodetails_is_processed_true()

        video_inferred_folder = os.path.join(self.inferred_folder, self.selected_videodetail.video_title)

        if not os.path.exists(os.path.join(video_inferred_folder)):
            self.ui.progressBar_status.show()
            self.ui.label_status.show()
            self.ui.label_status.setText("processing...")
            start_yolo()

        if(os.path.exists(video_inferred_folder)):
            for video in self.videodetails_list:
                if video.video_title == self.ui.comboBox_videoSelection_box.currentText():
                    video.index_persons()
                    self.ui.progressBar_status.setValue(95)
                    video.build_indexed_persons()
                    self.ui.progressBar_status.setValue(100)

        self._on_combobox_video_selection_changed()
        self.ui.label_status.setText("idle...")
        if self.ui.tab_details.isEnabled():
            self.ui.tabWidget_content.setCurrentIndex(1)

    def housekeeping(self):
        self.ui.tabWidget_content.setTabEnabled(1, False)

    def after_process(self):
        self.ui.tabWidget_content.setTabEnabled(1, True)

    def auto_button(self):
        # def do_last_button():
        #     if self.last_button_clicked == "next":
        #         self.crop_preview_next()
        #     elif self.last_button_clicked == "prev":
        #         self.crop_preview_prev()
        #
        # do_last_button()
        if self.ui.pushButton_personCropPreview_auto.isChecked():
            self.ui.pushButton_personCropPreview_next.setAutoRepeat(True)
            self.ui.pushButton_personCropPreview_prev.setAutoRepeat(True)
            self.ui.pushButton_personCropPreview_next.setAutoRepeatInterval(2)
            self.ui.pushButton_personCropPreview_prev.setAutoRepeatInterval(2)
            self.ui.pushButton_personCropPreview_next.setAutoRepeatDelay(2)
            self.ui.pushButton_personCropPreview_prev.setAutoRepeatDelay(2)
        else:
            self.ui.pushButton_personCropPreview_next.setAutoRepeat(False)
            self.ui.pushButton_personCropPreview_prev.setAutoRepeat(False)

    def crop_preview_next(self):
        def next():
            if self.selected_person_crop_counter < len(self.selected_person_crop_list) - 1:
                self.selected_person_crop_counter += 1

            image_path = self.selected_person_crop_list[self.selected_person_crop_counter]

            pixmap_crop = QPixmap(image_path.crop_path)
            pixmap_frame = QPixmap(image_path.frame_image)

            self.ui.label_personCropPreviewImage.setPixmap(pixmap_crop)
            self.ui.label_framePreview_image.setPixmap(pixmap_frame)
            self.last_button_clicked = "next"
            self.ui.label_cropCounter.setText(f"{self.selected_person_crop_counter + 1}/{len(self._selected_person_crop_list)}")

        next()

    def crop_preview_prev(self):
        if self.selected_person_crop_counter > 0:
            self.selected_person_crop_counter -= 1

        image_path = self.selected_person_crop_list[self.selected_person_crop_counter]

        pixmap_crop = QPixmap(image_path.crop_path)
        pixmap_frame = QPixmap(image_path.frame_image)

        self.ui.label_personCropPreviewImage.setPixmap(pixmap_crop)
        self.ui.label_framePreview_image.setPixmap(pixmap_frame)

        self.last_button_clicked = "prev"

        self.ui.label_cropCounter.setText(f"{self.selected_person_crop_counter + 1}/{len(self._selected_person_crop_list)}")

    def create_videodetails(self):
        self.ui.comboBox_videoSelection_box.clear()

        unprocessed_video_list = []
        for video in os.listdir(self.input_folder_path):
            try:
                if video.endswith(".mp4"):
                    unprocessed_video_list.append(str(video))
                    self.input_video_list.append(str(video))
            except Exception as e:
                print(f"Error adding video: {e}")

       # for added_video in self.add_video_list:
        #    unprocessed_video_list.extend(added_video)

        sql = SqliteScripts()
        processed_video_list = sql.get_processed_videos()

        # remove processed videos from unprocessed list
        for video in processed_video_list:
            if video.video_title in unprocessed_video_list:
                unprocessed_video_list.remove(video.video_title)


        videodetails_list = []
        for video in unprocessed_video_list:
            new_videodetails = VideoDetails(video_title=video)
            videodetails_list.append(new_videodetails)

        videodetails_list.extend(processed_video_list)

        self.videodetails_list = videodetails_list

    def on_startup(self):
        if not os.path.exists(self.input_folder_path):
            os.mkdir(self.input_folder_path)
        if not os.path.exists(self.output_folder_path):
            os.mkdir(self.output_folder_path)
        if not os.path.exists(self.temp_folder_path):
            os.mkdir(self.temp_folder_path)
        else:
            try:
                shutil.rmtree(self.temp_folder_path, ignore_errors=True)
                print("cleared temp folder")
            except OSError as e:
                print(f"Error deleting: {e}")

        self.ui.pushButton_summary_process.setDisabled(True)

    # Load combobox
    def load_combobox_video_selection(self):
        self.ui.comboBox_videoSelection_box.clear()
        for video in self.videodetails_list:
            try:
                self.ui.comboBox_videoSelection_box.addItem(str(video.video_title))
            except Exception as e:
                print(f"Error adding video: {e}")

    def load_detected_persons_combobox(self):
        #self.ui.comboBox_detectedPeople_list.clear()
        sql = SqliteScripts()
        self.videodetails_persons_list = sql.load_person_from_video_sql(self.selected_videodetail.video_title)
        for person in self.videodetails_persons_list:
            self.ui.comboBox_detectedPeople_list.addItem(f"person_{str(person.person_id)}")

    def _on_combobox_detected_persons_changed(self):
        def extract_number_and_prefix(text):
            # Extract the numeric part (if any) and consider the presence of a number in sorting
            if text == "F":
                text = "F1"

            number = ""
            has_number = False
            for char in text:
                if char.isdigit():
                    number += char
                    has_number = True
            return (not has_number, int(number) if number else float("inf"))


        if not self.selected_videodetail.is_processed:
            return

        if self.ui.comboBox_detectedPeople_list.count() == 0:
            return

        prefix, person_id = self.ui.comboBox_detectedPeople_list.currentText().split("_")
        self.selected_person = person_id
        sql = SqliteScripts()
        get_person: Optional[list[Person]] = sql.get_person_from_id_sql(person_id=self.selected_person, video_title=self.selected_videodetail.video_title)
        get_crops_of_person: Optional[list[Crop]] = sql.get_person_crops_sql(self.selected_person, self.selected_videodetail.video_title)

        sorted_crop_list = []
        for crop in get_crops_of_person:
            sorted_crop_list.append(os.path.basename(os.path.dirname(crop.frame_image)))

        sorted_crop_list = sorted(sorted_crop_list, key=extract_number_and_prefix)

        selected_person_crop_list = []
        counter = 0
        while counter < len(sorted_crop_list):
            for crop in get_crops_of_person:
                if os.path.basename(os.path.dirname(crop.frame_image)).endswith(sorted_crop_list[counter]):
                    selected_person_crop_list.append(crop)
            counter += 1

        #pixmap_crop_list = []
        #pixmap_frame_list = []
        # for crop in selected_person_crop_list:
        #     pixmap_crop_list.append(QPixmap(crop.crop_path))
        #     pixmap_frame_list.append(QPixmap(crop.frame_image))


        #self.preview_frame_pixmap_list = pixmap_frame_list
        #self._preview_crop_pixmap_list = pixmap_crop_list

        self.selected_person_crop_list = selected_person_crop_list

        crop_count = len(get_crops_of_person)
        self.selected_person = self.ui.comboBox_detectedPeople_list.currentText()
        if get_person[0].has_montage == 0:
            self.ui.label_montage_value.setText("No")
        else:
            self.ui.label_montage_value.setText("Yes")

        self.ui.label_crops_value.setText(str(crop_count))
        # selected_person_build_folder_path = os.path.join(self.current_build_folder_path, self._selected_person)

        self.selected_person_crop_counter = 0

        image_path = get_crops_of_person[0]
        pixmap_crop = QPixmap(image_path.crop_path)
        pixmap_frame = QPixmap(image_path.frame_image)

        self.ui.label_cropCounter.setText(
            f"{self.selected_person_crop_counter + 1}/{len(self._selected_person_crop_list)}")

        self.ui.label_personCropPreviewImage.setPixmap(pixmap_crop)
        self.ui.label_framePreview_image.setPixmap(pixmap_frame)

    def _on_combobox_video_selection_changed(self):
        self.current_selected_video = self.ui.comboBox_videoSelection_box.currentText()
        for video in self.videodetails_list:
            if video.video_title == self.current_selected_video:
                self.selected_videodetail = video

        self.current_build_folder_path = os.path.join(self.output_folder_path, "/build", self.current_selected_video)


        self.ui.pushButton_videoPreview_prev.setEnabled(False)
        self.ui.pushButton_videoPreview_next.setEnabled(False)
        # self.ui.progressBar_status.show()
        self.ui.label_status.show()
        self.ui.label_status.setText("processing")
        self.ui.progressBar_status.setValue(0)
        track_list = self.get_summary_details()
        preview_frames = self.get_video_preview_frames(int(track_list[4]))
        self.total_preview_frames = int(track_list[4])
        new_video_frame = VideoFrame()
        self.clear_temp_folder()

        # Extract frames
        self.ui.progressBar_status.setValue(50)
        new_video_frame.extract_and_save_frames(self.ui.progressBar_status, self.selected_video_filepath,
                                                self.temp_folder_path, preview_frames)
        self.set_preview_frame_images_list()
        # self.set_preview_frame_image()

        self.ui.pushButton_videoPreview_prev.setEnabled(True)
        self.ui.pushButton_videoPreview_next.setEnabled(True)

        self.ui.label_videoPreview_image.setPixmap(self.preview_frame_image_list[0])
        self._preview_frame_image_counter = 0

        self.ui.label_summary_format_content.setText(track_list[0])
        self.ui.label_summary_resolution_content.setText(track_list[1])
        self.ui.label_summary_duration_content.setText(track_list[2])
        self.ui.label_summary_framerate_content.setText(track_list[3])
        self.ui.label_summary_frames_content.setText(track_list[4])
        self.ui.label_summary_processed_content.setText(track_list[5])
        self.ui.label_status.setText("idle")
        #self.ui.label_status.hide()
        #self.ui.progressBar_status.hide()

    def set_preview_frame_images_list(self):
        def extract_number(text):
            # Extract the numeric part from the string, ignoring any leading "Frame_"
            return int(text.split("_")[1].split(".")[0])

        sorted_preview_frame_list = []
        for file in os.listdir(self.temp_folder_path):
            sorted_preview_frame_list.append(os.path.basename(file))

        sorted_preview_frame_list = sorted(sorted_preview_frame_list,
                                           key=extract_number)

        preview_image_path_list = []
        counter = 0
        while counter < len(sorted_preview_frame_list):
            for file in os.listdir(self.temp_folder_path):
                if file.endswith(sorted_preview_frame_list[counter]):
                    image_path = os.path.join(self.temp_folder_path, file)
                    pixmap = QPixmap(image_path)
                    preview_image_path_list.append(pixmap)
            counter += 1

        for img in preview_image_path_list:
            print(img)

        self.preview_frame_image_list = preview_image_path_list

    @staticmethod
    def get_video_preview_frames(frames):
        frame_list = []

        if frames is None:
            return frame_list

        if frames < 10:
            frame_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            i = 10
            while i <= 100:
                multiplier = i / 100
                frame_number = round(frames * multiplier)
                if frame_number >= frames:
                    frame_number = frames - 1
                frame_list.append(frame_number)
                i += 10

        return frame_list

    # Get summary details
    def get_summary_details(self):
        self.selected_video_filepath = os.path.join(self.input_folder_path,
                                                    self.ui.comboBox_videoSelection_box.currentText())

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
        # filename = os.path.basename(self.selected_video_filepath)

        if self.selected_videodetail.is_processed:
            processed = "Yes"
            self.ui.comboBox_detectedPeople_list.clear()
            self.ui.comboBox_detectedPeople_list.setCurrentIndex(-1)
            self.ui.tabWidget_content.setTabEnabled(1, True)
            self.ui.pushButton_summary_process.setDisabled(True)
            self.load_detected_persons_combobox()
        else:
            processed = "No"
            self.ui.comboBox_detectedPeople_list.clear()
            self.ui.tabWidget_content.setTabEnabled(1, False)
            self.ui.pushButton_summary_process.setEnabled(True)
            self.ui.comboBox_presetSelection_box.setEnabled(True)

        track_info_list.append(str(video_info.format))
        track_info_list.append(str(resolution))
        track_info_list.append(str(time_string))
        track_info_list.append(str(video_info.frame_rate))
        track_info_list.append(str(frames))
        track_info_list.append(str(processed))

        return track_info_list

    @staticmethod
    def get_frames(video_file):
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

    @staticmethod
    def test():
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

    @property
    def preset_combobox_list(self):
        return self.preset_combobox_list

    @preset_combobox_list.setter
    def preset_combobox_list(self, preset_combobox_list):
        self.preset_combobox_list = preset_combobox_list

    @property
    def preview_frame_pixmap_list(self):
        return self._preview_frame_pixmap_list

    @preview_frame_pixmap_list.setter
    def preview_frame_pixmap_list(self, preview_frame_pixmap_list):
        self._preview_frame_pixmap_list = preview_frame_pixmap_list

    @property
    def preview_crop_pixmap_list(self):
        return self._preview_crop_pixmap_list

    @preview_crop_pixmap_list.setter
    def preview_crop_pixmap_list(self, preview_crop_pixmap_list):
        self._preview_crop_pixmap_list = preview_crop_pixmap_list

    @property
    def last_button_clicked(self):
        return self._last_button_clicked

    @last_button_clicked.setter
    def last_button_clicked(self, last_button_clicked):
        self._last_button_clicked = last_button_clicked

    @property
    def auto_button_state(self):
        return self._auto_button_state

    @auto_button_state.setter
    def auto_button_state(self, button_state):
        self._auto_button_state = button_state

    @property
    def selected_person_crop_counter(self):
        return self._selected_person_crop_counter

    @selected_person_crop_counter.setter
    def selected_person_crop_counter(self, counter):
        self._selected_person_crop_counter = counter

    @property
    def preview_frame_image_list(self):
        return self._preview_frame_image_list

    @preview_frame_image_list.setter
    def preview_frame_image_list(self, preview_frame_image_list):
        self._preview_frame_image_list = preview_frame_image_list


    @property
    def selected_videodetail(self):
        return self._selected_videodetail

    @selected_videodetail.setter
    def selected_videodetail(self, selected_videodetail):
        self._selected_videodetail = selected_videodetail

    @property
    def selected_video(self):
        return self._selected_video

    @selected_video.setter
    def selected_video(self, selected_video):
        self._selected_video = selected_video

    @property
    def selected_video_filepath(self):
        return self._selected_video_filepath

    @selected_video_filepath.setter
    def selected_video_filepath(self, filepath):
        self._selected_video_filepath = filepath

    @property
    def videodetails_list(self):
        return self._videodetails_list

    @videodetails_list.setter
    def videodetails_list(self, videodetails_list):
        self._videodetails_list = videodetails_list

    @property
    def videodetails_persons_list(self):
        return self._videodetails_persons_list

    @videodetails_persons_list.setter
    def videodetails_persons_list(self, persons_list):
        self._videodetails_persons_list = persons_list

    @property
    def input_video_list(self):
        return self._input_video_list

    @input_video_list.setter
    def input_video_list(self, input_video_list):
        self._input_video_list = input_video_list

    @property
    def selected_build_folder_path(self):
        return self.selected_build_folder_path

    @selected_build_folder_path.setter
    def selected_build_folder_path(self, folder_path):
        self.selected_build_folder_path = folder_path

    @property
    def selected_person(self):
        return self._selected_person

    @selected_person.setter
    def selected_person(self, selected_person):
        self._selected_person = selected_person

    @property
    def selected_person_crop_list(self):
        return self._selected_person_crop_list

    @selected_person_crop_list.setter
    def selected_person_crop_list(self, selected_person_crop_list):
        self._selected_person_crop_list = selected_person_crop_list


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setApplicationName("Security System")
    main_window = SummaryLogic()

    app.exec()
    app.activeWindow()
