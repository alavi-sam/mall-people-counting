import cv2
from glob import glob
import os
from tqdm import tqdm


def capture_frames(*path: str) -> list:
    return glob(os.path.join(*path, '*.jpg'))


def frame_to_video(video_frames: list, output_name: str = 'output.mp4', frame_rate=5):
    sample_frame = cv2.imread(video_frames[0])
    frame_height, frame_width, _ = sample_frame.shape
    video_format = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_name, video_format, frame_rate, (frame_width, frame_height))

    for frame_address in tqdm(video_frames):
        frame = cv2.imread(frame_address)
        if frame is not None:
            writer.write(frame)
        else:
            print(f'Failed to load frame: {frame_address}')
        # writer.write(frame)

    writer.release()


frames = capture_frames('dataset', 'frames')

frame_to_video(frames)
