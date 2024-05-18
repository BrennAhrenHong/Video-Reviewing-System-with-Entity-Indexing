import cv2

def get_frame_timestamp(video_path, frame_number, fps=None):
    """
    Gets the timestamp in milliseconds for a specific frame in a video using
    either video properties or a constant frame rate.

    Args:
        video_path (str): Path to the video file.
        frame_number (int): The frame number for which to get the timestamp.
        fps (float, optional): Constant frame rate to use if video properties
            cannot be retrieved. Defaults to None.

    Returns:
        float: Timestamp in milliseconds for the specified frame,
               or None if the frame cannot be accessed.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Error opening video file.")

    # Try to get frame rate from video properties
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
    except:
        if fps is None:
            raise ValueError("Could not retrieve frame rate from video. Please provide a constant frame rate (fps) argument.")

    # Seek to the desired frame
    if not cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1):
        print(f"Warning: Could not seek to frame {frame_number}.")
        cap.release()
        return None

    # Read the frame (may not succeed if frame is out of range)
    ret, frame = cap.read()

    cap.release()

    if not ret:
        print(f"Warning: Could not read frame {frame_number}.")
        return None

    # Calculate timestamp based on frame number and frame rate
    timestamp_ms = frame_number * (1000 / fps)/1000

    return timestamp_ms

# Testing
video_path = f"./input/Thesis_Hdlcut_T100_5Mins_5fps_20secs.mp4"
frame_number = 92
fps = 5  # Or provide a constant frame rate if needed

try:
    timestamp = get_frame_timestamp(video_path, frame_number, fps)
    timestamp2 = get_frame_timestamp(video_path, frame_number, fps)

    text_to_write = f"Timestamp 1: {timestamp}\nTimestamp 2: {timestamp2}"

    # Open the file in write mode ("w") with a descriptive filename
    with open("./timestamps/my_notepad.txt", "w") as notepad_file:
        # Write the text to the file
        notepad_file.write(text_to_write)

    if timestamp is not None:
        print(f"Timestamp for frame {frame_number}: {timestamp:.2f} s")
except ValueError as e:
    print(e)