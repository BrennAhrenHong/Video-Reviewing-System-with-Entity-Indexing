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

    @property
    def is_processed(self):
        return self._is_processed

    @property
    def video_title(self):
        return self._video_title

    @property
    def person_list(self):
        return self._person_list

    @property
    def processed_frames_list(self):
        return self._processed_frames_list

    @person_list.setter
    def person_list(self, person_list):
        self._person_list = person_list

    @processed_frames_list.setter
    def processed_frames_list(self, processed_frames_list):
        self._processed_frames_list = processed_frames_list


class IndexingLogic:

    def __init__(self, video_title):
        self.video_title = video_title
        self.input_folder = r".\input"
        self.output_folder = r".\output"
        self.inferred_folder = r".\output\inferred"
        self.processed_folder = os.path.join(self.output_folder, r"processed")

        self.make_directory(self.input_folder)
        self.make_directory(self.output_folder)
        self.make_directory(self.processed_folder)

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
            if(len(os.listdir(folder_path)) != 3): #Check if the folder is not corrupted
                continue

            frame = Frame(folder_path)

            # Create crops
            counter = 0 # Get # of crops in frame
            crop_list = []
            while (counter < len(frame.label_list)):
                crop = frame.crops_list_path
                label = frame.label_list
                label_line = frame.label_list[counter]
                crop_id = label_line[5]

                new_crop = Crop(yolo_class=0, crop_path=crop[counter], crop_id=crop_id, label=label[counter], frame=frame.frame)
                crop_list.append(new_crop)

                new_person = Person(person_id=crop_id)
                # Create Person
                if len(indexed_persons_list) == 0:
                    indexed_persons_list.append(new_person)
                else:
                    for person in indexed_persons_list:
                        if person.person_id == new_person.person_id:
                            person.crop_list.append(new_crop)

                counter += 1
                frame.crop_list = crop_list #Save crop_list to frame to know which crops it has






        #frame_folders = os.path.join(self.output_folder, self.video_title)
        #for folder in os.listdir(frame_folders):
        pass

if __name__ == "__main__":
    x = IndexingLogic("Thesis_FullOfficeCut_T300_5mins")
    x.index_persons()
