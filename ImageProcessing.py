import os
import re
import json
import sqlite3
from typing import Optional


class Frame:

    # Properties
    def __init__(self, frame_number: Optional[int], frame_folder_path, frame_folder=None, frame_image = None, label_file_path=None):
        self._frame_number = frame_number
        self._frame_folder_path = frame_folder_path

        if frame_folder is None:
            self._frame_folder = os.path.basename(self.frame_folder_path)
        else:
            self._frame_folder = frame_folder

        if frame_image is None:
            self._frame_image = self.find_frame()
        else:
            self._frame_image = frame_image

        if label_file_path is None:
            self._label_file_path = self.find_label_file_path()
        else:
            self._label_file_path = label_file_path

    @property
    def frame_folder_path(self):
        return self._frame_folder_path

    @property
    def frame_folder(self):
        return self._frame_folder

    @frame_folder.setter
    def frame_folder(self, frame_folder):
        self.frame_folder = frame_folder

    @property
    def frame_number(self):
        return self._frame_number

    @property
    def frame_image(self):
        return self._frame_image

    @property
    def label_file_path(self):
        return self._label_file_path

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

    def find_label_file_path(self):
        label_folder_path = os.path.join(self.frame_folder_path, "labels")
        label_file_path = None
        for file in os.listdir(label_folder_path):
            if file.endswith(".txt"):
                label_file_path = os.path.join(label_folder_path, file)
                break
        return label_file_path

    def read_label(self):
        label_file_path = self._label_file_path
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

    def create_person_list(self, indexed_person_list):
        label_list = self.read_label()
        new_indexed_person_list = []
        counter = 0
        found_match = False

        if len(indexed_person_list) == 0 and len(label_list) > counter:
            label_line = label_list[counter]
            label_split = label_line.split(' ')
            person_id = int(label_split[5])
            new_person = Person(person_id=person_id)
            new_indexed_person_list.append(new_person)
            return new_indexed_person_list

        while len(label_list) > counter:
            label_line = label_list[counter]
            label_split = label_line.split(' ')
            person_id = int(label_split[5])

            new_person = Person(person_id=person_id)

            for person in indexed_person_list:
                if new_person.person_id == person.person_id:
                    found_match = True
                    break

            if found_match:
                counter += 1
                found_match = False
                continue

            new_indexed_person_list.append(new_person)
            counter += 1


        return new_indexed_person_list

    def create_crop_list(self, crop_number):
        label_list = self.read_label()
        crops_list_path = self.find_crops_list_path()
        crop_list = []
        crop_id = crop_number + 1
        counter = 0
        while (counter < len(label_list)):
            crop = crops_list_path
            label_line = label_list[counter]
            label_split = label_line.split(' ')
            person_id = int(label_split[5])

            new_crop = Crop(crop_id=crop_id, person_id=person_id, frame_number=self.frame_number, yolo_class=0, crop_path=crop[counter], label_line=label_line,
                            frame_image=self.frame_image)
            crop_list.append(new_crop)
            counter += 1
            crop_id += 1

        return crop_list


class Crop:

    #def __init__(self, yolo_class, crop_path, label, frame: Optional[Frame]):
    def __init__(self, crop_id, person_id, frame_number, yolo_class, crop_path, label_line, frame_image):
        self._crop_id = crop_id
        self._person_id = person_id
        self._frame_number = frame_number
        self._yolo_class = yolo_class
        self._crop_path = crop_path
        self._label_line = label_line
        self._frame_image = frame_image


        # self._frame_coordinates = self._set_frame_coordinates()
        self._hash_value = None

    # def _set_frame_coordinates(self):
    #     coordinates = []
    #     coordinates.append(self._label[1])
    #     coordinates.append(self._label[2])
    #     coordinates.append(self._label[3])
    #     coordinates.append(self._label[4])
    #     return coordinates

    @property
    def crop_path(self):
        return self._crop_path

    @property
    def person_id(self):
        return self._person_id

    @property
    def yolo_class(self):
        return self._yolo_class

    @property
    def label_line(self):
        return self._label_line
    # @property
    # def label(self):
    #     return self._label

    @property
    def frame_image(self):
        return self._frame_image

    @property
    def frame_number(self):
        return self._frame_number

    @property
    def crop_id(self):
        return self._crop_id

    @property
    def hash_value(self):
        return self._hash_value

    @hash_value.setter
    def hash_value(self, new_hash_value):
        self._hash_value = new_hash_value


class Person:

    def __init__(self, person_id: Optional[int], has_montage=None):
        self._person_id = person_id

        if has_montage is None:
            self._has_montage = False
        else:
            self._has_montage = has_montage


    @property
    def person_id(self):
        return self._person_id

    @property
    def has_montage(self):
        return self._has_montage

    @has_montage.setter
    def has_montage(self, has_montage):
        self._has_montage = has_montage