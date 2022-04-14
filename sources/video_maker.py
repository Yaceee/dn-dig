import cv2
from tqdm import tqdm
from os.path import join
from glob import glob
import re


def get_images_path(dir):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]

    return sorted(glob(join(dir, "*.png")), key=alphanum_key)


width = 1920
height = 1080
fps = 5

left_path = "../DB_fps_1/DAY/rgb"
center_path = "../DB_fps_0d75/DAY/rgb"
right_path = "../DB_fps_0d5/DAY/rgb"

left_files = get_images_path(left_path)
center_files = get_images_path(center_path)
right_files = get_images_path(right_path)

fourc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.avi', fourc, fps, (width, height))

for i in tqdm(range(1, len(left_files))):
    l = cv2.imread(left_files[i])
    c = cv2.imread(center_files[i])
    r = cv2.imread(right_files[i])

    l = cv2.resize(l, (640, height))
    c = cv2.resize(c, (640, height))
    r = cv2.resize(r, (640, height))

    img = cv2.hconcat([l, c, r])
    video.write(img)

cv2.destroyAllWindows()
video.release()
