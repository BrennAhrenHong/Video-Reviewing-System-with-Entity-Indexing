import sqlite3
from typing import Optional

from VideoIndexing import VideoDetails
from ImageProcessing import Frame, Crop, Person

class SqliteScripts:
    def __init__(self):
        pass

    def fetchall(self, query):
        try:
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute(query)
            all_entries = cursor.fetchall()
            conn.close()

            return all_entries

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def load_all_frame_sql(self, video_title):
        script = f"SELECT * FROM Frame WHERE video_title = '{video_title}';"
        all_entries = self.fetchall(script)
        frame_list = []
        for detail in all_entries:
            frame_id, frame_number, frame_folder_path, frame_folder, frame_image, label_file_path, video_title = detail
            frame_list.append(Frame(frame_number=frame_number, frame_folder_path=frame_folder_path
                                    , frame_folder=frame_folder, frame_image=frame_image,
                                    label_file_path=label_file_path, video_title=video_title))

        return frame_list


    def load_person_from_video_sql(self, video_title):
        script = f"SELECT * FROM Person WHERE video_title = '{video_title}';"
        all_entries = self.fetchall(script)

        person_list = []
        for detail in all_entries:
            person_name, person_id, has_montage, video_title = detail
            person_list.append(Person(person_id=person_id, has_montage=has_montage, video_title=video_title))

        return person_list


    def load_crop_sql(self, video_title):
        script = f"SELECT * FROM Crop WHERE video_title = '{video_title}';"
        all_entries = self.fetchall(script)

        crop_list = []
        for detail in all_entries:
            crop_name, crop_id, person_id, frame_number, yolo_class, crop_path, label_line, frame_image = detail
            crop_list.append(Crop(crop_id=crop_id,
                                  person_id=person_id,
                                  frame_number=frame_number
                                  , yolo_class=yolo_class,
                                  crop_path=crop_path,
                                  label_line=label_line
                                  , frame_image=frame_image))

        return crop_list


    def get_processed_videos(self, ):
        script = "SELECT * FROM VideoDetails"
        all_entries = self.fetchall(script)

        videodetails_db_list = []
        for detail in all_entries:
            video_title, is_processed = detail
            videodetails_db_list.append(VideoDetails(video_title=video_title, is_processed=is_processed))

        return videodetails_db_list

    def get_person_crops_sql(self, person_id: Optional[int], video_title):
        script = f"SELECT * FROM Crop WHERE person_id = {person_id} AND video_title='{video_title}';"
        all_entries = self.fetchall(script)

        crop_list = []
        for detail in all_entries:
            (crop_name, crop_id, person_id, video_title, frame_number, yolo_class, crop_path, label_line,
             frame_image) = detail

            crop_list.append(Crop(crop_id=crop_id,
                                  person_id=person_id,
                                  video_title=video_title,
                                  frame_number=frame_number,
                                  yolo_class=yolo_class,
                                  crop_path=crop_path,
                                  label_line=label_line,
                                  frame_image=frame_image))

        return crop_list

    def get_person_from_id_sql(self, person_id: Optional[int], video_title: Optional[str]):
        script = f"SELECT * FROM Person WHERE person_id = {person_id} AND video_title = '{video_title}';"
        all_entries = self.fetchall(script)

        person_list = []
        for detail in all_entries:
            person_name, person_id, has_montage, video_title = detail
            person_list.append(Person(person_id=person_id, has_montage=has_montage, video_title=video_title))

        return person_list

    def videodetails_is_processed_true(self, video_title):
        try:
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE VideoDetails SET (is_processed = True;) WHERE video_title='{video_title}';")
            conn.close()

            return True

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def person_has_montage_true(self, video_title, person_id):
        try:
            number_id = person_id.split("_")[1]
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE Person SET has_montage = True WHERE video_title='{video_title}' AND person_id={number_id};")
            conn.close()

            return True

        except sqlite3.Error as e:
            print(f"Error connecting to database:{e}")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    x = SqliteScripts()
    y = x.get_person_crops_sql(1)

    for crop in y:
        print(crop.crop_id)
