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
fps = 20

day_files = get_images_path("DB_video/DAY/rgb")
seg_files = get_images_path("DB_video/DAY/seg")
ngt_files = get_images_path("DB_video/NIGHT/rgb")


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.avi', fourcc, fps, (width, height))

for i in tqdm(range(1, len(day_files))):
    day = cv2.imread(day_files[i])
    ngt = cv2.imread(ngt_files[i])
    seg = cv2.imread(seg_files[i])

    ngt = cv2.resize(ngt, (640, height))
    day = cv2.resize(day, (640, height))
    seg = cv2.resize(seg, (640, height))

    img = cv2.hconcat([day, seg, ngt])
    video.write(img)

cv2.destroyAllWindows()
video.release()
