# Press ESC to continue to the next video in --folder mode.
import cv2
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Frame Cropper Detection using YOLO in OPENCV')
parser.add_argument('--folder', help='Path to a folder containing videos.')
parser.add_argument('--video', help='Path to a video file.')
parser.add_argument('--frame', default=50, help='Save a frame once in N frames. Once in 100 frames by default')
parser.add_argument('--save_path', help='Path to the folder where to save frames cropped')
arguments = parser.parse_args()

def crop_frames(cap, save_path, frame_N, output_name):
    '''
    :param cap: video object.
    :param save_path: where to save cropped out frames
    :param frame_N: save a frame once in N frames
    :return:
    '''
    frame_counter = 0
    while cv2.waitKey(1) < 0:
        has_frame, frame = cap.read()
        if not has_frame:
            print("Video", output_name, "has been processed.")
            return

        cv2.imshow(window_name, frame)

        if frame_counter < 700:  # Skip first section of the video
            frame_counter += 1
            print(frame_counter)
            continue

        if frame_counter % frame_N == 0:
            cv2.imwrite(os.path.join(save_path, output_name + '_' + str(frame_counter) + '.jpg'), frame)
        print(frame_counter)
        frame_counter += 1

def main():
    global window_name

    if not arguments.save_path:
        print("You have to specify the path to a folder where cropped frames will be saved.")
        sys.exit()
    save_path = arguments.save_path  # Path to save frames cropped

    once_in_N_frames = arguments.frame  # Save a frame once in N frames

    window_name = "Cropping frames good sir"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    if arguments.video:
        video_path = arguments.video
        if not any(video_path.endswith(ext) for ext in ['.mp4', '.MP4']):
            print("You were supposed to provide a videofile. Giving up.")
            sys.exit()
        output_name = os.path.basename(video_path)[:-4]
        cap = cv2.VideoCapture(video_path)
        crop_frames(cap, save_path, once_in_N_frames, output_name)

    elif arguments.folder:
        #To process all videos in a folder
        if not os.path.isdir(arguments.folder):
            print("You were supposed to provide a folder. Giving up.")

        for video in os.listdir(arguments.folder):
            if not any(video.endswith(ext) for ext in ['.mp4', '.MP4']):  # Discard everything except what we are after
                continue
            video_path = os.path.join(arguments.folder, video)
            output_name = video[:-4]
            cap = cv2.VideoCapture(video_path)
            crop_frames(cap, save_path, once_in_N_frames, output_name)

    else:
        print("Incorrect input. Giving up")

    print("Done. Exiting the script.")
    sys.exit()

if __name__ == '__main__':
    main()