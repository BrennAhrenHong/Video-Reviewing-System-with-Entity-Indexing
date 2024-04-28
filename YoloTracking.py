from ultralytics import YOLO
import os.path
import cv2
import time


def start_yolo(video_source, model, output_path, imgsz=1280, iou=0.8, conf=0.5, device="CPU"):
    cap = cv2.VideoCapture(video_source)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 5.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Attempt to make folder
    try:
        os.makedirs(output_path)
    except OSError as e:
        print(e)

    # create video file
    output_video_path = os.path.join(output_path, 'annotated_video.avi')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # output path of inference output folder
    project_output_path = os.path.join(output_path, "inference_output")

    # inferencing time list
    inference_times_list = []

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:

            # start time
            start_time = time.time()

            # run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True, classes=0, save=True, save_crop=True, save_txt=True, tracker="bytetrack.yaml",
                                  project=project_output_path, name="F", imgsz=imgsz, iou=iou, conf=conf, device=device)
            # end time
            end_time = time.time()

            # record inference time
            inference_time = end_time - start_time
            inference_times_list.append(inference_time)

            # visualize the results on the frame
            #annotated_frame = results[0].plot()

            # write
            #out.write(annotated_frame)

            # Display the annotated frame
            #cv2.imshow("YOLOv8 Tracking", annotated_frame)

            # break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # break the loop if the end of the video is reached
            break

    # release the video capture object and close the display window
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # save avg inference time to notepad
    mean_inference_time = sum(inference_times_list) / len(inference_times_list)

    inference_time_filename = os.path.join(output_path, "inference time.txt")
    with open(inference_time_filename, 'w') as file:
        file.write(str(mean_inference_time))
    pass


def test_all_model(video_source, def_output):
    yolov8n = YOLO('yolov8n.pt')
    yolov8s = YOLO('yolov8s.pt')
    yolov8m = YOLO('yolov8m.pt')
    yolov8l = YOLO('yolov8l.pt')
    yolov8x = YOLO('yolov8x.pt')

    yolo_model_list = [yolov8n, yolov8s, yolov8m, yolov8l, yolov8x]
    model_index = 0

    while model_index < len(yolo_model_list):
        model = yolo_model_list[model_index]

        m_filename, m_extension = str.split(model.model_name, sep='.')
        output_folder_path = os.path.join(def_output, m_filename)

        if os.path.exists(output_folder_path):
            i = 0
            new_output_path = output_folder_path
            while os.path.exists(new_output_path):
                i += 1
                new_output_path = output_folder_path + '_' + str(i)
            output_folder_path = new_output_path

        cap = cv2.VideoCapture(video_source)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 5.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Attempt to make folder
        try:
            os.makedirs(output_folder_path)
        except OSError as e:
            print(e)

        # create video file
        output_video_path = os.path.join(output_folder_path, 'annotated_video.avi')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        # output path of inference output folder
        project_output_path = os.path.join(output_folder_path, "inference_output")

        # inferencing time list
        inference_times_list = []

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:

                # start time
                start_time = time.time()

                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = model.track(frame, persist=True, classes=0, save=True, save_crop=True, save_txt=True,
                                      project=project_output_path, name="F", imgsz=1280, iou=0.8, conf=0.5, device=0)
                # end time
                end_time = time.time()

                # record inference time
                inference_time = end_time - start_time
                inference_times_list.append(inference_time)

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Write
                out.write(annotated_frame)

                # Display the annotated frame
                #cv2.imshow("YOLOv8 Tracking", annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        # Save avg inference time to notepad
        mean_inference_time = sum(inference_times_list) / len(inference_times_list)

        inference_time_filename = os.path.join(output_folder_path, "inference time.txt")
        with open(inference_time_filename, 'w') as file:
            file.write(str(mean_inference_time))

        model_index += 1
    pass


if __name__ == "__main__":
    # model = YOLO('yolov8n.pt')
    # model = YOLO('yolov8s.pt')
    model = YOLO('yolov8m.pt')
    # model = YOLO('yolov8l.pt')
    # model = YOLO('yolov8x.pt')

    model_name, model_extension = str.split(model.model_name, sep='.')

    # video_source = r"D:\A_Video_Folder\Thesis_Files\HDL_Videos\Cuts\Thesis_Hdlcut_T100_5Mins_5fps.mp4"
    video_source_path = r"./videos/Thesis_Hdlcut_T100_5Mins_5fps.mp4"
    #video_source_path = r"./videos/Thesis_FullOfficeCut_T300_5mins.mp4"
    #video_source_path = r"./videos/Thesis_Hdlcut_T100_5Mins_5fps_20secs.mp4"

    filename, extension = os.path.splitext(video_source_path)
    video_title = os.path.basename(filename)
    # project_output_path = os.path.join("./output/", video_title)

    output_path = os.path.join("./video_trials/TrackerTest", video_title, model_name)

    # Check if output folder already exists
    if os.path.exists(output_path):
        i = 0
        new_output_path = output_path
        while os.path.exists(new_output_path):
            i += 1
            new_output_path = output_path + '_' + str(i)
        output_path = new_output_path

    start_yolo(video_source=video_source_path, model=model, output_path=output_path)
    #output_path2 = os.path.join(r"./video_trials/LatencyTest", video_title)
    #test_all_model(video_source=video_source_path, def_output=output_path2)
