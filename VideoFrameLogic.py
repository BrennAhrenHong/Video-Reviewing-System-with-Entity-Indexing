import cv2
import os

class VideoFrame:

    def __init__(self):
        pass

    def extract_and_save_frames(self, ui_progressBar, video_path, output_path, frame_numbers):
        """Extracts specific frames from a video and saves them as PNG images.

        Args:
            video_path (str): The path to the video file.
            frame_numbers (list): A list of integers representing the desired frame numbers.

        Returns:
            int: The number of frames successfully extracted and saved,
                or -1 if there's an error.
        """

        cap = cv2.VideoCapture(video_path)
        saved_count = 0

        if not cap.isOpened():
            print("Error opening video file.")
            return -1

        # Loop through the desired frame numbers
        for frame_number in frame_numbers:
            # Check if frame number is valid (within video length)
            num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if frame_number < 0 or frame_number >= num_frames:
                print(f"Frame number {frame_number} is out of range.")
                continue  # Skip to the next frame number in the list

            # Set the capture frame to the desired frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            # Read the frame
            ret, frame = cap.read()

            if not ret:
                print(f"Error reading frame {frame_number}.")
                continue  # Skip to the next frame number in the list

            # Construct the output filename (e.g., frame_001.png)
            filename = f"frame_{frame_number}.png"
            output = os.path.join(os.path.dirname(output_path), filename)

            # Save the frame as a PNG image
            if cv2.imwrite(output, frame):
                saved_count += 1
                ui_progressBar.setValue(50 + (saved_count/len(frame_numbers)*50))
                print(f"Frame {frame_number} saved as '{output}'.")

            else:
                print(f"Error saving frame {frame_number}.")
