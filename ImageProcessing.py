import os
import re
from typing import Optional

class Frame:

    # Properties
    def __init__(self, frame_folder_path):
        self._frame_folder_path = frame_folder_path
        self._frame_folder = os.path.basename(self._frame_folder_path)

        extracted_frame_number = self.extract_frame_number(self._frame_folder)
        self._frame_number = extracted_frame_number[0]

        self._frame = self.find_frame()
        self._label_path = self.find_label_path()
        self._crops_list_path = self.find_crops_list_path() #crops path
        self._label_list = self.read_label()

        self._crop_list = self.create_crop_list()
    @property
    def frame_folder_path(self):
        return self._frame_folder_path

    @property
    def frame_folder(self):
        return self._frame_folder

    @property
    def frame_number(self):
        return self._frame_number

    @property
    def frame(self):
        return self._frame

    @property
    def label_path(self):
        return self._label_path

    @property
    def crops_list_path(self):
        return self._crops_list_path

    @property
    def label_list(self):
        return self._label_list

    @property
    def crop_list(self):
        return self._crop_list

    @crop_list.setter
    def crop_list(self, crop_list):
        self._crop_list = crop_list
    def extract_frame_number(self, folder_name):
        extract_frame_number = re.findall(r"\d+\.?\d*", self._frame_folder)
        if extract_frame_number == []:
            extract_frame_number = "1"
        return extract_frame_number

    def find_frame(self):
        frame_img = None
        for file in os.listdir(self._frame_folder_path):
            if file.endswith((".jpg", ".jpeg", ".png")):
                frame_img = os.path.join(self._frame_folder, file)
                break
        return frame_img

    def find_label_path(self):
        label_folder_path = os.path.join(self.frame_folder_path, "labels")
        label_file_path = None
        for file in os.listdir(label_folder_path):
            if file.endswith(".txt"):
                label_file_path = os.path.join(label_folder_path, file)
                break
        return label_file_path

    def read_label(self):
        label_file_path = self._label_path
        try:
            with open(label_file_path, 'r') as file:
                label_file = file.readlines()
                if label_file:
                    lines = []
                    for label in label_file:
                        lines.append(label.strip())
                return lines
        except FileNotFoundError:
            print(f"Error: File '{label_file_path}' not found.")
        except Exception as e:
            print(f"Error reading file '{label_file_path}': {e}")

    def find_crops_list_path(self):
        crops_folder_path = os.path.join(self._frame_folder_path, "crops", "person")
        crops_path_list = []
        for img in os.listdir(crops_folder_path):
            crops_path = os.path.join(crops_folder_path, img)
            crops_path_list.append(crops_path)
        return crops_path_list

    def create_crop_list(self):

        crop_list = []
        counter = 0
        while (counter < len(self.label_list)):
            crop = self.crops_list_path
            label = self.label_list
            label_line = self.label_list[counter]
            crop_id = label_line[5]

            new_crop = Crop(yolo_class=0, crop_path=crop[counter], crop_id=crop_id, label=label[counter],
                            frame=self.frame)
            crop_list.append(new_crop)

        return crop_list


class Crop:

    #def __init__(self, yolo_class, crop_path, label, frame: Optional[Frame]):
    def __init__(self, yolo_class, crop_path, crop_id, label, frame):
        self._yolo_class = yolo_class
        self._crop_path = crop_path
        self._label = label
        self._frame = frame

        self._crop_id = crop_id
        self._frame_coordinates = self._set_frame_coordinates()
        self._hash_value = None

    @property
    def crop_path(self):
        return self._crop_path

    @property
    def label(self):
        return self._label

    @property
    def frame(self):
        return self._frame

    @property
    def crop_id(self):
        return self._crop_id

    @property
    def hash_value(self):
        return self._hash_value

    @hash_value.setter
    def hash_value(self, new_hash_value):
        self._hash_value = new_hash_value


    def _set_frame_coordinates(self):
        coordinates = []
        coordinates.append(self._label[1])
        coordinates.append(self._label[2])
        coordinates.append(self._label[3])
        coordinates.append(self._label[4])
        return coordinates

class Person:

    def __init__(self, person_id):
        self._person_id = person_id
        self._crop_list = []
        self._is_processed = False

    @property
    def person_id(self):
        return self._person_id

    @property
    def crop_list(self):
        return self._crop_list

    def add_crop(self, crop):
        self._crop_list.append(crop)

    @crop_list.setter
    def crop_list(self, crop_list):
        self._crop_list = crop_list


    @property
    def is_processed(self):
        return self._is_processed

    @is_processed.setter
    def is_processed(self, is_processed):
        self._is_processed = is_processed