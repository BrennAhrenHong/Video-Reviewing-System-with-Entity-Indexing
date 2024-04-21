import os
import re
import shutil
import cv2
from ImageProcessing import Frame, Crop, Person


class VideoDetails:

    def __init__(self, video_title):
        self._video_title = video_title
        self._person_list = None
        self._processed_frames_list = None
        self._is_processed = False

        self.input_folder = r".\input"
        self.output_folder = r".\output"
        self.inferred_folder = r".\output\inferred"
        self.processed_folder = r".\output\builds"

        self.make_directory(self.input_folder)
        self.make_directory(self.output_folder)
        self.make_directory(self.processed_folder)

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

    def index_persons(self):
        if not os.path.exists(self.inferred_folder):
            print("ERROR! No inferencing occurred")
            pass

        indexed_persons_list = []
        frame_folders = os.path.join(self.inferred_folder, self.video_title)
        for folder in os.listdir(frame_folders):
            folder_path = os.path.join(frame_folders, folder)
            if (len(os.listdir(folder_path)) != 3):  #Check if the folder is not corrupted
                continue

            frame = Frame(folder_path)

            # Create crops
            for crop in frame.crop_list:

                new_person = Person(person_id=crop.crop_id)
                # Create Person
                if len(indexed_persons_list) == 0:
                    new_person.crop_list.append(crop)
                    indexed_persons_list.append(new_person)
                else:
                    person_not_found = False
                    for person in indexed_persons_list:
                        if person.person_id == new_person.person_id:  # Checking if person exists
                            person.crop_list.append(crop)
                            person_not_found = True
                            break
                    if person_not_found == False:
                        new_person.crop_list.append(crop)  # what happened???
                        indexed_persons_list.append(new_person)

        self.person_list = indexed_persons_list

    def build_indexed_persons(self):
        if self.person_list is None:
            print("Video is not indexed")
            pass
        video_build_directory = os.path.join(self.processed_folder, self.video_title)
        self.make_directory(video_build_directory)

        for person in self.person_list:
            person_folder_name = "person_"
            new_person_folder = os.path.join(video_build_directory, person_folder_name + person.person_id)
            if (os.path.exists(new_person_folder) == False):
                os.mkdir(new_person_folder)
            for crop in person.crop_list:
                shutil.copyfile(crop.crop_path, new_person_folder + "/" + crop.frame_number + ".jpg")

        #frame_folders = os.path.join(self.output_folder, self.video_title)
        #for folder in os.listdir(frame_folders):
        pass


if __name__ == "__main__":
    x = VideoDetails("Thesis_FullOfficeCut_T300_5mins")
    x.index_persons()
    x.build_indexed_persons()
