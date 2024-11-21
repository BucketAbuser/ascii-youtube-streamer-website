import cv2
from PIL import Image

def extract_frames(video_path):
    """
    Extract frames from the video file.
    """
    vidcap = cv2.VideoCapture(video_path)

    if not vidcap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    frames = []
    success, image = vidcap.read()

    while success:
        # Convert BGR (OpenCV format) to RGB (Pillow format)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        frames.append(pil_image)
        success, image = vidcap.read()

    vidcap.release()

    if len(frames) == 0:
        raise ValueError(f"No frames extracted from video: {video_path}")

    return frames
