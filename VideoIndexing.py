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

    def __init__(self, video_title, is_processed=False):
        self._video_title = video_title
        self._is_processed = is_processed
        # self._person_list = None
        # self._processed_frames_list = None


        self.input_folder = r".\input"
        self.output_folder = r".\output"
        self.inferred_folder = r".\output\inferred"
        self.processed_folder = r".\output\builds"

        self.make_directory(self.input_folder)
        self.make_directory(self.output_folder)
        self.make_directory(self.processed_folder)

    def save_videodetails_sql(self):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO VideoDetails(video_title, is_processed) VALUES (?, ?)", (self.video_title, self.is_processed))
        conn.commit()
        conn.close()

    def save_frame_sql(self, processed_frame_list : Optional[list[Frame]]):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        for frame in processed_frame_list:
            cursor.execute(f"INSERT INTO Frame(frame_number, frame_folder_path, frame_folder, frame_image, label_file_path) "
                                f"VALUES (?, ?, ?, ?, ?)",
                    (frame.frame_number, frame.frame_folder_path, frame.frame_folder, frame.frame_image, frame.label_file_path))
        conn.commit()
        conn.close()

    def save_person_sql(self, indexed_persons_list : Optional[list[Person]]):
        #conn = sqlite3.connect(r'..\DBMS_Database\main.db')
        conn = sqlite3.connect(r'main.db')
        cursor = conn.cursor()
        for person in indexed_persons_list:
            cursor.execute(f"INSERT INTO Person(person_id, has_montage) "
                                f"VALUES (?, ?)",
                    (person.person_id, person.has_montage))
        conn.commit()
        conn.close()
    def save_crop_sql(self, crop_list : Optional[list[Crop]]):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        for crop in crop_list:
            cursor.execute(f"INSERT INTO Crop(crop_id, person_id, frame_number, yolo_class, crop_path, label_line, frame_image)"
                                f" VALUES (?, ?, ?, ?, ?, ? ,?)",
                    (crop.crop_id, crop.person_id, crop.frame_number, crop.yolo_class, crop.crop_path, crop.label_line, crop.frame_image))
        conn.commit()
        conn.close()

    def load_videodetails_sql(self):
        try:
            conn = sqlite3.connect('main.db')

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

    def load_frame_sql(self):
        try:
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Frame")
            all_entries = cursor.fetchall()
            conn.close()

            frame_list = []
            for detail in all_entries:
                frame_number, frame_folder_path, frame_folder, frame_image, label_file_path = detail
                frame_list.append(Frame(frame_number=frame_number,frame_folder_path=frame_folder_path
                                  ,frame_folder=frame_folder, frame_image=frame_image, label_file_path=label_file_path))

            return frame_list

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def load_person_sql(self):
        try:
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Person")
            all_entries = cursor.fetchall()
            conn.close()

            person_list = []
            for detail in all_entries:
                person_id, has_montage = detail
                person_list.append(Person(person_id=person_id, has_montage=has_montage))

            return person_list

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def load_crop_sql(self):
        try:
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Crop")
            all_entries = cursor.fetchall()
            conn.close()

            list = []
            for detail in all_entries:
                crop_id, person_id, frame_number, yolo_class, crop_path, label_line, frame_image = detail
                list.append(Crop(crop_id=crop_id,
                                 person_id=person_id,
                                 frame_number=frame_number
                                 ,yolo_class=yolo_class,
                                 crop_path=crop_path,
                                 label_line=label_line
                                 ,frame_image=frame_image))

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_person_crops_sql(self, person_id : Optional[int]):
        try:
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM Crop WHERE person_id = {person_id};")
            all_entries = cursor.fetchall()
            conn.close()

            crop_list = []
            for detail in all_entries:
                crop_id, person_id, frame_number, yolo_class, crop_path, label_line, frame_image = detail
                crop_list.append(Crop(crop_id=crop_id,
                                     person_id=person_id,
                                     frame_number=frame_number,
                                     yolo_class=yolo_class,
                                     crop_path=crop_path,
                                     label_line=label_line,
                                     frame_image=frame_image))

            return crop_list

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")

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
        self.save_videodetails_sql()
        self.save_frame_sql(processed_frame_list=processed_frames_list)
        self.save_person_sql(indexed_persons_list=indexed_persons_list)
        self.save_crop_sql(crop_list=crop_list)

    def build_indexed_persons(self):
        if(not self.is_processed):
            print("Video is not processed")
            pass

        person_list = self.load_person_sql()

        video_build_directory = os.path.join(self.processed_folder, self.video_title)
        self.make_directory(video_build_directory)

        for person in person_list:
            person_crop_list = self.get_person_crops_sql(person.person_id)
            person_folder_name = "person_"
            new_person_folder = os.path.join(video_build_directory, person_folder_name + str(person.person_id))
            if not os.path.exists(new_person_folder):
                os.mkdir(new_person_folder)
            else:
                continue
            for crop in person_crop_list:
                shutil.copyfile(crop.crop_path, new_person_folder + "/" + str(crop.frame_number) + ".jpg")

    def start_inferencing(self):
        pass

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

if __name__ == "__main__":
    x = VideoDetails(video_title="Thesis_FullOfficeCut_T300_5mins", is_processed=True)
    x.index_persons()
    x.build_indexed_persons()
    #x.sql()
    #x.index_persons()
    #x.build_indexed_persons()

