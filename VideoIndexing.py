import os
import re
import shutil
import sys
from typing import Optional

import cv2
import sqlite3
from PySide6.QtSql import QSqlDatabase, QSqlQuery
import json
from ImageProcessing import Frame, Crop, Person


class VideoDetails:

    def __init__(self, video_title):
        self._video_title = video_title
        self._is_processed = False
        # self._person_list = None
        # self._processed_frames_list = None


        self.input_folder = r".\input"
        self.output_folder = r".\output"
        self.inferred_folder = r".\output\inferred"
        self.processed_folder = r".\output\builds"

        self.make_directory(self.input_folder)
        self.make_directory(self.output_folder)
        self.make_directory(self.processed_folder)

    def save_videodetails_sqldata(self):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO VideoDetails(video_title, is_processed) VALUES (?, ?)", (self.video_title, self.is_processed))
        conn.commit()
        conn.close()

    def save_frame_sqldata(self, processed_frame_list : Optional[list[Frame]]):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        for frame in processed_frame_list:
            cursor.execute(f"INSERT INTO Frame(frame_number, frame_folder_path, frame_folder, frame_image, label_file_path) "
                                f"VALUES (?, ?, ?, ?, ?)",
                    (frame.frame_number, frame.frame_folder_path, frame.frame_folder, frame.frame_image, frame.label_file_path))
        conn.commit()
        conn.close()

    def save_person_sqldata(self, indexed_persons_list : Optional[list[Person]]):
        #conn = sqlite3.connect(r'..\DBMS_Database\main.db')
        conn = sqlite3.connect(r'main.db')
        cursor = conn.cursor()
        for person in indexed_persons_list:
            cursor.execute(f"INSERT INTO Person(person_id, has_montage) "
                                f"VALUES (?, ?)",
                    (person.person_id, person.has_montage))
        conn.commit()
        conn.close()
    def save_crop_sqldata(self, crop_list : Optional[list[Crop]]):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        for crop in crop_list:
            cursor.execute(f"INSERT INTO Crop(crop_id, person_id, frame_number, yolo_class, crop_path, label_line, frame_image)"
                                f" VALUES (?, ?, ?, ?, ?, ? ,?)",
                    (crop.crop_id, crop.person_id, crop.frame_number, crop.yolo_class, crop.crop_path, crop.label_line, crop.frame_image))
        conn.commit()
        conn.close()

    def load_sql_data(self):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VideoDetails")
        all_entries = cursor.fetchall()
        conn.close()

        list = []
        for detail in all_entries:
            list.append(VideoDetails(detail, detail.video_detail))

    def index_persons(self):
        def extract_frame_number(frame_folder):
            extract_frame_number = re.findall(r"\d+\.?\d*", frame_folder)
            if extract_frame_number == []:
                extract_frame_number = "1"
            return extract_frame_number

        if not os.path.exists(self.inferred_folder):
            print("ERROR! No inferencing occurred")
            pass

        indexed_persons_list = []
        processed_frames_list = []
        crop_list = []
        crop_count = 0
        frame_folders = os.path.join(self.inferred_folder, self.video_title)
        for folder in os.listdir(frame_folders):
            frame_folder_path = os.path.join(frame_folders, folder)
            if (len(os.listdir(frame_folder_path)) != 3):  #Check if the folder is not corrupted
                continue

            frame_number = extract_frame_number(frame_folder=os.path.basename(frame_folder_path))
            frame = Frame(frame_number=int(frame_number[0]), frame_folder_path=frame_folder_path)

            person_list = frame.create_person_list(indexed_persons_list)
            indexed_persons_list.extend(person_list)

            # Create crops
            new_crop_list = frame.create_crop_list(crop_count)
            crop_list.extend(new_crop_list)
            crop_count += len(frame.find_crops_list_path())

            processed_frames_list.append(frame)

        self.is_processed = True
        self.save_videodetails_sqldata()
        self.save_frame_sqldata(processed_frame_list=processed_frames_list)
        self.save_person_sqldata(indexed_persons_list=indexed_persons_list)
        self.save_crop_sqldata(crop_list=crop_list)

    def build_indexed_persons(self):
        if self.person_list is None:
            print("Video is not indexed")
            pass
        video_build_directory = os.path.join(self.processed_folder, self.video_title)
        self.make_directory(video_build_directory)

        for person in self.person_list:
            person_folder_name = "person_"
            new_person_folder = os.path.join(video_build_directory, person_folder_name + person.person_id)
            if not os.path.exists(new_person_folder):
                os.mkdir(new_person_folder)
            else:
                continue
            for crop in person.crop_list:
                shutil.copyfile(crop.crop_path, new_person_folder + "/" + crop.frame_number + ".jpg")


    def __str__(self):
        return f"MyClass(data={self.video_title})"

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def video_title(self):
        return self._video_title

    @property
    def person_list(self):
        return self._person_list

    @property
    def processed_frames_list(self):
        return self._processed_frames_list

    @property
    def is_processed(self):
        return self._is_processed

    @is_processed.setter
    def is_processed(self, is_processed):
        self._is_processed = is_processed

    @person_list.setter
    def person_list(self, person_list):
        self._person_list = person_list

    @processed_frames_list.setter
    def processed_frames_list(self, processed_frames_list):
        self._processed_frames_list = processed_frames_list

    def make_directory(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    def start_inferencing(self):
        pass

if __name__ == "__main__":
    x = VideoDetails("Thesis_FullOfficeCut_T300_5mins")
    x.index_persons()
    #x.sql()
    #x.index_persons()
    #x.build_indexed_persons()

    def save_class(obj):
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        serialized_data = obj.to_json()
        try:
            cursor.execute("")
            conn.commit()
            print("Class saved successfully")
        except sqlite3.Error as e:
            print("Error saving class:", e)
        finally:
            conn.close()

    def load_class():
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT class_date FROM classes")
            #row = cursor.fetchone()
        finally:
            pass

